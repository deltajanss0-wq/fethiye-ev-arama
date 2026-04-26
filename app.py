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
        Zeynep ve patron için en önemli 2-3 maddeyi (fiyat, konum avantajı, kiralama süresi vb.) çıkar.
        Başlık: {title}
        Açıklama: {snippet}
        """
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI analizi şu an yapılamıyor."

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

    /* İlan Kartı Tasarımı */
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
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
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
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">🏡 Fethiye Emlak Radarı</h1>', unsafe_allow_html=True)
st.caption("Fethiye, Çalış, Çiftlik ve Kargı bölgelerindeki en güncel web ilanları.")

# ── FİLTRE VE ARAMA ────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    target_region = st.selectbox("Bölge Seçiniz:", ["Çalış", "Çiftlik", "Kargı"], index=0)
with col2:
    st.write("") # Boşluk
    st.write("")
    search_btn = st.button("🔍 Ara", use_container_width=True)

# ── İLANLARI GETİR VE LİSTELE ──────────────────────────────────────────────────
if search_btn or 'results' in st.session_state:
    if search_btn:
        with st.spinner(f"{target_region} ilanları taranıyor..."):
            query = f'site:sahibinden.com "fethiye" "{target_region.lower()}" "kiralık"'
            try:
                st.session_state.results = DDGS().text(query, max_results=8)
            except Exception as e:
                st.error("Arama motoru şu an meşgul, lütfen 1 dakika bekleyip tekrar basın.")
                st.session_state.results = []

    if st.session_state.get('results'):
        st.write(f"📌 {len(st.session_state.results)} ilan bulundu.")
        
        for i, res in enumerate(st.session_state.results):
            # Kart Yapısı
            with st.container():
                # Temsili Resim (Web araması resim URL'si vermediği için şık bir placeholder kullanıyoruz)
                placeholder_img = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80"
                
                st.markdown(f"""
                <div class="listing-card">
                    <img src="{placeholder_img}" class="card-image">
                    <div class="card-content">
                        <div class="card-tag">Sahibinden.com | {target_region}</div>
                        <div class="card-title">{res['title']}</div>
                        <div class="card-desc">{res['body']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.link_button("🚀 İlana Git", res['href'], use_container_width=True)
                with c2:
                    if st.button("🤖 AI Analiz", key=f"ai_{i}", use_container_width=True):
                        with st.spinner("Delta AI inceliyor..."):
                            analiz = analyze_snippet_with_ai(res['title'], res['body'])
                            st.success(analiz)
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.warning("Şu an yeni ilan indekslenmemiş görünüyor. Daha sonra tekrar deneyin.")

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.divider()
st.info("💡 Not: İlanların resimleri arama sonuçlarında ham olarak bulunmadığı için örnek görseller kullanılmıştır. Detaylar için 'İlana Git' butonunu kullanın.")
