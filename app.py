import streamlit as st
from duckduckgo_search import DDGS

# ── Sayfa Ayarları ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fethiye Web Radar",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── CSS ve Header ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .search-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #E8650A;
        margin-bottom: 20px;
    }
    .search-title {
        color: #1a0dab;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .search-body {
        color: #4d5156;
        font-size: 14px;
        margin-bottom: 12px;
    }
    .topbar {
        background-color: #202124;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <h2 style="margin:0;">🌐 Delta Web Radar</h2>
    <span style="font-size:14px; color:#aaa;">Sahibinden İlanlarını Arama Motorundan Çeker</span>
</div>
""", unsafe_allow_html=True)

# ── Filtreler ──────────────────────────────────────────────────────────────────
st.write("**Hedef Bölgeyi Seçin:**")
bolge = st.radio("Bölge:", ["Çalış", "Çiftlik", "Kargı"], horizontal=True, label_visibility="collapsed")

st.info(f"🔍 Arama Motoru botları Sahibinden.com'daki en güncel **{bolge}** ilanları için taranacak.")

# ── Arama İşlemi ───────────────────────────────────────────────────────────────
if st.button(f"🚀 {bolge} İlanlarını Getir", use_container_width=True):
    with st.spinner("Web'in derinlikleri taranıyor..."):
        
        # Sihirli Dorking Sorgumuz: Sadece sahibinden.com içinde fethiye, kiralık ve bölge adını arar.
        query = f'site:sahibinden.com "fethiye" "{bolge.lower()}" "kiralık"'
        
        try:
            # Arama motorundan verileri çekiyoruz (Maksimum 10 sonuç)
            results = DDGS().text(query, max_results=10)
            
            if not results:
                st.warning(f"Arama motorlarında {bolge} için indekslenmiş yeni Sahibinden ilanı bulunamadı.")
            else:
                st.success(f"✅ {len(results)} adet ilan bağlantısı bulundu!")
                
                # Sonuçları ekrana bas
                for r in results:
                    st.markdown(f"""
                    <div class="search-card">
                        <div class="search-title">{r.get('title', 'Başlık Bulunamadı')}</div>
                        <div class="search-body">{r.get('body', 'Açıklama bulunamadı...')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.link_button("🔗 İlanı Sahibinden'de Aç ↗", r.get('href', '#'))
                    st.write("") # Boşluk
                    
        except Exception as e:
            st.error(f"Arama motoruna bağlanırken bir sorun oluştu: {str(e)}")
            st.warning("Çok fazla istek atılmış olabilir, 1-2 dakika sonra tekrar deneyin.")

        # İşlem bittiğinde, "Ben doğrudan Google'da görmek istiyorum" diyenler için garanti link:
        st.markdown("---")
        google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        st.markdown(f"Alternatif: Tüm bu sonuçları doğrudan Google arayüzünde görmek için [Buraya Tıklayın ↗]({google_url})")
