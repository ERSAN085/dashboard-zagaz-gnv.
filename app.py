import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ZAGAZ Dashboard GNV",
    page_icon="🚗",
    layout="wide"
)

# ================================
# ESTILOS PERSONALIZADOS (AZULES)
# ================================
st.markdown("""
<style>
body {
    background-color: #f4f7fb;
}
h1, h2, h3 {
    color: #0b3d91 !important;
}
.sidebar .sidebar-content {
    background-color: #e9f0fb !important;
}
.big-kpi {
    padding: 25px;
    background: #ffffff;
    border-radius: 12px;
    text-align: center;
    border-left: 6px solid #0b66c3;
    font-size: 28px;
    font-weight: bold;
    color: #0b3d91;
}
.small-text {
    font-size: 16px;
    color: #1d4e89;
}
</style>
""", unsafe_allow_html=True)

# ================================
# CARGA DE DATOS
# ================================
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("DATASET VALORES.xlsx")
    except:
        df = pd.read_csv("DATASET VALORES.csv")
    return df

df = load_data()

st.title("📊 Dashboard Estratégico — ZAGAZ GNV")

# ================================
# KPIs PRINCIPALES
# ================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='big-kpi'>{len(df)}<br><span class='small-text'>Registros Totales</span></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='big-kpi'>{df['Tipo de unidad'].mode()[0]}<br><span class='small-text'>Vehículo Predominante</span></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='big-kpi'>{df['Marca'].mode()[0]}<br><span class='small-text'>Marca Dominante</span></div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='big-kpi'>{df['Tipo_Combustible'].mode()[0]}<br><span class='small-text'>Combustible Actual</span></div>", unsafe_allow_html=True)

st.markdown("---")

# ================================
# FILTROS LATERALES
# ================================
st.sidebar.header("🔎 Filtros del Dashboard")

marca_filtro = st.sidebar.multiselect("Marca", df["Marca"].unique())
unidad_filtro = st.sidebar.multiselect("Tipo de unidad", df["Tipo de unidad"].unique())
zona_filtro = st.sidebar.multiselect("Zona", df["Zona"].unique())

df_filtrado = df.copy()
if marca_filtro:
    df_filtrado = df_filtrado[df_filtrado["Marca"].isin(marca_filtro)]
if unidad_filtro:
    df_filtrado = df_filtrado[df_filtrado["Tipo de unidad"].isin(unidad_filtro)]
if zona_filtro:
    df_filtrado = df_filtrado[df_filtrado["Zona"].isin(zona_filtro)]

st.subheader("📈 Visualizaciones Interactivas")

# ================================
# GRAFICO 1 — Distribución de vehículo
# ================================
fig1 = px.histogram(
    df_filtrado,
    x="Tipo de unidad",
    color="Tipo de unidad",
    title="Distribución por Tipo de Unidad",
    color_discrete_sequence=px.colors.sequential.Blues
)
st.plotly_chart(fig1, use_container_width=True)

# ================================
# GRAFICO 2 — Marcas más comunes
# ================================
fig2 = px.histogram(
    df_filtrado,
    x="Marca",
    color="Marca",
    title="Marcas Más Utilizadas",
    color_discrete_sequence=px.colors.sequential.Blues
)
st.plotly_chart(fig2, use_container_width=True)

# ================================
# GRAFICO 3 — Consumo diario
# ================================
fig3 = px.box(
    df_filtrado,
    y="Consumo_Diario_Lts",
    title="Rango de Consumo Diario de Combustible",
    color_discrete_sequence=["#0b66c3"]
)
st.plotly_chart(fig3, use_container_width=True)

# ================================
# DESCARGA DEL DATASET
# ================================
st.subheader("⬇️ Descargar Datos")

st.download_button(
    label="Descargar dataset en CSV",
    data=df_filtrado.to_csv(index=False),
    file_name="dataset_filtrado_zagaz.csv",
    mime="text/csv"
)

st.success("Dashboard listo y corriendo en Streamlit Cloud cuando lo publiques.")
