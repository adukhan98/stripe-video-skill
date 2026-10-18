"""The brand layer: one brand file → brand.css (overrides the v7 runtime tokens) → every scene.

The runtime (templates/runtime/v7yt.css/js) carries default tokens; a project's `edit/brand/brand.json` re-points them.
board.py calls `install(hf)` whenever it installs the runtime (prepare / runtime / talkcaps), so every scene picks the
brand up without a manual step. The default brand of this skill is Stripe (brand/stripe.json).

    python3 helpers/brand.py init  --edit-dir E [--brand path.json]   # copy a brand file to E/brand/brand.json (Stripe default)
    python3 helpers/brand.py css   --edit-dir E                      # write E/brand/brand.css from it
    python3 helpers/brand.py apply --edit-dir E                      # css + install into every E/animations/*/hf
"""
import argparse
import json
import re
import shutil
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
DEFAULT = SKILL / "brand" / "stripe.json"
LINK = '<link rel="stylesheet" href="brand.css" />'


def rgb(h: str) -> str:
    h = h.lstrip("#")
    return ", ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def load(edit: Path) -> dict | None:
    p = edit / "brand" / "brand.json"
    return json.loads(p.read_text()) if p.exists() else None


def colors(b: dict) -> dict:
    return {k: v["hex"] for k, v in b["colors"].items()}


def css(edit: Path) -> Path | None:
    b = load(edit)
    if not b:
        return None
    C = colors(b)
    hero = b.get("captions", {}).get("hero", C["primary"])
    out = edit / "brand" / "brand.css"
    out.write_text(f"""/* brand.css — generated from brand/brand.json ({b['name']}) by helpers/brand.py. Edit brand.json, not this. */
:root, body[data-theme], body[data-theme="light"] {{
  --bg: {C['background']}; --card: {C['card']}; --ink: {C['text']}; --muted: {C['muted']};
  --brand-primary: {C['primary']}; --brand-primary-dark: {C['primary_dark']}; --brand-deep: {C['deep']};
  --brand-text: {C['text']}; --brand-card: {C['card']};
  --mint-soft: {C['soft']}; --mint-panel: {C['panel']}; --strawberry: {C['data']};
  --disc-shadow: 0 22px 36px -10px rgba({rgb(C['deep'])}, .36), 0 6px 12px -4px rgba({rgb(C['deep'])}, .2);
  --vignette-strong: radial-gradient(ellipse at 50% 42%, transparent 34%, rgba({rgb(C['deep'])}, .30) 100%);
  --shadow: 0 30px 50px -14px rgba({rgb(C['deep'])}, .22), 0 6px 14px -6px rgba({rgb(C['deep'])}, .14);
  --hl: {C['soft']}; --tag: {C['deep']}; --tag-text: #FFFFFF;
  --marker: {C['deep']}; --marker-text: {C['deep']}; --marker-ink: {C['deep']}; --callout: {C['deep']};
  --tile-text: {C['text']};
  --grid-a: rgba({rgb(C['deep'])}, 0.05);
}}
.emph, .mint {{ text-shadow: 0 3px 14px rgba({rgb(C['primary'])}, .18); }}
.w7 .mint, .w7.mint {{ color: {hero}; }}
""")
    return out


def install(hf: Path) -> bool:
    """Copy E/brand/brand.css into a scene and link it right after v7yt.css (idempotent). hf = E/animations/<id>/hf."""
    edit = hf.parents[2]
    src = edit / "brand" / "brand.css"
    if not src.exists() and not css(edit):
        return False
    shutil.copy2(src, hf / "brand.css")
    p = hf / "index.html"
    if p.exists():
        h = p.read_text()
        if 'href="brand.css"' not in h:
            h = re.sub(r'(<link rel="stylesheet" href="v7yt\.css" />)', r"\1\n    " + LINK, h, count=1)
            p.write_text(h)
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["init", "css", "apply"])
    ap.add_argument("--edit-dir", type=Path, required=True)
    ap.add_argument("--brand", type=Path, default=DEFAULT)
    a = ap.parse_args()
    edit = a.edit_dir.resolve()
    if a.cmd == "init":
        (edit / "brand").mkdir(parents=True, exist_ok=True)
        dst = edit / "brand" / "brand.json"
        if dst.exists():
            print(f"{dst} exists — leaving it")
        else:
            shutil.copy2(a.brand, dst)
            print(f"{a.brand.name} → {dst}")
    out = css(edit)
    if not out:
        raise SystemExit(f"no {edit / 'brand' / 'brand.json'} — run `brand.py init` first")
    print("→", out)
    if a.cmd == "apply":
        n = sum(install(hf) for hf in sorted((edit / "animations").glob("*/hf")))
        print(f"brand.css → {n} scene(s)")


if __name__ == "__main__":
    main()
