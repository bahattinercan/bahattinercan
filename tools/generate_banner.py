"""Profil banner ve social preview SVG'lerini tek kaynaktan uretir.

Kullanim:
    python tools/generate_banner.py

Cikti:
    assets/banner-dark.svg   1280x220
    assets/banner-light.svg  1280x220
    assets/social-preview.svg 1280x640 (GitHub sosyal kart)

Bagimlilik yok. Renkler tema sozlugunde; iki tema ayni yerlesimi paylasir,
boylece koyu/acik varyant birbirinden kaymaz.
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

SANS = "'Segoe UI',Ubuntu,Roboto,Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',ui-monospace,Consolas,'Liberation Mono',Menlo,monospace"

NAME = "Bahattin Ercan"
ROLE = "COMPUTER ENGINEER"
STACK = "Django / DRF \u00b7 Node.js \u00b7 Flutter \u00b7 TypeScript \u00b7 PostgreSQL"
# Mobil varyant: 640 px genislikte tek satir okunmuyor, iki satira bolunur.
STACK_MOBILE = ["Django / DRF \u00b7 Node.js \u00b7 Flutter", "TypeScript \u00b7 PostgreSQL"]
META = "K\u00fctahya, Turkey \u00b7 4+ years professional \u00b7 English C1"
PROMPT_DIR = "~/bahattin"
PROMPT_CMD = "whoami"
CHIP = "[ OK ] open to work"

DARK = {
    "bg0": "#0d1117",
    "bg1": "#101a24",
    "fg": "#e6edf3",
    "muted": "#9aa4ae",
    "dim": "#6e7681",
    "accent0": "#39d353",
    "accent1": "#2dd4bf",
    "dot": "#8b949e",
    "dot_op": "0.14",
    "glow0_op": "0.20",
    "glow1_op": "0.20",
    "border_op": "0.22",
    "chip_fill_op": "0.10",
    "caret_op": "0.9",
}

LIGHT = {
    "bg0": "#ffffff",
    "bg1": "#f2f8f6",
    "fg": "#1f2328",
    "muted": "#57606a",
    "dim": "#6e7681",
    "accent0": "#1f883d",
    "accent1": "#0f766e",
    "dot": "#1f2328",
    "dot_op": "0.10",
    "glow0_op": "0.10",
    "glow1_op": "0.10",
    "border_op": "0.28",
    "chip_fill_op": "0.08",
    "caret_op": "1",
}


def defs(t, h):
    return f"""  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg0']}"/>
      <stop offset="0.6" stop-color="{t['bg0']}"/>
      <stop offset="1" stop-color="{t['bg1']}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['accent0']}"/>
      <stop offset="1" stop-color="{t['accent1']}"/>
    </linearGradient>
    <radialGradient id="glow-a" cx="0.08" cy="0.1" r="0.8">
      <stop offset="0" stop-color="{t['accent0']}" stop-opacity="{t['glow0_op']}"/>
      <stop offset="1" stop-color="{t['accent0']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow-b" cx="0.95" cy="1" r="0.75">
      <stop offset="0" stop-color="{t['accent1']}" stop-opacity="{t['glow1_op']}"/>
      <stop offset="1" stop-color="{t['accent1']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.5" fill="{t['dot']}" fill-opacity="{t['dot_op']}"/>
    </pattern>
    <clipPath id="frame">
      <rect width="1280" height="{h}" rx="16"/>
    </clipPath>
  </defs>
"""


def halo(t, w, h):
    """Arka plan: gradyan + nokta dokusu + iki yumusak isik."""
    return f"""  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" fill="url(#dots)"/>
  <rect width="{w}" height="{h}" fill="url(#glow-a)"/>
  <rect width="{w}" height="{h}" fill="url(#glow-b)"/>
"""


def prompt(t, x, y, size):
    """`~/bahattin $ whoami` satiri + yanip sonen imlec."""
    gap = round(size * 0.55, 1)
    return (
        f'    <text x="{x}" y="{y}" font-size="{size}" fill="{t["accent0"]}">'
        f'{PROMPT_DIR}</text>\n'
        f'    <text x="{x + round(len(PROMPT_DIR) * size * 0.6 + gap, 1)}" y="{y}" '
        f'font-size="{size}" fill="{t["dim"]}">$</text>\n'
        f'    <text x="{x + round(len(PROMPT_DIR) * size * 0.6 + gap * 2 + size * 0.6, 1)}" '
        f'y="{y}" font-size="{size}" fill="{t["fg"]}">{PROMPT_CMD}</text>\n'
        f'    <rect x="{x + round(len(PROMPT_DIR + " $ " + PROMPT_CMD) * size * 0.6 + gap, 1)}" '
        f'y="{y - size * 0.82}" width="{round(size * 0.52, 1)}" '
        f'height="{size}" fill="{t["accent0"]}" fill-opacity="{t["caret_op"]}"/>\n'
    )


def chip(t, x, y, h=26, size=13):
    """[ OK ] open to work cipi."""
    w = round(len(CHIP) * size * 0.62 + 26, 1)
    return f"""    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}"
          fill="{t['accent0']}" fill-opacity="{t['chip_fill_op']}"
          stroke="{t['accent0']}" stroke-opacity="0.45"/>
    <text x="{x + 13}" y="{y + h / 2 + size * 0.36}" font-size="{size}"
          fill="{t['accent0']}">{CHIP}</text>
"""


def banner(t, theme_name):
    w, h = 1280, 220
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{NAME}, {ROLE.title()}. {STACK}. {META}.">
  <title>{NAME} \u2014 {ROLE.title()}</title>
{defs(t, h)}  <g clip-path="url(#frame)">

{halo(t, w, h)}    <g font-family="{MONO}">
{prompt(t, 72, 62, 16)}    </g>
    <g font-family="{SANS}">
      <text x="70" y="128" font-size="46" font-weight="700" fill="{t['fg']}">{NAME}</text>
      <text x="72" y="160" font-size="16" fill="{t['muted']}">{STACK}</text>
    </g>
    <g font-family="{MONO}">
{chip(t, 72, 176)}{'      '}<text x="{round(len(CHIP) * 13 * 0.62 + 72 + 39, 1)}" y="193" font-size="13"
            fill="{t['dim']}">{META}</text>
    </g>
  </g>

  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="none"
        stroke="{t['accent0']}" stroke-opacity="{t['border_op']}"/>
  <rect x="0" y="0" width="6" height="{h}" fill="url(#accent)"/>
</svg>
"""


def banner_mobile(t):
    """Mobil banner: 640x260, tipografi buyutulmus, stack iki satir."""
    w, h = 640, 260
    stack = "".join(
        f'      <text x="42" y="{136 + i * 21}" font-size="14" fill="{t["muted"]}">{line}</text>' + chr(10)
        for i, line in enumerate(STACK_MOBILE)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{NAME}, {ROLE.title()}. {STACK}. {META}.">
  <title>{NAME} \u2014 {ROLE.title()}</title>
{defs(t, h)}  <g clip-path="url(#frame)">
{halo(t, w, h)}    <g font-family="{MONO}">
{prompt(t, 42, 50, 14)}    </g>
    <g font-family="{SANS}">
      <text x="40" y="108" font-size="40" font-weight="700" fill="{t['fg']}">{NAME}</text>
{stack}    </g>
    <g font-family="{MONO}">
{chip(t, 42, 178, h=24, size=12)}      <text x="42" y="232" font-size="12" fill="{t['dim']}">{META}</text>
    </g>
  </g>

  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="none"
        stroke="{t['accent0']}" stroke-opacity="{t['border_op']}"/>
  <rect x="0" y="0" width="6" height="{h}" fill="url(#accent)"/>
</svg>
"""


def social(t):
    w, h = 1280, 640
    body = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{NAME}, {ROLE.title()}. {STACK}. {META}.">
  <title>{NAME} \u2014 {ROLE.title()}</title>
{defs(t, h)}
{halo(t, w, h)}  <g font-family="{MONO}">
    <text x="88" y="150" font-size="20" letter-spacing="4" fill="{t['accent0']}">{ROLE}</text>
{prompt(t, 88, 208, 22)}  </g>
  <g font-family="{SANS}">
    <text x="84" y="330" font-size="76" font-weight="700" fill="{t['fg']}">{NAME}</text>
    <text x="88" y="392" font-size="24" fill="{t['muted']}">{STACK}</text>
  </g>
  <g font-family="{MONO}">
{chip(t, 88, 432, h=34, size=16)}    <text x="88" y="512" font-size="16" fill="{t['dim']}">{META}</text>
    <text x="88" y="566" font-size="16" fill="{t['dim']}">github.com/bahattinercan</text>
  </g>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" fill="none"
        stroke="{t['accent0']}" stroke-opacity="{t['border_op']}"/>
  <rect x="0" y="0" width="{w}" height="6" fill="url(#accent)"/>
</svg>
"""
    return body


def write(path, body):
    io.open(path, "w", encoding="utf-8", newline="\n").write(body)
    print(f"yazildi: {os.path.relpath(path, ROOT)} ({len(body.encode('utf-8'))} bayt)")


def main():
    for theme, suffix in ((DARK, "dark"), (LIGHT, "light")):
        write(os.path.join(ASSETS, f"banner-{suffix}.svg"), banner(theme, suffix))
        write(os.path.join(ASSETS, f"banner-mobile-{suffix}.svg"), banner_mobile(theme))
    write(os.path.join(ASSETS, "social-preview.svg"), social(DARK))


if __name__ == "__main__":
    main()
