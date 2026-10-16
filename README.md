<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img src="assets/banner-dark.svg" alt="Bahattin Ercan — Computer Engineer" width="100%">
</picture>

<a href="mailto:bahattin.ercan.43@gmail.com"><img src="https://img.shields.io/badge/bahattin.ercan.43@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="E-posta"></a>
<a href="https://bahattinercan-portfolio.vercel.app"><img src="https://img.shields.io/badge/Portfolyo-39D353?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolyo sitesi"></a>
<a href="https://www.linkedin.com/in/bahattin-ercan"><img src="https://img.shields.io/badge/bahattin--ercan-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<img src="https://img.shields.io/badge/K%C3%BCtahya,%20T%C3%BCrkiye-1f6feb?style=for-the-badge&logo=googlemaps&logoColor=white" alt="Konum">

</div>

## Kısaca

Çok kiracılı iş uygulamaları, Windows masaüstü araçları ve zamanlanmış veri hatları geliştiriyorum.
Arayüzü Flutter/Dart ile mobil ve masaüstünde, TypeScript ile web'de (Next.js + NestJS) yazıyorum;
veri katmanında PostgreSQL, SQLite ve MongoDB kullanıyorum.

İşi "çalışıyor" noktasında bırakmamaya çalışıyorum: kritik mantığı testle kilitliyorum,
kararları ve kısıtları repo içinde dokümante ediyorum, teslim edilebilir bir sürüm çıkarıyorum.

<sub>**In English** — I build multi-tenant business applications, Windows desktop tools and scheduled data pipelines.
Flutter/Dart for mobile & desktop, TypeScript (Next.js + NestJS) for web, PostgreSQL/SQLite/MongoDB for data.
I keep the work past the "it runs" stage: tests around the logic that can silently break, decisions and
constraints documented in the repo, and something that can actually be shipped.</sub>

---

## Ne yapıyorum

| | |
|---|---|
| **Çok kiracılı ürünler** | Güzellik salonu platformu (API + web admin + iki Flutter uygulaması) ve çok şirketli bakım-onarım yönetim sistemi. İzolasyon sınırı tenant/şirket, yetkilendirme rol bazlı. |
| **Masaüstü ve mobil** | Windows'ta kurulan çevrimdışı Flutter masaüstü uygulamaları, Flutter mobil uygulamalar, Kotlin/Android oyun prototipleri. |
| **Zamanlanmış veri hatları** | Kaynaklardan toplayan, normalize eden, sınıflandıran ve snapshot olarak yayınlayan ingest sistemleri (Next.js + GitHub Actions / cron). |
| **Arayüz işçiliği** | Sıfır bağımlılık statik siteler, kurumsal paneller, veri yoğun tablo/rapor ekranları. |

---

## Öne çıkan projeler

<table>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/bahattinercan/local-ai-news"><img src="assets/projects/openweight-radar.webp" alt="OpenWeight Radar — model listesi ve filtre paneli" width="100%"></a>

### OpenWeight Radar &nbsp;·&nbsp; [canlı](https://local-ai-news.vercel.app)

Yerelde çalıştırılabilir **açık ağırlıklı AI modellerini** kategori sekmeleriyle takip eden, haber akışı zamanlanmış olarak güncellenen izleme sitesi.

`Next.js 16` `TypeScript` `Hugging Face` `GitHub Actions`

<sub>Sınıflandırma mantığı 40 fixture'lık regresyon kapısıyla korunuyor; kaynak sağlığı ayrı bir komutla raporlanıyor.</sub>

</td>
<td width="50%" valign="top">

<a href="https://github.com/bahattinercan/beauty-salon"><img src="assets/projects/beauty-salon.webp" alt="Güzellik salonu platformu — müşteri uygulaması ve admin paneli" width="100%"></a>

### Güzellik Salonu Platformu

**Çok kiracılı** salon yönetimi: Express + Sequelize API, Next.js admin paneli, Flutter salon ve müşteri uygulamaları.

`Express` `Sequelize` `Next.js` `Flutter`

<sub>Üretimde varsayılan şifreyle seed çalıştırmayı reddeden koruma; demo veri ile gerçek veri ayrımı.</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/bahattinercan/russia-plague-website"><img src="assets/projects/plague-tracker.webp" alt="Plague Tracker — kaynak izleme panosu" width="100%"></a>

### Plague Tracker &nbsp;·&nbsp; [canlı](https://plague-tracker.vercel.app)

Haber iddialarını **kaç bağımsız kaynağın bildirdiğine** göre etiketleyen izleme sitesi. Sistem hiçbir yerde "doğrulandı" demez; yalnızca kimin ne bildirdiğini raporlar.

`Next.js` `TypeScript` `Drizzle ORM` `Vercel`

<sub>Bağımsızlık grupları, çelişkili bilgi etiketi ve kaynak sağlığı takibi.</sub>

</td>
<td width="50%" valign="top">

<a href="https://github.com/bahattinercan/barber_shops"><img src="assets/projects/barber-shops.webp" alt="Berber randevu uygulaması — giriş, kayıt ve salon ekranları" width="100%"></a>

### Barber Shops

Berber randevu ve personel yönetimi. Flutter uygulaması + Node.js/Express REST API'si; müdür, çalışan ve admin rolleri.

`Flutter` `Dart` `Node.js` `Express`

<sub>Randevu, dükkan, servis, yorum ve favori akışlarının tamamı rol bazlı yetkilendirmeyle korunuyor.</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/bahattinercan/doner-website"><img src="assets/projects/doner-website.webp" alt="Döner sipariş sitesi — ana sayfa" width="100%"></a>

### Döner Sipariş Sitesi &nbsp;·&nbsp; [canlı](https://doner-website.vercel.app)

Lokanta için **sıfır bağımlılık** statik sipariş sitesi: WhatsApp üzerinden sipariş, gece modu, localStorage sepet.

`HTML` `CSS` `JavaScript` `MIT`

<sub>Derleme adımı ve framework yok — dosyayı kopyala, çalışır. Küçük işletmeler için bakımı bedava.</sub>

</td>
<td width="50%" valign="top">

<img src="assets/projects/siparis-takip.webp" alt="Müşteri Sipariş Takip Sistemi — müşteriler ekranı" width="100%">

### Müşteri Sipariş Takip

İmalat atölyesi için sipariş → üretim → tahsilat takibi. **Windows masaüstü, çevrimdışı**, veriler yerel SQLite'ta.

`Flutter` `Dart` `SQLite` `Windows`

<sub>Çok kalemli sipariş, kullanıcı tanımlı üretim aşamaları, kısmi tahsilat, stok ve raporlar. 725 test / 145 Dart dosyası.<br>[Vaka çalışması](https://github.com/bahattinercan/case-studies/blob/main/docs/musteri-siparis-takip.md) · kaynak kod özel.</sub>

</td>
</tr>
</table>

### Bunların dışında

Bazı işler **özel repolarda** yürüyor. Kodları yayınlanmıyor ama mühendislik anlatımları
[kaynak kodu özel olan dört ürünün vaka çalışmaları](https://github.com/bahattinercan/case-studies)
altında: problem, mimari, ölçülmüş kanıt ve bilinen sınırlar.

- **[Bakım Onarım Yönetim Sistemi (CMMS)](https://github.com/bahattinercan/case-studies/blob/main/docs/bakim-onarim-yonetim.md)** —
  Çok şirketli bakım süreci (arıza → SLA → iş emri → saha → kapanış).
  NestJS + Prisma + PostgreSQL, BullMQ outbox, React web, Expo mobil.
  Katman sınırları dependency-cruiser ile denetleniyor; OpenAPI sözleşme kayması CI'da yakalanıyor.
- **[Taskbar Hero](https://github.com/bahattinercan/case-studies/blob/main/docs/new-taskbar-hero.md)** —
  Android için idle RPG. Savaş motoru **saf Kotlin ve sabit adımlı**: aynı seed aynı sonucu
  üretir, denge ölçümü JVM testleriyle tekrarlanabilir. 101 test.
- **[JobRadar](https://github.com/bahattinercan/case-studies/blob/main/docs/find-job.md)** —
  7 kaynaktan iş ilanı toplayan, normalize eden, tekilleştiren ve deterministik skorlayan ingest
  sistemi. Kaynak sağlığı raporu "boru hattı sessizce bozuldu mu?" sorusunu cevaplar.
- **[Müşteri Sipariş Takip](https://github.com/bahattinercan/case-studies/blob/main/docs/musteri-siparis-takip.md)**
  vaka çalışması — 725 test, çevrimdışı lisans/aktivasyon, tek bilgisayar kurulumu.
- **Mavi Konak QR Menü** — Kütahya çini motiflerinden esinlenmiş kafe menüsü sitesi (kaynak özel).
- **[Unity prototip arşivi](https://github.com/bahattinercan/unity-prototypes-archive)** — 2022–2023 arasında C# ile geliştirilmiş 23 oynanabilir prototip:
  hiper-casual, ritim, match-3, üs savunma, VR. Arşiv repo'su mekanikleri ve tekrar eden sistemleri indeksler.
- **E-ticaret üçlüsü** — React vitrin, React admin paneli ve Express + MongoDB backend.

---

## Teknoloji

**Mobil & Masaüstü**
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)
![Dart](https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white)

**Web**
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

**Backend & Veri**
![Node.js](https://img.shields.io/badge/Node.js-5FA04E?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white)
![NestJS](https://img.shields.io/badge/NestJS-E0234E?style=for-the-badge&logo=nestjs&logoColor=white)
![Prisma](https://img.shields.io/badge/Prisma-2D3748?style=for-the-badge&logo=prisma&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![BullMQ](https://img.shields.io/badge/BullMQ-CC0000?style=for-the-badge&logo=redis&logoColor=white)

**Oyun & Sistem**
![C#](https://img.shields.io/badge/C%23-512BD4?style=for-the-badge&logo=csharp&logoColor=white)
![Unity](https://img.shields.io/badge/Unity-000000?style=for-the-badge&logo=unity&logoColor=white)
![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)
![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Araçlar**
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

---

## Nasıl çalışıyorum

- **Test, sonradan eklenen bir katman değil.** Sessizce bozulabilecek mantığın etrafına test yazıyorum:
  sınıflandırma, skorlama, üretim aşamaları, yetkilendirme.
  *Müşteri Sipariş Takip'te 508 test/112 dosya, Taskbar Hero'da 101 JVM testi.*
- **Kararlar repoda.** Neyin neden böyle olduğu, hangi kısıtın kabul edildiği ve nasıl çalıştırılacağı
  kodun yanında duruyor; sözlü aktarılan bilgiye bırakmıyorum.
- **Gerçek veri ile demo veri karışmıyor.** Geliştirme sentetik veriyle yapılıyor; üretimde
  varsayılan şifreyle seed çalıştırmak reddediliyor.
- **Teslim edilebilir sürüm çıkarıyorum.** Kurulum notu, sürüm numarası, sürüm notu ve yedekleme
  olmadan "bitti" demiyorum.

---

## Sayılar

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/generated/contributions-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/generated/contributions.svg">
  <img src="assets/generated/contributions.svg" alt="Son 12 ayda katkı özeti ve günlük katkı ızgarası" width="100%">
</picture>

<sub>Kart her gün otomatik yenileniyor ([`stats.yml`](.github/workflows/stats.yml), veri doğrudan
katkı grafiğinden) ve **özel repolardaki katkıları da sayıyor** — hazır istatistik kartları bunu
gösteremez. Bu yüzden buradaki sayı, üstteki aktivite grafiğiyle aynı kaynaktan gelir; popüler
üçüncü parti kartların gösterdiği daha düşük sayı yanıltıcıdır.</sub>

</div>

---

## Katkı grafiği

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/bahattinercan/bahattinercan/output/github-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/bahattinercan/bahattinercan/output/github-snake.svg">
  <img src="https://raw.githubusercontent.com/bahattinercan/bahattinercan/output/github-snake.svg" alt="Katkı grafiği animasyonu" width="100%">
</picture>

</div>

---

## İletişim

<div align="center">

İş görüşmesi, freelance proje veya teknik soru için e-posta en hızlı yol.
Vaka çalışmaları ve iletişim bilgileri portfolyo sitesinde de var:
[bahattinercan-portfolio.vercel.app](https://bahattinercan-portfolio.vercel.app)

<a href="mailto:bahattin.ercan.43@gmail.com"><img src="https://img.shields.io/badge/E--posta%20g%C3%B6nder-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="E-posta gönder"></a>
<a href="https://bahattinercan-portfolio.vercel.app"><img src="https://img.shields.io/badge/Portfolyo-39D353?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolyo"></a>
<a href="https://www.linkedin.com/in/bahattin-ercan"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>

</div>
