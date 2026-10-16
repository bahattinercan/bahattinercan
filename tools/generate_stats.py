"""Profil katki kartini kendi verimizden uretir (harici servis yok).

Kaynak: https://github.com/users/<user>/contributions
Bu HTML, GitHub'in gorunur katki grafiginin aynisi; ozel repolardaki
katkilar da sayiya dahil. Ucuncu parti kartlar (github-readme-stats,
streak-stats) bunu gosteremez ve biri coktugunde profil bozulur.

Cikti: assets/generated/contributions.svg (light) ve -dark.svg
"""
import io
import os
import re
import sys
import urllib.request
from datetime import date

USER = "bahattinercan"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets", "generated")
URL = f"https://github.com/users/{USER}/contributions"

MONTHS_TR = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]

THEMES = {
    "dark": {
        "bg": "#0d1117", "bg2": "#101a24", "border": "#30363d",
        "accent_a": "#39d353", "accent_b": "#2dd4bf",
        "title": "#8b949e", "num": "#e6edf3", "label": "#8b949e",
        "levels": ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
    },
    "light": {
        "bg": "#ffffff", "bg2": "#f1f8f5", "border": "#d0d7de",
        "accent_a": "#1f883d", "accent_b": "#0f766e",
        "title": "#57606a", "num": "#1f2328", "label": "#6e7681",
        "levels": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
    },
}


def fetch(user):
    req = urllib.request.Request(
        URL.replace(USER, user),
        headers={"User-Agent": "Mozilla/5.0 (profile-stats-card)"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def parse(html):
    """(gun, katki, seviye) listesi dondurur; tarihe gore artan.

    Not: GitHub'in isaretlemesinde nitelik sirasi sabit degil
    (data-date ... id ... data-level) ve id tarih degil sutun-satir tasir;
    bu yuzden her <td> etiketi ayri ayri cozumlenir.
    """
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html))
    days = []
    for tag in re.findall(r"<td\b[^>]*data-date=[^>]*>", html):
        d = re.search(r'data-date="([0-9]{4}-[0-9]{2}-[0-9]{2})"', tag)
        lvl = re.search(r'data-level="(\d)"', tag)
        cid = re.search(r'id="([^"]+)"', tag)
        if not (d and lvl):
            continue
        t = tips.get(cid.group(1), "") if cid else ""
        cm = re.match(r"(\d+|No) contribution", t)
        n = 0 if (not cm or cm.group(1) == "No") else int(cm.group(1))
        days.append((d.group(1), n, int(lvl.group(1))))
    days.sort(key=lambda x: x[0])
    return days


def streaks(days):
    cur = 0
    for _, n, _ in reversed(days):
        if n > 0:
            cur += 1
        else:
            break
    best = run = 0
    for _, n, _ in days:
        run = run + 1 if n > 0 else 0
        best = max(best, run)
    return cur, best


def fmt(d):
    y, m, dd = d.split("-")
    return f"{int(dd)} {MONTHS_TR[int(m) - 1]}"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render(days, theme_name):
    t = THEMES[theme_name]
    total = sum(n for _, n, _ in days)
    active = sum(1 for _, n, _ in days if n > 0)
    cur, best = streaks(days)
    best_day = max(days, key=lambda x: x[1])
    if not days:
        raise SystemExit("katki verisi bulunamadi")

    # Haftalik izgara: ilk gunu Pazar'a hizala
    W = 1100
    PAD = 30
    LABEL_SPACE = 34  # sagda Pzt/Car/Cum etiketleri icin
    dow = (date.fromisoformat(days[0][0]).weekday() + 1) % 7  # Pazar = 0
    cells = [None] * dow + [(n, lvl) for _, n, lvl in days]
    while len(cells) % 7:
        cells.append(None)
    weeks = len(cells) // 7

    # Izgarayi (etiket payi disinda) kartin tum genisligine yay
    slot = (W - 2 * PAD - LABEL_SPACE) / weeks
    GAP = slot * 0.20
    CELL = slot - GAP
    grid_w = weeks * slot - GAP
    grid_h = 7 * slot - GAP
    grid_y = 152
    H = int(grid_y + grid_h + 28)
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="{total} katkı, son 12 ay, {active} aktif gün">'
    )
    parts.append("<defs>")
    parts.append(
        '<linearGradient id="ac" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{t["accent_a"]}"/>'
        f'<stop offset="1" stop-color="{t["accent_b"]}"/></linearGradient>'
    )
    parts.append(
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["bg"]}"/>'
        f'<stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>'
    )
    parts.append("</defs>")
    parts.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')
    parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" '
                 f'fill="none" stroke="{t["border"]}"/>')

    ff = "font-family=\"'Segoe UI',Ubuntu,Roboto,Helvetica,Arial,sans-serif\""
    parts.append(
        f'<text x="{PAD}" y="42" {ff} font-size="13" fill="{t["title"]}" '
        f'letter-spacing="2.4">SON 12 AY KATKI</text>'
    )
    rng = f'{fmt(days[0][0])} {days[0][0][:4]} – {fmt(days[-1][0])} {days[-1][0][:4]}'
    parts.append(
        f'<text x="{W-PAD}" y="42" text-anchor="end" {ff} font-size="13" '
        f'fill="{t["title"]}">{esc(rng)}</text>'
    )

    stats = [
        (f"{total:,}".replace(",", "."), "toplam katkı"),
        (str(active), "aktif gün"),
        (f"{cur}", "şu anki seri"),
        (f"{best} gün", "en uzun seri"),
        (f'{best_day[1]}', f"en yoğun gün · {fmt(best_day[0])}"),
    ]
    x = PAD
    for i, (val, lab) in enumerate(stats):
        parts.append(
            f'<text x="{x}" y="102" {ff} font-size="30" font-weight="700" '
            f'fill="{t["num"]}">{esc(val)}</text>'
        )
        parts.append(
            f'<text x="{x}" y="124" {ff} font-size="12" fill="{t["label"]}">{esc(lab)}</text>'
        )
        x += 172

    # izgara
    for idx, cell in enumerate(cells):
        week, dowi = divmod(idx, 7)
        cx = PAD + week * slot
        cy = grid_y + dowi * slot
        if cell is None:
            fill = "none"
        else:
            n, lvl = cell
            fill = t["levels"][max(0, min(4, lvl))]
        parts.append(
            f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{CELL:.1f}" height="{CELL:.1f}" '
            f'rx="2.4" fill="{fill}"/>'
        )

    # gun etiketleri (Pzt/Car/Cum) — izgaranin saginda
    lx = PAD + grid_w + 9
    for name, dowi in (("Pzt", 1), ("Çar", 3), ("Cum", 5)):
        parts.append(
            f'<text x="{lx:.1f}" y="{grid_y + dowi * slot + CELL - 1:.1f}" '
            f'{ff} font-size="10" fill="{t["label"]}">{name}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    user = sys.argv[1] if len(sys.argv) > 1 else USER
    html = fetch(user)
    days = parse(html)
    if len(days) < 30:
        raise SystemExit(f"beklenenden az gun dondu: {len(days)}")
    os.makedirs(OUT_DIR, exist_ok=True)
    for theme, suffix in (("light", ""), ("dark", "-dark")):
        svg = render(days, theme)
        p = os.path.join(OUT_DIR, f"contributions{suffix}.svg")
        io.open(p, "w", encoding="utf-8").write(svg)
        print(f"  {os.path.basename(p):26s} {len(svg):>6} bayt")
    total = sum(n for _, n, _ in days)
    active = sum(1 for _, n, _ in days if n > 0)
    print(f"{user}: {len(days)} gun, {total} katki, {active} aktif gun "
          f"({days[0][0]} -> {days[-1][0]})")


if __name__ == "__main__":
    main()
