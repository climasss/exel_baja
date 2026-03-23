import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import io

# Configuração da página
st.set_page_config(page_title="Gerenciador de Gráficos - Excel Baja", layout="wide")
st.title("🏎️ Excel Baja 3.0 - Analisador de Arquivos")

# --- UPLOAD DO ARQUIVO ---
dados = st.file_uploader("Escolha um arquivo CSV", type=['csv', 'txt'])

if dados is not None:
    try:
        # Lendo com o separador ponto e vírgula conforme sua planilha
        df = pd.read_csv(dados, sep=';')
        st.success("✅ Arquivo carregado com sucesso!")
        
        # --- SIDEBAR ---
        st.sidebar.title("Configurações do Gráfico")
        tipo = st.sidebar.selectbox("Tipo de Gráfico", ["Linha", "Barra", "Mapa de Calor"])
        
        # Eixo X geralmente é o tempo ou intervalo
        x = st.sidebar.selectbox("Eixo X (Referência)", df.columns)
        
        # Lista de sensores que queremos monitorar (exatamente como no seu CSV)
        opcoes_y = ["💨Velocidade", "🌡️Temperatura motor", "🌡️Temperatura CVT", "🛰️Odometro", "🚨Vibracao", "🛰️Sinal LoRa", "⏲RPM"]
        
        # Filtrar apenas o que realmente existe no arquivo subido
        colunas_validas = [c for c in opcoes_y if c in df.columns]
        
        if not colunas_validas:
            colunas_validas = df.columns.tolist() # Se não achar nada, libera todas as colunas
            
        y = st.sidebar.selectbox("Eixo Y (Sensor)", colunas_validas)

        # --- LÓGICA DO PLOTLY ---
        data = []
        if tipo == "Linha":
            data = [go.Scatter(x=df[x], y=df[y], mode='lines+markers', name=y)]
        elif tipo == "Barra":
            data = [go.Bar(x=df[x], y=df[y], name=y)]
        elif tipo == "Mapa de Calor":
            data = [go.Heatmap(x=df[x], y=df[y], z=df[y], colorscale='Viridis')]

        layout = go.Layout(
            title=f"Análise Detalhada: {y} vs {x}",
            xaxis_title=x,
            yaxis_title=y,
            hovermode="x unified",
            template="plotly_white"
        )
        
        fig = go.Figure(data=data, layout=layout)

        # --- EXIBIÇÃO NO SITE ---
        # No Streamlit Cloud, usamos st.plotly_chart para o gráfico aparecer na tela
        st.plotly_chart(fig, use_container_width=True)

        # --- EXPORTAR PARA HTML (O que o pyo.plot tentava fazer) ---
        st.divider()
        st.subheader("💾 Exportar Resultado")
        
        # Criando o buffer do arquivo HTML
        html_buffer = io.StringIO()
        fig.write_html(html_buffer, include_plotlyjs='cdn')
        html_bytes = html_buffer.getvalue().encode()

        st.download_button(
            label="📥 Baixar Gráfico Interativo (.html)",
            data=html_bytes,
            file_name=f"analise_{y}.html",
            mime='text/html',
            help="Baixe o gráfico para abrir no navegador mesmo sem internet."
        )

        # Exibir a tabela abaixo para conferência
        with st.expander("Ver dados brutos da planilha"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
        st.info("Certifique-se que o arquivo usa ';' como separador.")

else:
    st.info("Aguardando upload do arquivo CSV para iniciar a análise.")


