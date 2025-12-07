import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# CONFIGURACIÓN GENERAL
# =========================================
st.set_page_config(
    page_title="ZAGAZ · Dashboard Estratégico GNV",
    page_icon="🚀",
    layout="wide"
)

# =========================================
# ESTILOS PERSONALIZADOS ZAGAZ
# =========================================
st.markdown("""
<style>

/* Fondo general */
body {
    background-color: #f3f6f4;
}

/* Contenedor principal */
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 2rem;
}

/* Encabezado premium */
.zg-header-bar {
    background: linear-gradient(90deg, #15803d, #0f766e);
    padding: 1.4rem 1.8rem;
    border-radius: 0 0 18px 18px;
    color: #ffffff;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.22);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.zg-title {
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 0.15rem;
}

.zg-subtitle {
    font-size: 0.9rem;
    opacity: 0.9;
}

.zg-badge {
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    background: rgba(15,23,42,0.25);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Tarjetas KPI */
.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.0rem 1.1rem;
    box-shadow: 0 4px 16px rgba(15,23,42,0.10);
    border-left: 6px solid #16a34a;
}

.kpi-label {
    font-size: 0.80rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    margin-bottom: 0.35rem;
}

.kpi-value {
    font-size: 1.7rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.10rem;
}

.kpi-extra {
    font-size: 0.80rem;
    color: #0f766e;
}

/* Título de sección */
.section-title {
    font-size: 1.1rem;
    font-weight: 800;
    margin-top: 1.5rem;
    margin-bottom: 0.4rem;
    color: #0f172a;
}

/* Caja de insights */
.insight-box {
    background: #0f172a;
    color: #e2f3ed;
    border-radius: 14px;
    padding: 0.9rem 1.0rem;
    margin-bottom: 0.45rem;
    border-left: 5px solid #22c55e;
    font-size: 0.95rem;
}

/* Etiqueta de filtros */
.filtros-chip {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
    margin-bottom: 0.1rem;
}

</style>
""", unsafe_allow_html=True)



# =========================================
# UTILIDADES
# =========================================
def fmt_or_dash(value, fmt="{:,.1f}"):
    """Formatea un número o devuelve '—' si no hay dato."""
    try:
        if value is None or pd.isna(value):
            return "—"
        return fmt.format(value)
    except Exception:
        return "—"

# =========================================
# CARGA DE DATOS
# =========================================
@st.cache_data
def load_data():
    df = pd.read_excel("DATASET VALORES.xlsx")
    return df

df = load_data()
df = df.copy()

# =========================================
# ENCABEZADO
# =========================================
st.markdown(
    """
    <div class='zg-header-bar'>
        <div>
            <div class='zg-title'>ZAGAZ · Dashboard Estratégico GNV</div>
            <div class='zg-subtitle'>
                Decisiones basadas en datos — segmentos, adopción, miedos y oportunidades
            </div>
        </div>
        <div class='zg-badge'>Versión piloto · Encuesta de campo</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================
# FILTROS SUPERIORES
# =========================================
st.markdown("<div class='filtros-chip'>Filtros del panel</div>", unsafe_allow_html=True)

f1, f2, f3, f4, f5 = st.columns(5)

with f1:
    zonas = st.multiselect(
        "Zona",
        options=sorted(df["Zona"].dropna().unique()) if "Zona" in df.columns else [],
        default=[]
    )
with f2:
    perfiles = st.multiselect(
        "Perfil de adopción",
        options=sorted(df["Perfil_Adopción"].dropna().unique()) if "Perfil_Adopción" in df.columns else [],
        default=[]
    )
with f3:
    tipos = st.multiselect(
        "Tipo de unidad",
        options=sorted(df["Tipo de unidad"].dropna().unique()) if "Tipo de unidad" in df.columns else [],
        default=[]
    )
with f4:
    combustibles = st.multiselect(
        "Combustible actual",
        options=sorted(df["Tipo_Combustible"].dropna().unique()) if "Tipo_Combustible" in df.columns else [],
        default=[]
    )
with f5:
    miedos = st.multiselect(
        "Miedo dominante",
        options=sorted(df["Miedo_GNV"].dropna().unique()) if "Miedo_GNV" in df.columns else [],
        default=[]
    )

df_fil = df.copy()
if zonas:
    df_fil = df_fil[df_fil["Zona"].isin(zonas)]
if perfiles:
    df_fil = df_fil[df_fil["Perfil_Adopción"].isin(perfiles)]
if tipos:
    df_fil = df_fil[df_fil["Tipo de unidad"].isin(tipos)]
if combustibles:
    df_fil = df_fil[df_fil["Tipo_Combustible"].isin(combustibles)]
if miedos:
    df_fil = df_fil[df_fil["Miedo_GNV"].isin(miedos)]

if df_fil.empty:
    st.warning("No hay registros que coincidan con los filtros seleccionados. Ajusta los filtros para ver información.")
    st.stop()

# =========================================
# KPIs PRINCIPALES — ENCUESTA
# =========================================
st.markdown("### Indicadores clave de la encuesta ZAGAZ")

k1, k2, k3, k4 = st.columns(4)

# Consumo promedio
try:
    consumo_prom = df_fil["Consumo_Diario_Lts"].mean()
except KeyError:
    consumo_prom = None

# Conocimiento GNV
try:
    conoc_pct = df_fil["Conocimiento_GNV"].isin(["Medio", "Alto"]).mean() * 100
except KeyError:
    conoc_pct = None

# Disposición GNV
try:
    disp_pct = (df_fil["Disposición_GNV"] == "Sí").mean() * 100
except KeyError:
    disp_pct = None

# Visionarios
try:
    vis_pct = (df_fil["Perfil_Adopción"] == "Visionario").mean() * 100
except KeyError:
    vis_pct = None

with k1:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Consumo diario promedio</div>
            <div class='kpi-value'>{fmt_or_dash(consumo_prom, "{:,.1f}")} Lts</div>
            <div class='kpi-extra'>Basado en operadores filtrados</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Conocimiento del GNV</div>
            <div class='kpi-value'>{fmt_or_dash(conoc_pct, "{:,.1f}")}%</div>
            <div class='kpi-extra'>Declaran conocimiento medio/alto</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Disposición a convertir</div>
            <div class='kpi-value'>{fmt_or_dash(disp_pct, "{:,.1f}")}%</div>
            <div class='kpi-extra'>Responderían "Sí" a convertir a GNV</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Visionarios detectados</div>
            <div class='kpi-value'>{fmt_or_dash(vis_pct, "{:,.1f}")}%</div>
            <div class='kpi-extra'>del total filtrado</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Segunda fila de KPIs
k5, k6, k7, k8 = st.columns(4)

# Volumen fase 1 (visionarios)
try:
    visionarios_df = df_fil[df_fil["Perfil_Adopción"] == "Visionario"]
    vol_fase1 = visionarios_df["Consumo_Diario_Lts"].sum()
except KeyError:
    vol_fase1 = None

# Edad promedio
try:
    edad_prom = df_fil["Edad"].mean()
except KeyError:
    edad_prom = None

# Unidades antiguas
try:
    antiguas_pct = (df_fil["Año_Vehículo"] <= 2015).mean() * 100
except KeyError:
    antiguas_pct = None

total_reg = len(df_fil)

with k5:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Volumen diario fase 1 (visionarios)</div>
            <div class='kpi-value'>{fmt_or_dash(vol_fase1, "{:,.0f}")} Lts</div>
            <div class='kpi-extra'>Si solo los visionarios cargaran GNV hoy</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k6:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Edad promedio del operador</div>
            <div class='kpi-value'>{fmt_or_dash(edad_prom, "{:,.1f}")} años</div>
            <div class='kpi-extra'>Perfil de edad del segmento actual</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k7:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Unidades 2015 o más antiguas</div>
            <div class='kpi-value'>{fmt_or_dash(antiguas_pct, "{:,.1f}")}%</div>
            <div class='kpi-extra'>Candidatas naturales a sustitución</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k8:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Registros en muestra filtrada</div>
            <div class='kpi-value'>{total_reg}</div>
            <div class='kpi-extra'>Entrevistas válidas</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================
# KPIs DE CONTEXTO (FIJOS DEL ESTUDIO)
# =========================================
st.markdown("### Contexto PV — Tamaño de mercado (no filtrable)")

c1, c2, c3, c4 = st.columns(4)

TOTAL_TAXIS = 1739      # taxis tradicionales en PV
TOTAL_RTN = 1331        # vehículos de plataforma (Uber / Didi)
TOTAL_BUSES = 333       # autobuses urbanos
TOTAL_BUSES_GNV = 244   # autobuses ya a GNV

with c1:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Taxis registrados en PV</div>
            <div class='kpi-value'>{TOTAL_TAXIS:,}</div>
            <div class='kpi-extra'>Alta prioridad para conversión</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Vehículos de plataforma</div>
            <div class='kpi-value'>{TOTAL_RTN:,}</div>
            <div class='kpi-extra'>Uber / Didi estimados en la zona</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Autobuses urbanos</div>
            <div class='kpi-value'>{TOTAL_BUSES:,}</div>
            <div class='kpi-extra'>Flota total UNIBUS PV</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Autobuses ya a GNV</div>
            <div class='kpi-value'>{TOTAL_BUSES_GNV:,}</div>
            <div class='kpi-extra'>Pioneros en modelo limpio</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================
# INSIGHTS ESTRATÉGICOS AUTOMÁTICOS
# =========================================
st.markdown("<div class='section-title'>📌 Insights estratégicos automáticos</div>", unsafe_allow_html=True)

insights = []

# Mejor zona por disposición
try:
    zona_disp = df_fil.groupby("Zona")["Disposición_GNV"].apply(lambda s: (s == "Sí").mean() * 100)
    if not zona_disp.empty:
        zmax = zona_disp.idxmax()
        pct = zona_disp.max()
        consumo_z = df_fil[df_fil["Zona"] == zmax]["Consumo_Diario_Lts"].mean()
        insights.append(
            f"La zona **{zmax}** muestra la mayor disposición a convertir (**{pct:,.1f}%**) "
            f"con un consumo promedio de **{consumo_z:,.1f} Lts**. Es un segmento prioritario para fase 1."
        )
except Exception:
    pass

# Miedo dominante
try:
    miedo_dom = df_fil["Miedo_GNV"].value_counts().idxmax()
    insights.append(
        f"El miedo dominante es **{miedo_dom}**. Conviene preparar mensajes educativos específicos "
        "para desmontar esta objeción."
    )
except Exception:
    pass

# Tipo de unidad más intensivo
try:
    consumo_tipo = df_fil.groupby("Tipo de unidad")["Consumo_Diario_Lts"].mean()
    if not consumo_tipo.empty:
        tmax = consumo_tipo.idxmax()
        cmax = consumo_tipo.max()
        insights.append(
            f"El tipo de unidad con mayor consumo promedio es **{tmax}** (**{cmax:,.1f} Lts/día**). "
            "Ideal para campañas iniciales y pilotos."
        )
except Exception:
    pass

# Visionarios vs total
if vis_pct is not None:
    insights.append(
        f"Del total filtrado, **{fmt_or_dash(vis_pct, '{:,.1f}')}%** son visionarios. "
        "Recomendado enfocar la fase 1 solo en estos operadores y su círculo de influencia."
    )

for txt in insights:
    st.markdown(f"<div class='insight-box'>{txt}</div>", unsafe_allow_html=True)

# =========================================
# VISUALIZACIONES
# =========================================
st.markdown("<div class='section-title'>📊 Visualizaciones clave</div>", unsafe_allow_html=True)

g1, g2 = st.columns(2)

# Gráfico 1: tipo de unidad vs combustible
with g1:
    try:
        fig_unidad = px.bar(
            df_fil,
            x="Tipo de unidad",
            color="Tipo_Combustible",
            title="Distribución por tipo de unidad y combustible",
            barmode="group"
        )
        fig_unidad.update_layout(height=380, margin=dict(l=40,r=20,t=60,b=40))
        st.plotly_chart(fig_unidad, use_container_width=True)
    except Exception:
        st.info("No se pudo generar la gráfica de tipo de unidad vs combustible (revisa nombres de columnas).")

# Gráfico 2: perfil de adopción
with g2:
    try:
        fig_perfil = px.pie(
            df_fil,
            names="Perfil_Adopción",
            hole=0.55,
            title="Perfil de adopción en la muestra filtrada"
        )
        fig_perfil.update_layout(height=380, margin=dict(l=40,r=20,t=60,b=40))
        st.plotly_chart(fig_perfil, use_container_width=True)
    except Exception:
        st.info("No se pudo generar la gráfica de perfil de adopción (revisa nombres de columnas).")

g3, g4 = st.columns(2)

# Gráfico 3: miedos
with g3:
    try:
        perfil_miedo = df_fil["Miedo_GNV"].value_counts().reset_index()
        perfil_miedo.columns = ["Miedo_GNV", "count"]
        fig_miedo = px.bar(
            perfil_miedo,
            x="Miedo_GNV",
            y="count",
            title="Principales miedos frente al GNV"
        )
        fig_miedo.update_layout(height=380, margin=dict(l=40,r=20,t=60,b=40))
        st.plotly_chart(fig_miedo, use_container_width=True)
    except Exception:
        st.info("No se pudo generar la gráfica de miedos (revisa nombres de columnas).")

# Gráfico 4: edad vs consumo
with g4:
    try:
        fig_edad = px.scatter(
            df_fil,
            x="Edad",
            y="Consumo_Diario_Lts",
            color="Perfil_Adopción",
            size="Consumo_Diario_Lts",
            title="Edad vs consumo diario (por perfil de adopción)",
            hover_data=["Tipo de unidad", "Tipo_Combustible"]
        )
        fig_edad.update_layout(height=380, margin=dict(l=40,r=20,t=60,b=40))
        st.plotly_chart(fig_edad, use_container_width=True)
    except Exception:
        st.info("No se pudo generar la gráfica de edad vs consumo (revisa nombres de columnas).")

# =========================================
# DESCARGA DE DATOS
# =========================================
st.markdown("<div class='section-title'>⬇️ Descargar datos filtrados</div>", unsafe_allow_html=True)

st.download_button(
    label="Descargar CSV filtrado",
    data=df_fil.to_csv(index=False),
    file_name="zagaz_gnv_filtrado.csv",
    mime="text/csv"
)
