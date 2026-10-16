"""Pin'lenecek / vitrinde gorunecek public repolarin metadata'sini doldurur.

description + topics + homepage alanlarini GitHub API uzerinden gunceller.
Bos birakilan alanlara dokunulmaz.
"""
import json
import subprocess
import sys
import tempfile

OWNER = "bahattinercan"

# repo -> (description, [topics], homepage)
META = {
    "russia-plague-website": (
        "Haber iddialarını kaç bağımsız kaynağın bildirdiğine göre etiketleyen izleme "
        "platformu — \"doğrulandı\" demez, kaynak bağımsızlığını ölçer. Next.js + TypeScript",
        ["nextjs", "typescript", "drizzle-orm", "news-monitoring", "open-source",
         "disease-surveillance", "public-health"],
        "https://plague-tracker.vercel.app",
    ),
    "doner-website": (
        "Lokanta / dönerci için sıfır bağımlılık statik sipariş sitesi — WhatsApp sipariş, "
        "gece modu, localStorage sepet. HTML/CSS/JS",
        ["html", "css", "javascript", "static-site", "restaurant", "whatsapp",
         "dark-mode", "no-dependencies"],
        None,
    ),
    "barber_shops": (
        "Berber randevu ve personel yönetimi — Flutter mobil uygulaması (müdür, çalışan ve "
        "admin rolleri)",
        ["flutter", "dart", "mobile-app", "appointment-booking", "barber", "firebase"],
        None,
    ),
    "barber-shops-api": (
        "Barber Shops uygulamasının Node.js + Express REST API'si — randevu, dükkan, servis, "
        "yorum, favori ve rol bazlı yetkilendirme",
        ["nodejs", "express", "rest-api", "javascript", "mongodb", "role-based-access-control"],
        None,
    ),
    "e-commerce-backend": (
        "E-ticaret vitrin ve admin paneli için Express + MongoDB backend — oturum ve güvenlik "
        "testleri dahil",
        ["nodejs", "express", "mongodb", "mongoose", "rest-api", "ecommerce"],
        None,
    ),
    "e-commerce-frontend": (
        "React e-ticaret vitrin arayüzü — ürün listeleme, sepet, giriş/kayıt",
        ["react", "javascript", "ecommerce", "responsive-design"],
        None,
    ),
    "e-commerce-admin": (
        "E-ticaret yönetim paneli — ürün ve sipariş yönetimi (React)",
        ["react", "javascript", "admin-dashboard", "ecommerce"],
        None,
    ),
    "smart_home_design": (
        "Akıllı ev kontrolü mobil arayüz tasarımı (Flutter)",
        ["flutter", "dart", "ui-design", "mobile-app"],
        None,
    ),
    "smart-home-design-2": (
        "Akıllı ev arayüzü — ikinci tasarım denemesi (Flutter)",
        ["flutter", "dart", "ui-design"],
        None,
    ),
    "amazon-clone": (
        "Amazon arayüz klonu — saf HTML/CSS/JS layout çalışması",
        ["html", "css", "javascript", "clone", "practice-project"],
        None,
    ),
    "steam-layout": (
        "Steam mağaza arayüzünün yeniden yorumu (HTML/CSS)",
        ["html", "css", "layout", "clone", "practice-project"],
        None,
    ),
    "edusity": (
        "Eğitim platformu arayüz çalışması (HTML/CSS/JS)",
        ["html", "css", "javascript", "layout"],
        None,
    ),
    "instagram_frontend": (
        "Instagram mobil arayüz klonu (Flutter)",
        ["flutter", "dart", "ui-design", "clone"],
        None,
    ),
    "tiktok_frontend": (
        "TikTok mobil arayüz klonu (Flutter)",
        ["flutter", "dart", "ui-design", "clone"],
        None,
    ),
    "flutter-responsive-ui": (
        "Responsive Flutter layout referansı — cihaz boyutuna göre uyarlanan iskelet",
        ["flutter", "dart", "responsive-design", "ui"],
        None,
    ),
    "flutter-neumorphism-design": (
        "Neumorphism UI komponent seti (Flutter)",
        ["flutter", "dart", "neumorphism", "ui-design", "components"],
        None,
    ),
    "math-vr": (
        "VR matematik etkileşimi prototipi (Unity/C#)",
        ["unity", "csharp", "vr", "education", "prototype"],
        None,
    ),
    "weapon-craft-run-clone": (
        "Weapon Craft Run mekanik incelemesi ve klonu (Unity/C#)",
        ["unity", "csharp", "game-development", "prototype"],
        None,
    ),
    "b2b-site": (
        "B2B satış sitesi (PHP)",
        ["php", "html", "css", "b2b"],
        None,
    ),
    "b2b-site-angular": (
        "B2B satış sitesinin Angular sürümü",
        ["angular", "typescript", "b2b"],
        None,
    ),
    "toggle-crm-api": (
        "Toggle zamanlayıcılarını CRM'e aktarıp işlem yapan entegrasyon API'si",
        ["nodejs", "javascript", "integration", "api"],
        None,
    ),
    "digi_gfp_api": (
        "Dijital GFP projesinin Node.js API'si",
        ["nodejs", "javascript", "api"],
        None,
    ),
    "cafe_api": (
        "Kafe keşif uygulaması için REST API",
        ["nodejs", "javascript", "express", "api"],
        None,
    ),
}


def gh_api(method, path, payload=None):
    cmd = ["gh", "api", "-X", method, path]
    tmp = None
    if payload is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                          encoding="utf-8")
        json.dump(payload, tmp, ensure_ascii=False)
        tmp.close()
        cmd += ["--input", tmp.name]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    finally:
        if tmp:
            import os
            os.unlink(tmp.name)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    only = sys.argv[1:] or list(META)
    ok = fail = 0
    for repo in only:
        desc, topics, homepage = META[repo]
        body = {"description": desc}
        if homepage:
            body["homepage"] = homepage
        rc, out = gh_api("PATCH", f"repos/{OWNER}/{repo}", body)
        if rc != 0:
            print(f"  HATA  {repo}: {out.strip()[:200]}")
            fail += 1
            continue
        rc, out = gh_api("PUT", f"repos/{OWNER}/{repo}/topics", {"names": topics})
        if rc != 0:
            print(f"  KISMI {repo}: description ok, topics hata: {out.strip()[:160]}")
            fail += 1
            continue
        print(f"  ok    {repo}  ({len(topics)} topic)")
        ok += 1
    print(f"\n{ok} repo guncellendi, {fail} sorun.")


if __name__ == "__main__":
    main()
