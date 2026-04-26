import streamlit as st
from duckduckgo_search import DDGS
import google.generativeai as genai

# ── YAPAY ZEKA AYARLARI ────────────────────────────────────────────────────────
GOOGLE_API_KEY = "AIzaSyDss_TBJ75iglS3oi43QBe-j1Hk1dNmqcs"
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_snippet_with_ai(title, snippet):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Aşağıdaki emlak ilanı başlığını ve kısa açıklamasını analiz et. 
        En önemli 2-3 maddeyi (fiyat, konum avantajı, kiralama süresi vb.) çıkar.
        Başlık: {title}
        Açıklama: {snippet}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI analizi şu an yapılamıyor."

# ── SAYFA AYARLARI VE TASARIM ──────────────────────────────────────────────────
st.set_page_config(page_title="Fethiye Emlak Radarı", page_icon="🏡", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #1877F2;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 10px;
    }
    .listing-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border: 1px solid #eee;
        transition: transform 0.2s;
    }
    .listing-card:hover {
        transform: translateY(-5px);
    }
    .card-image {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    .card-content {
        padding: 15px;
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        color: #1d1d1f;
        margin-bottom: 8px;
    }
    .card-desc {
        font-size: 14px;
        color: #636366;
        line-height: 1.4;
        margin-bottom: 15px;
    }
    .card-tag {
        background: #f0f2f5;
        color: #1877F2;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }
    .fallback-warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 14px;
        border-left: 5px solid #ffeeba;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">🏡 Fethiye Emlak Radarı</h1>', unsafe_allow_html=True)
st.caption("Fethiye, Çalış, Çiftlik ve Kargı bölgelerindeki en güncel ilanlar.")

# ── FİLTRE VE ARAMA ────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    target_region = st.selectbox("Bölge Seçiniz:", ["Çalış", "Çiftlik", "Kargı"], index=0)
with col2:
    st.write("") 
    st.write("")
    search_btn = st.button("🔍 Ara", use_container_width=True)

# ── YEDEK VERİ (FALLBACK) SİSTEMİ ──────────────────────────────────────────────
def get_fallback_data(region):
    # Arama motoru ban attığında panelin boş kalmaması için acil durum verileri
    data = {
        "Çalış": [
            {"title": "Çalış Plajına 100m, 2+1 Eşyalı Kiralık", "body": "Fethiye Çalış'ta denize yürüme mesafesinde, sıfır eşyalı, yıllık kiralık fırsat daire. Memur veya kurumsal çalışan tercihimizdir.", "href": "https://www.sahibinden.com/"},
            {"title": "Çalış Merkezde Müstakil Havuzlu 3+1 Villa", "body": "Sadece kış sezonu (Mayıs'a kadar) kiralıktır. Elektrik, su, internet fiyata dahildir. Evcil hayvan kabul edilmez.", "href": "https://www.sahibinden.com/"}
        ],
        "Çiftlik": [
            {"title": "Fethiye Çiftlik'te Geniş Bahçeli 2+1 Kiralık", "body": "Doğa ile iç içe, anayola yakın, ulaşım sorunu olmayan eşyasız kiralık daire. Geniş balkonlu ve otoparklıdır.", "href": "https://www.sahibinden.com/"}
        ],
        "Kargı": [
            {"title": "Kargı Köyü İçinde 1+1 Taş Ev", "body": "Kargı'da mandalina bahçeleri içinde, tamamen restore edilmiş şirin taş ev. Uzun dönem kiralıktır, masrafsızdır.", "href": "https://www.sahibinden.com/"}
        ]
    }
    return data.get(region, [])

# ── İLANLARI GETİR VE LİSTELE ──────────────────────────────────────────────────
if search_btn or 'results' in st.session_state:
    if search_btn:
        with st.spinner(f"{target_region} ilanları web'de taranıyor..."):
            query = f'fethiye {target_region.lower()} kiralık ev daire'
            try:
                # Önce canlı arama motorunu deneriz
                raw_results = DDGS().text(query, max_results=5)
                if not raw_results:
                    raise Exception("Sonuç boş döndü")
                st.session_state.results = raw_results
                st.session_state.is_fallback = False
            except Exception as e:
                # Ban yersek sistemi çökertmeyiz, yedek veriyi yükleriz
                st.session_state.results = get_fallback_data(target_region)
                st.session_state.is_fallback = True

    if st.session_state.get('results'):
        if st.session_state.get('is_fallback'):
            st.markdown("""
            <div class="fallback-warning">
                <b>⚠️ Arama Motoru Engeli:</b> Sistem şu an canlı veri çekemiyor. Panel arayüzünü ve AI özelliklerini test edebilmeniz için <b>Çevrimdışı Yedek İlanlar</b> gösteriliyor.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write(f"📌 **{len(st.session_state.results)} adet** canlı ilan bulundu.")
        
        for i, res in enumerate(st.session_state.results):
            with st.container():
                placeholder_img = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80"
                
                st.markdown(f"""
                <div class="listing-card">
                    <img src="{placeholder_img}" class="card-image">
                    <div class="card-content">
                        <div class="card-tag">📍 {target_region}</div>
                        <div class="card-title">{res.get('title', '')}</div>
                        <div class="card-desc">{res.get('body', '')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.link_button("🚀 İlana Git", res.get('href', '#'), use_container_width=True)
                with c2:
                    if st.button("🤖 AI Analizi İste", key=f"ai_{target_region}_{i}", use_container_width=True):
                        with st.spinner("Delta AI inceliyor..."):
                            analiz = analyze_snippet_with_ai(res.get('title', ''), res.get('body', ''))
                            st.success(analiz)
                st.markdown("<br>", unsafe_allow_html=True)
