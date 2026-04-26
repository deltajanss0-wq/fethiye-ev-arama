# 🏡 Fethiye Ev Arama Paneli

Fethiye'nin **Çiftlik, Kargı ve Çalış** bölgelerinde kira ilanlarını filtreleyen,
mobil uyumlu Streamlit uygulaması.

---

## 🚀 Canlı Uygulama

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

> Deploy ettikten sonra buraya Streamlit Cloud linkinizi yapıştırın.

---

## 📱 Özellikler

- **Bölge filtresi** — Çiftlik / Kargı / Çalış
- **Eşya durumu** — Eşyalı / Eşyasız
- **Kira aralığı** — Slider ile 15.000–30.000 ₺ arası
- **Oda sayısı** — 1+1, 2+1, 3+1, 4+1
- **Resim slider** — Her ilan için birden fazla fotoğraf
- **Favori sistemi** — ❤️ butonuyla ilan kaydetme
- **Sıralama** — Yeniye göre / fiyata göre
- **Sahibinden linki** — Filtreleri sahibinden.com'a aktararak açma
- **Mobil uyumlu** — Telefonda rahat kullanım

---

## 🛠️ Kurulum (Visual Studio Code)

### 1. Repoyu klonla
```bash
git clone https://github.com/KULLANICI_ADINIZ/fethiye-ev-arama.git
cd fethiye-ev-arama
```

### 2. Sanal ortam oluştur
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları yükle
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı çalıştır
```bash
streamlit run app.py
```

Tarayıcı otomatik açılır: `http://localhost:8501`

---

## 📂 Proje Yapısı

```
fethiye-ev-arama/
│
├── app.py                    # Ana Streamlit uygulaması
├── requirements.txt          # Python bağımlılıkları
├── .gitignore
├── README.md
│
├── assets/
│   └── style.css             # Mobil CSS stilleri
│
├── data/
│   ├── __init__.py
│   └── listings.py           # İlan verisi (örnek / API)
│
└── .streamlit/
    └── config.toml           # Streamlit tema ayarları
```

---

## ☁️ GitHub'a Yükleme

```bash
git init
git add .
git commit -m "ilk commit: fethiye ev arama paneli"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/fethiye-ev-arama.git
git push -u origin main
```

---

## 🌐 Streamlit Cloud'a Deploy

1. [share.streamlit.io](https://share.streamlit.io) adresine git
2. GitHub hesabınla giriş yap
3. **New app** → repoyu seç → `app.py` → **Deploy**
4. 2-3 dakika sonra uygulama canlıda!

Üretilen link: `https://KULLANICI.streamlit.app`

---

## 🔧 Gerçek Veri Entegrasyonu

`data/listings.py` dosyasındaki `get_listings()` fonksiyonunu
gerçek veri kaynağına bağlayabilirsiniz:

```python
import requests
from bs4 import BeautifulSoup

def get_listings():
    # Örnek: sahibinden.com arama sonuçlarını çek
    # Not: sahibinden.com scraping koşullarını kontrol edin
    url = "https://www.sahibinden.com/kiralik-daire/fethiye"
    # ... implementasyon
    pass
```

---

## 📄 Lisans

MIT © 2024
