Görseli inceledim, GitHub'ın Markdown motoru bazen `<p align="center">` içindeki `<img>` etiketlerinin ve HTML boşluklarının (`&nbsp;`) altındaki metinle birleşmesine veya hizalamanın bozulmasına neden olabiliyor.

Senin paylaştığın o profesyonel görünümü (Dominos şablonundaki netlikte) tam olarak yakalamak ve o dağınık görüntüden kurtulmak için temizlenmiş, **boşlukları optimize edilmiş** son halini hazırladım.

Aşağıdaki bağlantıdan en temiz haliyle `.txt` dosyasını indirebilirsin:

[file-tag: code-generated-file-0-1778321625635966138]

### Neyi Düzelttim?

1. **Gereksiz Boşluklar:** `&nbsp;` gibi hatalı karakterleri temizledim, GitHub'ın kendi satır başı mantığına göre düzenledim.
2. **ANSI Bloğu:** ````ansi` etiketini sadece kutu tasarımı için bıraktım, böylece terminal havası bozulmadan net görünecek.
3. **Hizalama:** Badge (rozet) kısmını ve metin bloklarını birbirinden ayırarak sayfanın daha geniş ve ferah durmasını sağladım.

Eğer dosyayı açmakla uğraşmak istemiyorsan, direkt buradan da kopyalayabilirsin (bu sefer hiçbir kayma olmayacak şekilde optimize edildi):

```markdown
# 🎬 Netflix Automation Tool v3.0 - Premium Theme Engine 🚀

<p align="center">
  <img src="[https://img.shields.io/badge/Python-3.8+-red.svg?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3.8+-red.svg?style=for-the-badge&logo=python&logoColor=white)">
  <img src="[https://img.shields.io/badge/UI-Theme_Engine_v3-FF0000.svg?style=for-the-badge](https://img.shields.io/badge/UI-Theme_Engine_v3-FF0000.svg?style=for-the-badge)">
  <img src="[https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg?style=for-the-badge&logo=linux&logoColor=white](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg?style=for-the-badge&logo=linux&logoColor=white)">
  <img src="[https://img.shields.io/badge/Status-Active-2ECC71.svg?style=for-the-badge](https://img.shields.io/badge/Status-Active-2ECC71.svg?style=for-the-badge)">
</p>

---

**Netflix Automation Tool v3.0**, hesap yönetimi ve otomasyon süreçlerini terminal üzerinde en estetik ve hızlı şekilde gerçekleştirmek için tasarlanmış profesyonel bir araçtır. Gelişmiş **Glow Theme Engine** altyapısı sayesinde terminal deneyimini görsel bir şölene dönüştürürken, çoklu iş parçacığı desteğiyle maksimum performans sağlar.

---

## ✨ Özellikler (Features)

* 🎨 **Gelişmiş Tema Motoru (Theme Engine v3.0):** 20'den fazla özel tasarım neon tema.
* 🌟 **Glow Effects:** Terminal üzerinde parlama ve vurgu efektleri.
* ⚡ **Yüksek Performans (Multi-threading):** 1'den 100'e kadar ayarlanabilir thread desteği.
* 🔍 **Otomatik Veri Algılama:** `cookies/` klasöründeki verileri otomatik tarama.
* 📊 **Detaylı Loglama:** Tarih ve saat damgalı renkli kayıt sistemi.

---

## 🎨 Arayüz Önizlemesi

```ansi
╔══════════════════════════════════════════════════════════════╗
║  🎬 Netflix Automation Tool v3.0                            ║
║  Theme Engine: 20+ Custom Glow Themes                      ║
╚══════════════════════════════════════════════════════════════╝

[1] 🚀 Start Checker (Multi-threaded)
[2] 🎨 Theme Engine (Glow Effects)
[3] ⚙️  Settings & Proxies
[4] ❌ Exit

```

---

## 🛠️ Kurulum ve Gereksinimler

Uygulamayı çalıştırmak için bilgisayarınızda **Python 3.8** veya üzeri yüklü olmalıdır.

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/r2xzzs/netflix-checker.git
cd netflix-checker

```

### 2. Kütüphaneleri Yükleyin

```bash
pip install requests pyyaml

```

### 3. Başlatın

```bash
python main.py

```

---
