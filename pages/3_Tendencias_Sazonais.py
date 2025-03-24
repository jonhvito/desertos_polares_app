import streamlit as st
import matplotlib.pyplot as plt
from utils.processamento import carregar_dados, tendencia_estacional
import pandas as pd

st.header("📉 Tendência de Extensão do Gelo por Estação")

# Carregar dados e calcular tendência por estação
df = carregar_dados()
df_sazonal = tendencia_estacional(df)

# Cores para cada estação
cores = {
    "Verão": "#d95f02",
    "Outono": "#7570b3",
    "Inverno": "#1b9e77",
    "Primavera": "#e7298a"
}

# Gráfico geral com todas as estações
st.subheader("Variação da Extensão Média do Gelo ao Longo dos Anos (por Estação)")
fig, ax = plt.subplots(figsize=(13, 5))
for estacao in ["Verão", "Outono", "Inverno", "Primavera"]:
    dados = df_sazonal[df_sazonal["Estacao"] == estacao]
    lw = 2.5 if estacao == "Verão" else 1.5
    ax.plot(dados["Year"], dados["Extent"], label=estacao, color=cores[estacao], linewidth=lw)

# Anotação de destaque para o verão
ax.annotate("🔻 Derretimento mais intenso no verão",
            xy=(2015, df_sazonal[(df_sazonal["Year"] == 2015) & (df_sazonal["Estacao"] == "Verão")]["Extent"].values[0]),
            xytext=(2005, 10),
            arrowprops=dict(arrowstyle="->", color=cores["Verão"]),
            fontsize=9, color=cores["Verão"], weight="bold")

ax.set_xlabel("Ano")
ax.set_ylabel("Extensão média (milhões km²)")
ax.set_title("Tendência de Extensão do Gelo por Estação (1979–2024)")
ax.grid(True)
ax.legend(title="Estação")
st.pyplot(fig)

# Comparativo entre 1979 e 2024 por estação
st.markdown("#### 📊 Mudança média por estação (1979 → 2024)")
for estacao in ["Verão", "Outono", "Inverno", "Primavera"]:
    dados = df_sazonal[df_sazonal["Estacao"] == estacao]
    try:
        inicio = dados[dados["Year"] == 1979]["Extent"].values[0]
        fim = dados[dados["Year"] == 2024]["Extent"].values[0]
        delta = fim - inicio
        st.markdown(f"**{estacao}**: {delta:.2f} milhões km² {'📉' if delta < 0 else '📈'}")
    except IndexError:
        st.warning(f"⚠️ Dados ausentes para {estacao} em 1979 ou 2024.")

# Gráfico interativo por estação
st.markdown("#### 🔎 Explore uma estação específica")
estacao_sel = st.selectbox("Escolha uma estação:", ["Verão", "Outono", "Inverno", "Primavera"])
dados_filtrados = df_sazonal[df_sazonal["Estacao"] == estacao_sel]
st.line_chart(dados_filtrados.set_index("Year")["Extent"])

# Interpretação final
st.markdown("""
---

### 📘 Interpretação:

Este gráfico mostra como a extensão média do gelo na Antártica varia ao longo dos anos, dividida por estação do ano.

- A linha do **verão** mostra uma **queda mais acentuada**, indicando que o derretimento tem se intensificado.
- As estações de **transição (primavera e outono)** também apresentam declínio.
- O **inverno**, embora mais estável, também mostra sinais de retração gradual.

---

### 🌍 Relação com Desertificação Polar:

- A diminuição da cobertura de gelo reduz o efeito de albedo, aumentando a absorção de calor.
- Isso acelera o aquecimento da região, contribuindo diretamente para o **processo de desertificação dos desertos polares**.
- A perda de gelo nos verões é crítica: representa um desequilíbrio crescente na sazonalidade natural.

---

### ⚡ Conexão com dados energéticos (próxima aba):

- A próxima aba mostra como essas mudanças sazonais se relacionam com dados reais de:
  - **Radiação solar**
  - **Velocidade dos ventos**
  - **Temperatura, pressão e umidade**

📊 Explore a aba **Energia e Clima** para ver como o ambiente antártico pode estar se tornando mais vulnerável — e ao mesmo tempo mais estudado para energias limpas e monitoramento climático.
""")
