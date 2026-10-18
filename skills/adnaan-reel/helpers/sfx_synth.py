"""Synthesize the edit's sound-effect kit: whoosh, chime, ticks, ping, sub-drop, flick.

Everything is generated from numpy noise and sine partials (no samples), with a
fixed seed per sound, so the same command always writes byte-identical files.
Output is 48 kHz stereo 16-bit WAV, peaks <= 0.95.

  whoosh.wav   every layout change; swells to its PEAK AT 0.25 s, so place it
               0.25 s before the cut (see ATTACK_S)
  chime.wav    two-tone bell, a new numbered section
  ticks.wav    six quick clicks, a highlight or typing
  ping.wav     single bright bell, a logo or sticker pop
  subdrop.wav  pitch-falling sub hit, the hook
  flick.wav    short noise flick, a card entrance

ATTACK_S maps each name to the time of its peak in seconds: start the sound at
(event time - ATTACK_S[name]) so the loudest moment lands on the event.

Usage:
    python helpers/sfx_synth.py                       # writes <skill>/assets/sfx/*.wav
    python helpers/sfx_synth.py --out /path/to/sfx    # somewhere else
    python helpers/sfx_synth.py --only whoosh ping
    python helpers/sfx_synth.py --list                # name, duration, attack (time of peak)
"""

from __future__ import annotations

import argparse
import sys
import wave
from pathlib import Path
from typing import Callable

import numpy as np

SR = 48000
SEED = 7
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "assets" / "sfx"
# whoosh/ping in assets/sfx are the ElevenLabs house kit (v4) — never overwrite them by default
PROTECTED = {"whoosh", "ping"}

# Time of each sound's peak, in seconds. Kept in step with the synthesis by the tests.
ATTACK_S: dict[str, float] = {
    "whoosh": 0.25,
    "chime": 0.0,
    "ticks": 0.0,
    "ping": 0.0,
    "subdrop": 0.0,
    "flick": 0.0,
}


# -------- building blocks ----------------------------------------------------------


def _time(seconds: float) -> np.ndarray:
    return np.arange(int(round(SR * seconds))) / SR


def _bandpass(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """Brick-wall band-pass in the frequency domain."""
    spec = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    spec[(freqs < lo) | (freqs > hi)] = 0
    return np.fft.irfft(spec, len(x))


def _bell(freq: float, seconds: float, decay: float,
          partials: tuple[tuple[float, float], ...] = ((2, 0.12), (3, 0.04)),
          attack: float = 0.004) -> np.ndarray:
    """Sine with a few harmonics, a linear attack and an exponential decay."""
    t = _time(seconds)
    s = np.sin(2 * np.pi * freq * t)
    for mult, amp in partials:
        s += amp * np.sin(2 * np.pi * freq * mult * t)
    return s * np.clip(t / attack, 0, 1) * np.exp(-decay * t)


def _reverb(x: np.ndarray, rng: np.random.Generator, length: float, wet: float) -> np.ndarray:
    """Noise-burst impulse response: a small, cheap room tail."""
    n = int(SR * length)
    ir = rng.standard_normal(n) * np.exp(-6 * np.arange(n) / n)
    ir *= 3 / np.abs(ir).sum()
    tail = np.convolve(x, ir)
    dry = np.zeros(len(tail))
    dry[:len(x)] = x
    return dry * (1 - wet) + tail * wet


def _mix(events: list[tuple[float, np.ndarray]], seconds: float) -> np.ndarray:
    out = np.zeros(int(SR * seconds))
    for offset, sig in events:
        i = int(offset * SR)
        n = min(len(sig), len(out) - i)
        out[i:i + n] += sig[:n]
    return out


def _normalize(x: np.ndarray, peak: float) -> np.ndarray:
    return x / np.abs(x).max() * peak


# -------- the kit --------------------------------------------------------------------


def whoosh(rng: np.random.Generator) -> np.ndarray:
    t = _time(0.55)
    swell = np.where(t < 0.25, (t / 0.25) ** 2.2, np.exp(-(t - 0.25) * 14))
    return _normalize(_bandpass(rng.standard_normal(len(t)), 700, 9000) * swell, 0.7)


def chime(rng: np.random.Generator) -> np.ndarray:
    # The lower second tone sits under the first so the peak (the attack) stays on the onset.
    two_tone = _mix([(0.0, _bell(2637, 0.6, 9)), (0.11, 0.5 * _bell(2088, 0.9, 7))], 1.4)
    return _normalize(_reverb(two_tone, rng, 0.8, 0.25), 0.8)


def ticks(rng: np.random.Generator) -> np.ndarray:
    def tick() -> np.ndarray:
        return _bell(3510, 0.05, 90, partials=((2, 0.05),), attack=0.001)
    clicks = _mix([(k * 0.062, tick() * (1 - 0.08 * k)) for k in range(6)], 0.8)
    return _normalize(_reverb(clicks, rng, 0.3, 0.15), 0.6)


def ping(rng: np.random.Generator) -> np.ndarray:
    return _normalize(_reverb(_mix([(0.0, _bell(3060, 0.5, 14))], 1.0), rng, 0.7, 0.25), 0.7)


def subdrop(rng: np.random.Generator) -> np.ndarray:
    t = _time(1.6)
    freq = 45 + 65 * np.exp(-6 * t)                    # 110 Hz falling to 45 Hz
    phase = 2 * np.pi * np.cumsum(freq) / SR
    body = np.tanh(1.6 * np.sin(phase)) * np.exp(-2.2 * t) * np.clip(t / 0.003, 0, 1)
    click = rng.standard_normal(len(t)) * np.exp(-t / 0.004) * 0.3
    return _normalize(body + click, 0.95)


def flick(rng: np.random.Generator) -> np.ndarray:
    t = _time(0.12)
    env = np.exp(-t / 0.012) * np.clip(t / 0.0015, 0, 1)
    return _normalize(_bandpass(rng.standard_normal(len(t)), 1800, 7000) * env, 0.8)


SOUNDS: dict[str, Callable[[np.random.Generator], np.ndarray]] = {
    "whoosh": whoosh, "chime": chime, "ticks": ticks,
    "ping": ping, "subdrop": subdrop, "flick": flick,
}


def synth(name: str) -> np.ndarray:
    """Mono float signal for one sound. Each sound has its own seeded generator, so
    output does not depend on which other sounds are generated or in what order."""
    index = list(SOUNDS).index(name)
    return SOUNDS[name](np.random.default_rng([SEED, index]))


def to_pcm_stereo(x: np.ndarray) -> bytes:
    pcm = np.round(np.clip(x, -1, 1) * 32767).astype("<i2")
    return np.repeat(pcm, 2).tobytes()                  # interleaved L R


def write_wav(path: Path, x: np.ndarray) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(to_pcm_stereo(x))


def peak_time(x: np.ndarray) -> float:
    return float(np.argmax(np.abs(x))) / SR


def generate(out_dir: Path, names: list[str] | None = None) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in names or list(SOUNDS):
        path = out_dir / f"{name}.wav"
        write_wav(path, synth(name))
        paths.append(path)
    return paths


def main() -> None:
    ap = argparse.ArgumentParser(description="Synthesize the SFX kit (48 kHz stereo 16-bit WAV)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output directory (default: {DEFAULT_OUT})")
    ap.add_argument("--only", nargs="+", choices=list(SOUNDS), help="generate just these sounds")
    ap.add_argument("--list", action="store_true", help="print name, duration and attack (time of peak); write nothing")
    args = ap.parse_args()

    if args.list:
        print(f"{'name':<8} {'duration':>9} {'attack':>8}")
        for name in args.only or list(SOUNDS):
            x = synth(name)
            print(f"{name:<8} {len(x) / SR:>8.3f}s {peak_time(x):>7.3f}s")
        return
    names = args.only or [n for n in SOUNDS if not (args.out == DEFAULT_OUT and n in PROTECTED)]
    if args.out == DEFAULT_OUT and set(names) & PROTECTED:
        sys.exit("whoosh/ping in assets/sfx are the ElevenLabs kit; write synth versions with --out assets/sfx/synth")
    for path in generate(args.out, names):
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
