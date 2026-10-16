"""Vitrin repolarina ilk surum etiketini ve release notunu olusturur.

Notlar repolarin gercek iceriginden yazildi; uydurma madde yok.
Surum numaralari durumu yansitir: v0.1.0 = gelistirilmekte olan urun,
v1.0.0 = teslim edilmis/kullanilan is.
"""
import subprocess

OWNER = "bahattinercan"

RELEASES = [
    ("doner-website", "v1.0.0", "Döner Sipariş Sitesi v1.0.0", """\
Lokanta için sıfır bağımlılık statik sipariş sitesi. Derleme adımı ve framework yok.

**İçinde ne var**
- WhatsApp üzerinden sipariş akışı, mobil öncelikli yerleşim
- Gece modu ve `localStorage` sepet (sunucu gerekmez)
- Menü sayfası, iletişim ve KVKK/gizlilik metni
- Vektör logo ve öz barındırılan fontlar — harici istek yok

**Güvenlik**
- CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` başlıkları
- `vercel.json` kaynak deseni `/(.*)` (öncesinde `/**` geçersizdi ve deploy düşüyordu,
  yani başlıklar hiç uygulanmıyordu)

**Dağıtım:** https://doner-website.vercel.app · Lisans: MIT"""),

    ("russia-plague-website", "v1.0.0", "Plague Tracker v1.0.0", """\
Haber iddialarını **kaç bağımsız kaynağın bildirdiğine** göre etiketleyen izleme platformu.

**Temel ilke**
Sistem hiçbir yerde "doğrulandı" / "confirmed" / "verified" demez. Yalnızca hangi kaynağın
ne bildirdiğini raporlar. Etiketler: resmî açıklama · çoklu bağımsız kaynak bildiriyor ·
tek kaynak bildiriyor · doğrulanmamış iddia · çelişkili bilgi.

**Teknik**
- Next.js + TypeScript + Drizzle ORM
- Bağımsızlık grupları: aynı olayı bildiren kaynaklar bağımsızlık açısından gruplanır,
  etiket bu grupların sayısına göre atanır
- Kaynak sağlığı takibi ve son tarama durumunun arayüzde gösterimi
- TR/EN arayüz

**Dağıtım:** https://plague-tracker.vercel.app · Lisans: MIT"""),

    ("local-ai-news", "v0.1.0", "OpenWeight Radar v0.1.0", """\
Yerelde çalıştırılabilir **açık ağırlıklı AI modellerini** kategori sekmeleriyle takip eden,
haber akışı zamanlanmış olarak güncellenen izleme sitesi.

**Bu sürümde**
- Hugging Face tabanlı ingest: yeni yayınlanan modelleri toplar, kategorilere ayırır
- Snapshot depolama (Vercel Blob) — uygulama veritabanı gerektirmez
- `npm run classify-check`: 40 fixture model ile **sınıflandırma regresyon kapısı**
- `npm run sources-check`: kaynak sağlık raporu (çevrimdışı fixture desteğiyle)
- Filtreler (pencere, sıralama, kalite kapısı, runner, boyut, lisans), kaydedilmiş filtreler
- RSS, sitemap ve TR/EN `hreflang`

**Durum:** geliştirme sürümü. Üretim sertleştirmesi ve dağıtımı açık.
`openweightradar.com` alan adı henüz yayında değil."""),

    ("beauty-salon", "v0.1.0", "Beauty Salon Platform v0.1.0", """\
Çok kiracılı güzellik salonu platformu: 4 uygulama, tek API.

**İçinde ne var**
- `apps/api` — Express 5 + Sequelize 6, JWT (kısa ömürlü access + refresh), rol bazlı yetkilendirme
- `apps/admin_panel` — Next.js 16 platform yönetim paneli
- `apps/customer_app` / `apps/salon_app` — Flutter müşteri ve salon uygulamaları
- 12 tablo, 14 route grubu, kiracı izolasyonu test edilmiş

**Test:** 535 test çalıştırılarak doğrulandı (API 286, customer 201, salon 48)

**Güvenlik**
- Üretimde (`NODE_ENV=production`) demo şifreleriyle seed **reddedilir**;
  `SEED_*_PASSWORD` zorunlu
- Yönetim panelinde giriş formu üretim derlemesinde boş açılır (demo ön doldurma
  `NODE_ENV` kapısıyla dead-code olarak elenir)
- `.env`, `*.sqlite` ve `uploads/` izlenmez

**Bilinen sınırlar:** migration yok (`sequelize.sync()` + `ensureColumns`), admin_panel
test edilmiyor, yüklemeler yerel diske yazılıyor, ödeme entegrasyonu yok."""),

    ("barber_shops", "v1.0.0", "Barber Shops v1.0.0", """\
Berber randevu ve personel yönetimi uygulaması (Flutter).

**İçinde ne var**
- Randevu oluşturma, düzenleme, iptal
- Dükkan yönetimi; hizmet (servis) tanımları
- Kullanıcı tipleri: müdür, çalışan, admin — rol bazlı yetkilendirme
- Yorumlar, favoriler, kullanıcı kaydı ve şifre/e-posta işlemleri
- API tarafı ayrı repoda: `barber-shops-api` (Node.js + Express)

**Lisans:** MIT"""),

    ("unity-prototypes-archive", "v1.0.0", "Unity Prototip Arşivi v1.0.0", """\
2022–2023 arasında Unity/C# ile yazılmış **23 oynanabilir prototipin indeksi**.

Her prototip için ne yaptığı ve hangi sistemlerden oluştuğu (gerçek script adlarından
doğrulanmış) listeleniyor. Ayrıca 23 prototipte tekrar eden desenler ve
"bugün aynısını yazsam" bölümü var.

Türler: hiper-casual/runner, arcade ve spor, platform ve aksiyon-macera, bulmaca ve kelime,
ritim, strateji/savunma, idle, VR, araç.

**Lisans:** MIT"""),
]


def main():
    for repo, tag, title, notes in RELEASES:
        r = subprocess.run(
            ["gh", "release", "create", tag, "--repo", f"{OWNER}/{repo}",
             "--title", title, "--notes", notes],
            capture_output=True, text=True, encoding="utf-8")
        out = (r.stdout or r.stderr or "").strip()
        ok = r.returncode == 0
        print(f"{'ok  ' if ok else 'HATA'} {repo:26s} {tag}")
        if ok:
            print("      ", out.splitlines()[-1] if out else "")
        else:
            print("      ", out[:200])


if __name__ == "__main__":
    main()
