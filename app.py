import streamlit as st
import pandas as pd

# ── Sayfa ayarları ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fethiye Ev Arama",
    page_icon="🏡",
    layout="centered",  # Resimlerin devasa çıkmaması için 'centered' yaptık 
    initial_sidebar_state="collapsed",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

# ── CSS ────────────────────────────────────────────────────────────────────────
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Uyarı: 'assets/style.css' dosyası bulunamadı. Tasarım standart görünebilir.")

# ── Veri ───────────────────────────────────────────────────────────────────────
from data.listings import get_listings

# ── Session state ──────────────────────────────────────────────────────────────
if "favorites" not in st.session_state:
    st.session_state.favorites = set()


# ══════════════════════════════════════════════════════════════════════════════
# RENDER CARD
# ══════════════════════════════════════════════════════════════════════════════
def render_card(row):
    is_fav = row["id"] in st.session_state.favorites
    fav_icon = "❤️" if is_fav else "🤍"
    esya_cls = "badge-esyali" if row["esya"] == "Eşyalı" else "badge-esyasiz"
    new_badge = "<span class='badge-new'>🆕 Yeni</span>" if row.get("yeni") else ""

    imgs = row["resimler"]
    img_key = f"img_idx_{row['id']}"
    if img_key not in st.session_state:
        st.session_state[img_key] = 0

    idx = st.session_state[img_key]
    current_img = imgs[idx % len(imgs)]

    img_col, nav_col = st.columns([6, 1])
    with img_col:
        st.image(current_img, use_container_width=True)
    with nav_col:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if len(imgs) > 1:
            if st.button("›", key=f"next_{row['id']}"):
                st.session_state[img_key] = (idx + 1) % len(imgs)
                st.rerun()
            if st.button("‹", key=f"prev_{row['id']}"):
                st.session_state[img_key] = (idx - 1) % len(imgs)
                st.rerun()
        st.caption(f"{idx+1}/{len(imgs)}")

    fiyat_fmt = f"{row['fiyat']:,.0f}".replace(",", ".")
    
    # KRİTİK DÜZELTME: HTML etiketlerinin yanlarda kod olarak görünmemesi için 
    # string içindeki girintileri (boşlukları) tamamen kaldırdık. 
    card_html = f"""
<div class="card-body">
<div class="card-top-row">
<div class="price">₺{fiyat_fmt}<span class='price-sub'>/ay</span></div>
{new_badge}
</div>
<div class="badges">
<span class="badge-bolge">{row['bolge']}</span>
<span class="{esya_cls}">{row['esya']}</span>
</div>
<div class="card-title">{row['baslik']}</div>
<div class="card-meta">
🛏 {row['oda']} &nbsp;|&nbsp; 📐 {row['m2']} m²
&nbsp;|&nbsp; 🏢 {row['kat']}. Kat
</div>
</div>"""
    
    st.markdown(card_html, unsafe_allow_html=True)

    btn1, btn2, btn3 = st.columns([3, 2, 2])
    with btn1:
        st.link_button("🔗 İlana Git ↗", row["url"], use_container_width=True)
    with btn2:
        if st.button(
            f"{fav_icon} Favori",
            key=f"fav_{row['id']}",
            use_container_width=True,
        ):
            if row["id"] in st.session_state.favorites:
                st.session_state.favorites.discard(row["id"])
            else:
                st.session_state.favorites.add(row["id"])
            st.rerun()
    with btn3:
        st.caption(f"📅 {row['tarih']}")

    st.markdown("<hr class='card-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <span class="live-dot"></span>
        <span class="topbar-title">🏡 Fethiye Ev Arama</span>
    </div>
    <div class="topbar-right">
        <span class="badge-site">Sahibinden.com</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NAVİGASYON
# ══════════════════════════════════════════════════════════════════════════════
try:
    from streamlit_option_menu import option_menu
    selected = option_menu(
        menu_title=None,
        options=["İlanlar", "Favoriler", "Filtrele"],
        icons=["house-fill", "heart-fill", "search"],
        orientation="horizontal",
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"font-size": "14px"},
            "nav-link": {
                "font-size": "13px",
                "font-family": "'Plus Jakarta Sans', sans-serif",
                "padding": "8px 4px",
            },
            "nav-link-selected": {
                "background-color": "#E8650A",
                "color": "white",
                "border-radius": "8px",
            },
        },
    )
except ImportError:
    selected = st.radio(
        "Sayfa",
        ["İlanlar", "Favoriler", "Filtrele"],
        horizontal=True,
        label_visibility="collapsed",
    )


# ══════════════════════════════════════════════════════════════════════════════
# SAYFA: İLANLAR & FİLTRELE
# ══════════════════════════════════════════════════════════════════════════════
if selected in ("İlanlar", "Filtrele"):

    with st.expander("🔧 Filtreler", expanded=(selected == "Filtrele")):
        c1, c2 = st.columns(2)
        with c1:
            bolge = st.selectbox(
                "Bölge",
                ["Tümü", "Çiftlik", "Kargı", "Çalış"],
                key="bolge",
            )
        with c2:
            esya = st.selectbox(
                "Eşya Durumu",
                ["Tümü", "Eşyalı", "Eşyasız"],
                key="esya",
            )

        kira_min, kira_max = st.slider(
            "Kira Aralığı (₺/ay)",
            min_value=5_000,
            max_value=50_000,
            value=(15_000, 30_000),
            step=500,
            format="₺%d",
            key="kira",
        )

        c3, c4 = st.columns(2)
        with c3:
            oda = st.multiselect(
                "Oda Sayısı",
                ["1+1", "2+1", "3+1", "4+1"],
                default=[],
                placeholder="Tümü",
                key="oda",
            )
        with c4:
            siralama = st.selectbox(
                "Sıralama",
                ["En Yeni", "Fiyat ↑", "Fiyat ↓"],
                key="siralama",
            )

        url_params = (
            f"price_min={kira_min}&price_max={kira_max}&sorting=date_desc"
            f"&category_id=1&searchFrom=header"
        )
        st.markdown(
            f'<a href="https://www.sahibinden.com/kiralik-daire/fethiye?{url_params}"'
            f' target="_blank" class="btn-sahibinden">'
            f"🔗 Sahibinden.com'da Filtreli Ara ↗</a>",
            unsafe_allow_html=True,
        )

    # ── Filtreleme ──────────────────────────────────────────────────────────
    df = get_listings()
    if bolge != "Tümü":
        df = df[df["bolge"] == bolge]
    if esya != "Tümü":
        df = df[df["esya"] == esya]
    if oda:
        df = df[df["oda"].isin(oda)]
    df = df[(df["fiyat"] >= kira_min) & (df["fiyat"] <= kira_max)]

    if siralama == "En Yeni":
        df = df.sort_values("id", ascending=False)
    elif siralama == "Fiyat ↑":
        df = df.sort_values("fiyat")
    else:
        df = df.sort_values("fiyat", ascending=False)

    # ── İstatistikler ───────────────────────────────────────────────────────
    toplam = len(df)
    esyali_n = len(df[df["esya"] == "Eşyalı"])
    esyasiz_n = len(df[df["esya"] == "Eşyasız"])
    ort_fiyat = int(df["fiyat"].mean()) if toplam > 0 else 0
    ort_fmt = f"₺{ort_fiyat:,.0f}".replace(",", ".")

    s1, s2, s3, s4 = st.columns(4)
    for col, val, lbl, icon in zip(
        [s1, s2, s3, s4],
        [toplam, esyali_n, esyasiz_n, ort_fmt],
        ["İlan", "Eşyalı", "Eşyasız", "Ort. Kira"],
        ["📋", "🛋️", "📦", "💰"],
    ):
        col.markdown(
            f"""<div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-num">{val}</div>
                <div class="stat-lbl">{lbl}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── İlanlar ─────────────────────────────────────────────────────────────
    if toplam == 0:
        st.markdown(
            "<div class='no-result'>😕 Kriterlere uygun ilan bulunamadı."
            "<br><small>Filtreleri genişletmeyi deneyin.</small></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='section-label'>📋 {toplam} ilan listelendi</div>",
            unsafe_allow_html=True,
        )
        for _, row in df.iterrows():
            render_card(row)


# ══════════════════════════════════════════════════════════════════════════════
# SAYFA: FAVORİLER
# ══════════════════════════════════════════════════════════════════════════════
elif selected == "Favoriler":
    df_all = get_listings()
    favs = df_all[df_all["id"].isin(st.session_state.favorites)]

    st.markdown(
        f"<div class='section-label'>❤️ {len(favs)} favori ilan</div>",
        unsafe_allow_html=True,
    )

    if favs.empty:
        st.markdown(
            "<div class='no-result'>Henüz favori eklemediniz."
            "<br><small>İlan kartlarındaki 🤍 butonuna tıklayın.</small></div>",
            unsafe_allow_html=True,
        )
    else:
        for _, row in favs.iterrows():
            render_card(row)
