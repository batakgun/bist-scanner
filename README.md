# BIST 100 Scanner 🚀

Gerçek zamanlı BIST 100 teknik analiz tarayıcısı. RSI, MACD, Bollinger Bands, EMA Crossover, ADX ve hacim analizi.

---

## Deploy Rehberi

### 1. Railway (Backend)

1. [railway.app](https://railway.app) → "New Project" → "Deploy from GitHub Repo"
2. Bu repoyu seç
3. Deploy tamamlandıktan sonra:
   - Sol menüden projeye tıkla
   - "Settings" → "Networking" → **"Generate Domain"** butonuna bas
   - Sana şöyle bir URL verecek: `https://bist-scanner-xxxx.up.railway.app`
4. Bu URL'i kopyala

### 2. HTML Dosyasını Güncelle

`bist_scanner.html` dosyasını aç, şu satırı bul:

```javascript
const API_URL = 'http://localhost:5000';
```

Railway URL'inle değiştir:

```javascript
const API_URL = 'https://bist-scanner-xxxx.up.railway.app';
```

Kaydet ve GitHub'a push et.

### 3. GitHub Pages (Frontend)

1. GitHub'da repo sayfasına git
2. "Settings" → sol menüde "Pages"
3. "Source" → "Deploy from a branch"
4. Branch: `main`, klasör: `/ (root)` → "Save"
5. Birkaç dakika sonra: `https://KULLANICIADIN.github.io/bist-scanner`

---

## Kullanım

- Dashboard açıldığında demo veri gösterir
- **TARA** butonuna bas → Railway'deki backend Yahoo Finance'dan canlı veri çeker
- İlk tarama ~5-8 dakika sürer (100 hisse analiz ediliyor)
- Railway ücretsiz planda sunucu uyku moduna girebilir, ilk istekte 30-60 sn bekleyebilirsin

---

## Dosya Yapısı

```
bist-scanner/
├── scanner.py          # Flask backend
├── bist_scanner.html   # Dashboard
├── requirements.txt    # Python bağımlılıkları
├── Procfile            # Railway başlatma komutu
└── README.md
```

## Notlar

- Ücretsiz Railway planında aylık 500 saat kullanım hakkı var
- Tarama sonuçları cache'lenmez, her TARA butonunda yeniden çekilir
- BIST 100 listesi Şubat 2025 itibarıyla günceldir
