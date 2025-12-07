import streamlit as st
import pandas as pd
import plotly.express as px

# ================================
# CONFIGURACIÓN INICIAL
# ================================
st.set_page_config(
    page_title="ZAGAZ · Panel Estratégico GNV",
    layout="wide"
)

# ================================
# ESTILO VISUAL PREMIUM
# ================================
st.markdown("""
<style>
body {
    background-color: #0b0d10;
}
.big-kpi {
    padding: 25px;
    background: #10202f;
    border-radius: 12px;
    text-align: left;
    border-left: 6px solid #16a34a;
    font-size: 32px;
    font-weight: bold;
    color: white;
}
.big-sub {
    font-size: 14px;
    font-weight: normal;
    color: #9bb8d1;
}
.insight-box {
    background: #1b2735;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #3b82f6;
    color: #e0e6ed;
    font-size: 16px;
}
.section-title {
    font-size: 26px;
    color: #16a34a;
    font-weight: bold;
    padding-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# CARGA DE DATOS
# ================================
@st.cache_data
def load_data():
    try:
        return pd.read_excel("DATASET VALORES.xlsx")
    except:
        return pd.read_csv("DATASET VALORES.csv")

df = load_data()

st.title("🚀 ZAGAZ · Dashboard Estratégico GNV")
st.markdown("## Decisiones basadas en datos — Segmentos, adopción, miedos y oportunidades")

# ================================
# FILTROS
# ================================
st.sidebar.header("🔍 Filtros del Panel")

zona_f = st.sidebar.multiselect("Zonas", df["Zona"].unique(), default=df["Zona"].unique())
perfil_f = st.sidebar.multiselect("Perfil de Adopción", df["Perfil_Adopción"].unique(), default=df["Perfil_Adopción"].unique())

df_fil = df[df["Zona"].isin(zona_f)]
df_fil = df_fil[df_fil["Perfil_Adopción"].isin(perfil_f)]

# ================================
# KPI CARDS
# ================================
st.markdown("<div class='section-title'>Indicadores Clave</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Consumo promedio
consumo = df_fil["Consumo_Diario_Lts"].mean()
col1.markdown(f"<div class='big-kpi'>{consumo:.1f} Lts<br><span class='big-sub'>Consumo Diario Promedio</span></div>", unsafe_allow_html=True)

# % Conoce GNV
conocen = df_fil["Conocimiento_GNV"].isin(["Medio", "Alto"]).mean() * 100
col2.markdown(f"<div class='big-kpi'>{conocen:.1f}%<br><span class='big-sub'>Conocimiento del GNV</span></div>", unsafe_allow_html=True)

# % dispuestos
dispuestos = (df_fil["Disposición_GNV"] == "Sí").mean() * 100
col3.markdown(f"<div class='big-kpi'>{dispuestos:.1f}%<br><span class='big-sub'>Disposición a Convertir</span></div>", unsafe_allow_html=True)

# Visionarios
vis = (df_fil["Perfil_Adopción"] == "Visionario").mean() * 100
col4.markdown(f"<div class='big-kpi'>{vis:.1f}%<br><span class='big-sub'>Visionarios Detectados</span></div>", unsafe_allow_html=True)

# ================================
# INSIGHTS AUTOMÁTICOS (INTELIGENCIA)
# ================================
st.markdown("<div class='section-title'>📌 Insights Estratégicos Automáticos</div>", unsafe_allow_html=True)

insights = []

# Insight 1: zona con mayor disposición
zona_disp = df_fil.groupby("Zona")["Disposición_GNV"].apply(lambda x: (x=="Sí").mean()*100)
if not zona_disp.empty:
    z_max = zona_disp.idxmax()
    pct = zona_disp.max()
    consumo_z = df_fil[df_fil["Zona"]==z_max]["Consumo_Diario_Lts"].mean()
    insights.append(f"La zona **{z_max}** presenta la mayor disposición ({pct:.1f}%), con un consumo promedio de **{consumo_z:.1f} Lts**. Es un segmento prioritario.")

# Insight 2: miedo dominante
miedo_dom = df_fil["Miedo_GNV"].mode()
if not miedo_dom.empty:
    insights.append(f"El miedo dominante es **{miedo_dom.iloc[0]}**. Conviene preparar mensajes educativos específicos para esta objeción.")

# Insight 3: tipo de unidad más rentable
unidad_rank = df_fil.groupby("Tipo de unidad")["Consumo_Diario_Lts"].mean().sort_values(ascending=False)
if not unidad_rank.empty:
    insights.append(f"El tipo de unidad con mayor consumo promedio es **{unidad_rank.index[0]}** ({unidad_rank.iloc[0]:.1f} Lts). Perfecto para campañas iniciales.")

# Insight 4: perfil prioritario
insights.append(f"Del total filtrado, **{vis:.1f}%** son visionarios. Recomendado enfocar la fase 1 solo en estos operadores.")

# Mostrar insights
for i in insights:
    st.markdown(f"<div class='insight-box'>{i}</div>", unsafe_allow_html=True)

# ================================
# GRÁFICAS PROFESIONALES
# ================================
st.markdown("<div class='section-title'>📊 Visualizaciones Clave</div>", unsafe_allow_html=True)

# DISTRIBUCIÓN DE PERFILES
fig_perfil = px.bar(
    df_fil["Perfil_Adopción"].value_counts().reset_index(),
    x="index", y="Perfil_Adopción",
    title="Distribución de Perfiles de Adopción",
    labels={"index": "Perfil", "Perfil_Adopción": "Cantidad"},
    color="index",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_perfil, use_container_width=True)

# MIEDOS GNV
fig_miedos = px.bar(
    df_fil["Miedo_GNV"].value_counts().reset_index(),
    x="index", y="Miedo_GNV",
    title="Miedos principales frente al GNV",
    labels={"index": "Miedo", "Miedo_GNV": "Cantidad"},
    color="index",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_miedos, use_container_width=True)

# ================================
# TABLA FINAL
# ================================
st.markdown("<div class='section-title'>📋 Tabla Filtrada</div>", unsafe_allow_html=True)
st.dataframe(df_fil)
