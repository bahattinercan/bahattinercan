"""Profil README'si icin proje karti gorselleri uretir.

Kaynak: yerel repo ekran goruntuleri + indirilen mobil ekran goruntuleri.
Cikti: assets/projects/*.webp (1200x675, 16:9)
"""
import os
from PIL import Image, ImageDraw, ImageFilter

OUT = "assets/projects"
W, H = 1200, 675
BG = (13, 17, 23)
BORDER = (48, 54, 61)
RADIUS = 10
PAD = 18
GAP = 14

ROOT = "D:/code/projeler"
os.makedirs(OUT, exist_ok=True)


def rrect(im, box, radius, fill=None, outline=None, width=1):
    """Yuvarlatilmis dikdortgen; radius=0 ise normal dikdortgen."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    return Image.alpha_composite(im.convert("RGBA"), layer)


def fit(im, height=None, width=None):
    w, h = im.size
    if height:
        width = max(1, round(w * height / h))
    else:
        height = max(1, round(h * width / w))
    return im.convert("RGB").resize((width, height), Image.LANCZOS)


def crop_16_9(im, top=0):
    w, h = im.size
    target_h = round(w * 9 / 16)
    if h - top < target_h:
        top = max(0, h - target_h)
    return im.convert("RGB").crop((0, top, w, top + target_h))


def canvas():
    return Image.new("RGB", (W, H), BG)


def paste_card(cv, im, x, y):
    """Karti golge + cerceve + yuvarlak kose ile yerlestirir."""
    w, h = im.size
    shadow = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((12, 12, w + 12, h + 12), radius=RADIUS, fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))
    cv.paste(shadow, (x - 12, y - 12), shadow)
    card = rrect(im.convert("RGBA").convert("RGB"), (0, 0, w - 1, h - 1), RADIUS,
                 outline=BORDER)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=RADIUS, fill=255)
    cv.paste(card, (x, y), mask)


def save(cv, name):
    path = os.path.join(OUT, name)
    cv.save(path, "WEBP", quality=86, method=6)
    print(f"  {name:26s} {os.path.getsize(path)//1024:>4} KB")


def row(images, height, name, top_pad=None):
    """Gorselleri tek satirda ortalar."""
    cv = canvas()
    fitted = [fit(i, height=height) for i in images]
    total = sum(i.size[0] for i in fitted) + GAP * (len(fitted) - 1)
    x = (W - total) // 2
    y = (H - height) // 2 if top_pad is None else top_pad
    for im in fitted:
        paste_card(cv, im, x, y)
        x += im.size[0] + GAP
    save(cv, name)


def pair(phone_path, desktop_path, name):
    """Solda telefon, sagda masaustu: telefona gore dikey hizali."""
    cv = canvas()
    phone, desktop = Image.open(phone_path), Image.open(desktop_path)
    ph_h = H - 2 * PAD
    ph = fit(phone, height=ph_h)
    dw = W - 2 * PAD - GAP - ph.size[0]
    dt = fit(desktop, width=dw)
    if dt.size[1] > H - 2 * PAD:  # cok yuksek olursa telefona esitle
        dt = fit(desktop, height=ph_h)
    total = ph.size[0] + GAP + dt.size[0]
    x = (W - total) // 2
    paste_card(cv, ph, x, (H - ph.size[1]) // 2)
    paste_card(cv, dt, x + ph.size[0] + GAP, (H - dt.size[1]) // 2)
    save(cv, name)


def single(src, name, top=0):
    """Tam kare 16:9 karti (arka plan dolgusu yok)."""
    im = crop_16_9(Image.open(src), top=top).resize((W, H), Image.LANCZOS)
    save(im, name)


print("Proje kartlari uretiliyor:")

# 1) OpenWeight Radar — Next.js arayuzu (uzun sayfa, hero bolgesinden kirp)
single(f"{ROOT}/local-ai-news/.shots/audit-v2-feed-1440-dark.png",
       "openweight-radar.webp", top=150)

# 2) Plague Tracker — canli site
single(f"{ROOT}/russia-plague-website/.shots/after2-tr-home.png",
       "plague-tracker.webp", top=0)

# 3) Guzellik salonu platformu — telefon + admin paneli
pair(f"{ROOT}/beauty_salon/screenshots/customer_app/fix01_home.png",
     f"{ROOT}/beauty_salon/screenshots/admin_panel/dark_dashboard.png",
     "beauty-salon.webp")

# 4) Musteri Siparis Takip — Windows masaustu
single(f"{ROOT}/musteri-siparis-takip program\u0131/screenshots/musteriler-liste.png",
       "siparis-takip.webp", top=170)

# 5) Berber randevu uygulamasi — 3 telefon ekrani
phones = [
    "C:/Users/bahat/AppData/Local/Temp/bs/bf6b3254-419b-42c2-a475-1b5aad5c1678.img",
    "C:/Users/bahat/AppData/Local/Temp/bs/8336ec6a-b480-47b7-b246-95dbbc89dc9c.img",
    "C:/Users/bahat/AppData/Local/Temp/bs/0475bbb0-e4b3-40af-b6c4-ddb85f8913d3.img",
]
if all(os.path.exists(p) for p in phones):
    row([Image.open(p) for p in phones], 620, "barber-shops.webp")

# 6) Doner siparis sitesi
single(f"{ROOT}/doner-website/assets/preview.jpg", "doner-website.webp")

# 7) JobRadar — terminal tabanli ingest, ekran goruntusu yok: baslik karti
print("bitti.")
