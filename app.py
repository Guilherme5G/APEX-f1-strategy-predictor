import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# Configuração e tema do Dashboard
st.set_page_config(page_title="F1 Strategy Command Center", page_icon="🏎️", layout="wide")

# Estilização CSS customizada
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #ff2800; }
    </style>
""", unsafe_allow_html=True)

# 1. PAINEL LATERAL (Filtros e Entradas)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=130)
st.sidebar.title("Telemetria & Simulação")
st.sidebar.markdown("---")

piloto = st.sidebar.selectbox("Piloto Base", ["Max Verstappen (VER)", "Lewis Hamilton (HAM) - Em breve", "Charles Leclerc (LEC) - Em breve"])
circuito = st.sidebar.selectbox("Circuito", ["GP de São Paulo (Interlagos)", "GP de Zandvoort - Em breve"])
composto = st.sidebar.selectbox("Composto Atual", ["Intermediate", "Soft - Em breve", "Medium - Em breve", "Hard - Em breve"])

st.sidebar.markdown("---")
total_voltas = st.sidebar.slider("Janela de Voltas Simuladas", min_value=10, max_value=50, value=30)

# CABEÇALHO PRINCIPAL
st.title("🏎️ F1 Pit Stop Strategy Command Center")
st.caption("Sistema de Suporte à Decisão Estratégica baseado em Machine Learning (AdaBoost)")
st.markdown("---")

# CARREGAMENTO DO MODELO
@st.cache_resource
def carregar_modelo():
    return joblib.load('modelo_adaboost.pkl')

try:
    modelo = carregar_modelo()

    # Prepara dados para predição
    colunas_X = ['LapNumber', 'Stint', 'TyreLife', 'Compound_INTERMEDIATE']
    dados_simulados = {
        'LapNumber': list(range(1, total_voltas + 1)),
        'Stint': [1.0] * total_voltas,
        'TyreLife': list(range(1, total_voltas + 1)),
        'Compound_INTERMEDIATE': [1] * total_voltas
    }

    df_simulacao = pd.DataFrame(dados_simulados)[colunas_X]
    df_simulacao['Tempo_Previsto'] = modelo.predict(df_simulacao)

    # Cálculo da Regra de Negócio (Cliff)
    df_simulacao['Delta_Tempo'] = df_simulacao['Tempo_Previsto'].diff().fillna(0)
    linha_cliff = df_simulacao.loc[df_simulacao['Delta_Tempo'].idxmax()]
    volta_cliff = int(linha_cliff['LapNumber'])
    perda_tempo = linha_cliff['Delta_Tempo']

    # 2. MÉTRICAS PRINCIPAIS (Cards no Topo)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Margem de Erro (MAE)", "0.477s", help="Erro médio absoluto do modelo AdaBoost nos testes")
    c2.metric("Ponto do Cliff", f"Volta {volta_cliff}", help="Momento exato da queda de aderência")
    c3.metric("Perda Estimada", f"+{perda_tempo:.3f}s", help="Aumento no tempo de volta após o Cliff")
    c4.metric("Janela Ideal de Pit Stop", f"Voltas {volta_cliff - 1} a {volta_cliff}")

    st.markdown("---")

    # 3. ÁREA CENTRAL (Gráficos Interativos e Alertas)
    col_grafico, col_relatorio = st.columns([2, 1])

    with col_grafico:
        st.subheader("📊 Degradação do Pneu vs Tempo de Volta")
        
        # Gráfico Interativo Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_simulacao['LapNumber'], 
            y=df_simulacao['Tempo_Previsto'],
            mode='lines+markers',
            name='Tempo de Volta (s)',
            line=dict(color='#ff2800', width=3),
            marker=dict(size=8, color='#ffffff')
        ))
        
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Volta / Idade do Pneu",
            yaxis_title="Tempo Previsto (segundos)",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_relatorio:
        st.subheader("🚨 Relatório de Estratégia")
        
        st.error(f"""
        **ALERTA DE BOX DETECTADO**
        
        * **Carro:** {piloto.split()[0]}
        * **Circuito:** {circuito.split()[0]}
        * **Pneu:** {composto}
        
        ---
        **DIAGNÓSTICO:**  
        O modelo identificou uma perda brusca de ritmo de **+{perda_tempo:.3f}s** na **Volta {volta_cliff}**.
        
        **RECOMENDAÇÃO:**  
        Efetuar a troca de pneus na **Volta {volta_cliff - 1}** para evitar desgaste excessivo e manter o ritmo de pista limpa.
        """)

except Exception as e:
    st.error(f"Erro ao carregar o modelo. Certifique-se de que o arquivo 'modelo_adaboost.pkl' está na raiz do projeto. Detalhes: {e}")