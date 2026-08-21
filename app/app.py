import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Retail Radar | Customer Segmentation",
    page_icon="🎯",
    layout="wide"
)

# 2. Veri Yükleme ve Segmentasyon (Cache'li)
@st.cache_data
def load_data():
    df = pd.read_excel("data/raw/Online Retail.xlsx")
    
    # Veri Temizliği
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df = df.drop_duplicates()
    df = df[df["UnitPrice"] > 0]
    df = df[df["Quantity"] > 0]
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    df = df.dropna(subset=["CustomerID"])
    df["CustomerID"] = df["CustomerID"].astype(int)
    
    # RFM Tablosu
    max_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("CustomerID").agg(
        recency_days=("InvoiceDate", lambda x: (max_date - x.max()).days),
        total_orders=("InvoiceNo", "nunique"),
        total_spending=("Revenue", "sum"),
        unique_products=("StockCode", "nunique")
    ).reset_index()
    
    rfm["avg_order_value"] = rfm["total_spending"] / rfm["total_orders"]
    
    # K-Means Kümeleme (k=4)
    features_log = np.log1p(rfm[["recency_days", "total_orders", "total_spending"]])
    scaled_features = StandardScaler().fit_transform(features_log)
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    rfm["cluster_k4"] = kmeans.fit_predict(scaled_features)
    
    # Segment İsimlendirme
    segment_map = {
        2: "High Value",
        0: "Occasional",
        3: "Regular",
        1: "At Risk"
    }
    rfm["segment"] = rfm["cluster_k4"].map(segment_map)
    
    # Segment bilgisini ana df'e de bağlayalım
    df = df.merge(rfm[["CustomerID", "segment"]], on="CustomerID", how="left")
    
    return df, rfm

# Verileri yükle
df, rfm = load_data()

# -------------------------------------------------------------
# 3. Sol Kenar Çubuğu (Sidebar) - Filtreleme Paneli
# -------------------------------------------------------------
st.sidebar.header("🔍 Filtreleme Paneli")

# Ülke Filtresi
all_countries = sorted(df["Country"].unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Ülke Seçiniz:",
    options=all_countries,
    default=[] # Boş bırakıldığında 'Tüm Ülkeler' geçerli olsun
)

# Segment Filtresi
all_segments = ["High Value", "Regular", "Occasional", "At Risk"]
selected_segments = st.sidebar.multiselect(
    "Müşteri Segmenti Seçiniz:",
    options=all_segments,
    default=all_segments # Varsayılan olarak tüm segmentler seçili
)

# Filtreleri Uygula
filtered_df = df.copy()
if selected_countries:
    filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]

if selected_segments:
    filtered_df = filtered_df[filtered_df["segment"].isin(selected_segments)]

# Filtrelenmiş müşteri ID'lerine göre RFM tablosunu filtrele
filtered_rfm = rfm[rfm["CustomerID"].isin(filtered_df["CustomerID"].unique())]

# -------------------------------------------------------------
# 4. Ana Sayfa Başlık ve Açıklama
# -------------------------------------------------------------
st.title("🎯 Retail Radar: Customer Segmentation & Analytics")
st.markdown("""
Bu dashboard, **UCI Online Retail** veri seti üzerindeki işlem verilerini ve **RFM + K-Means** 
kümeleme modeliyle elde edilen müşteri segmentlerini interaktif olarak incelemek için hazırlanmıştır.
""")
st.divider()

# -------------------------------------------------------------
# 5. Temel KPI Kartları (Filtrelenmiş Veriye Göre)
# -------------------------------------------------------------
st.subheader("📌 Genel Performans Göstergeleri (KPIs)")

if filtered_df.empty:
    st.warning("⚠️ Seçilen filtrelere uygun veri bulunamadı. Lütfen filtreleri kontrol edin.")
else:
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = filtered_df["Revenue"].sum()
    total_customers = filtered_rfm["CustomerID"].nunique()
    total_orders = filtered_df["InvoiceNo"].nunique()
    avg_spending_per_cust = filtered_rfm["total_spending"].mean() if total_customers > 0 else 0

    with col1:
        st.metric("Toplam Gelir (Revenue)", f"£{total_revenue:,.0f}")
    with col2:
        st.metric("Toplam Müşteri", f"{total_customers:,}")
    with col3:
        st.metric("Toplam Sipariş", f"{total_orders:,}")
    with col4:
        st.metric("Müşteri Başına Ort. Harcama", f"£{avg_spending_per_cust:,.2f}")

    st.divider()

    # -------------------------------------------------------------
    # 6. Müşteri Segmentleri Dağılımı ve Analizi
    # -------------------------------------------------------------
    st.subheader("👥 Müşteri Segment Dağılımı (K-Means)")

    segment_colors = {
        "At Risk": "#E63946",
        "High Value": "#2A9D8F",
        "Regular": "#457B9D",
        "Occasional": "#E9C46A"
    }

    seg_col1, seg_col2 = st.columns([1, 1])

    with seg_col1:
        segment_counts = filtered_rfm["segment"].value_counts().reset_index()
        segment_counts.columns = ["Segment", "Müşteri Sayısı"]
        
        fig_pie = px.pie(
            segment_counts,
            names="Segment",
            values="Müşteri Sayısı",
            title="Segmentlerin Müşteri Tabanındaki Payı",
            hole=0.45,
            color="Segment",
            color_discrete_map=segment_colors
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with seg_col2:
        seg_summary = filtered_rfm.groupby("segment").agg(
            Müşteri_Sayısı=("CustomerID", "count"),
            Ort_Son_Ziyaret_Gün=("recency_days", "mean"),
            Ort_Sipariş_Sayısı=("total_orders", "mean"),
            Ort_Harcama=("total_spending", "mean")
        ).reset_index()
        
        seg_summary.columns = ["Segment", "Müşteri Sayısı", "Ort. Recency (Gün)", "Ort. Sipariş", "Ort. Harcama (£)"]
        seg_summary["Ort. Recency (Gün)"] = seg_summary["Ort. Recency (Gün)"].round(1)
        seg_summary["Ort. Sipariş"] = seg_summary["Ort. Sipariş"].round(1)
        seg_summary["Ort. Harcama (£)"] = seg_summary["Ort. Harcama (£)"].map("£{:,.0f}".format)
        
        st.write("📊 **Segment Karakteristikleri:**")
        st.dataframe(seg_summary, use_container_width=True, hide_index=True)
        
        st.info("""
        💡 **Temel İçgörü:** Müşteri tabanının **%37.9'u (1.642 müşteri) 'At Risk'** grubunda yer alıyor. 
        Bu müşteriler ortalama 179 gündür sipariş vermemiş olup geri kazanım (win-back) kampanyaları için birincil hedeftir.
        """)

    st.divider()

    # -------------------------------------------------------------
    # 7. Zaman İçinde Satış Trendi
    # -------------------------------------------------------------
    st.subheader("📈 Aylık Satış ve Gelir Trendi")

    filtered_df["YearMonth"] = pd.to_datetime(filtered_df["InvoiceDate"]).dt.to_period("M").astype(str)

    monthly_sales = filtered_df.groupby("YearMonth").agg(
        Revenue=("Revenue", "sum"),
        OrderCount=("InvoiceNo", "nunique")
    ).reset_index()

    fig_trend = px.line(
        monthly_sales,
        x="YearMonth",
        y="Revenue",
        title="Aylık Toplam Gelir (£)",
        markers=True,
        labels={"YearMonth": "Yıl - Ay", "Revenue": "Gelir (£)"}
    )
    fig_trend.update_traces(
        line_color="#457B9D",
        line_width=3,
        marker=dict(size=8, color="#1D3557")
    )
    fig_trend.update_layout(
        xaxis_title="Dönem",
        yaxis_title="Toplam Gelir (£)",
        hovermode="x unified"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.caption("ℹ️ *Not: Aralık 2011 verisi sadece ayın ilk 9 gününü kapsamaktadır.*")

    st.divider()

    # -------------------------------------------------------------
    # 8. Ürün Performansı Analizi
    # -------------------------------------------------------------
    st.subheader("🏆 Ürün Performansı: En Çok Gelir ve Adet Getirenler")

    prod_col1, prod_col2 = st.columns(2)

    top_revenue_products = filtered_df.groupby("Description")["Revenue"].sum().reset_index()
    top_revenue_products = top_revenue_products.sort_values(by="Revenue", ascending=True).tail(10)

    top_quantity_products = filtered_df.groupby("Description")["Quantity"].sum().reset_index()
    top_quantity_products = top_quantity_products.sort_values(by="Quantity", ascending=True).tail(10)

    with prod_col1:
        fig_top_rev = px.bar(
            top_revenue_products,
            x="Revenue",
            y="Description",
            orientation="h",
            title="Top 10 Ürün (Toplam Gelire Göre - £)",
            labels={"Revenue": "Toplam Gelir (£)", "Description": "Ürün"},
            color="Revenue",
            color_continuous_scale="Blues"
        )
        fig_top_rev.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_rev, use_container_width=True)

    with prod_col2:
        fig_top_qty = px.bar(
            top_quantity_products,
            x="Quantity",
            y="Description",
            orientation="h",
            title="Top 10 Ürün (Satış Adedine Göre)",
            labels={"Quantity": "Satılan Toplam Adet", "Description": "Ürün"},
            color="Quantity",
            color_continuous_scale="Teal"
        )
        fig_top_qty.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_qty, use_container_width=True)
