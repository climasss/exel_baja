import streamlit as st
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Setando a pagina
st.set_page_config(page_title="Gerenciador de Gráficos", layout="wide")
st.title("Exel Baja 3.0")

# Lendo os dados do LoRa
dados = st.file_uploader("Escolha um arquivo CSV", type=['csv', 'txt'])
d = 0

if dados is not None:
    # Se for um CSV, lê com pandas
    try:
        df = pd.read_csv(dados, sep=';')
        st.write("Upload bem-sucedido!")
        d = 1
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

if d == 1:
# Criar a SIDEBAR
    st.sidebar.title("Configurações do Gráfico")
    tipo = st.sidebar.selectbox("Tipo de Gráfico", ["Linha", "Barra", "Mapa de Calor"])
    x = st.sidebar.selectbox("Eixo X", df.columns)  
    y = st.sidebar.selectbox("Eixo Y", ["🌡️Temperatura motor", "🌡️Temperatura CVT", "🛰️Odometro", "🚨Vibracao", "🛰️Sinal LoRa"])

    data = []

# Criar o gráfico com base nas seleções
    if tipo == "Linha":
        data = [go.Scatter(x=df[x], y=df[y], mode='lines')]
    elif tipo == "Barra":
        data = [go.Bar(x=df[x], y=df[y])]
    elif tipo == "Mapa de Calor":
        data = [go.Heatmap(x=df[x], y=df[y], z=df[y], colorscale='Viridis')]

    layout = go.Layout(title=f"{y} vs {x}", xaxis_title=x, yaxis_title=y)
    fig = go.Figure(data=data, layout=layout)

    if st.button("Gerar Gráfico"):
        pyo.plot(fig, filename='gráfico selecionado.html')
    else:
        st.write("Selecione as opções e clique em 'Gerar Gráfico' para visualizar.")    