import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from utils.processamento import carregar_dados, media_anual
import pandas as pd

st.header("📈 Extensão do Gelo ao Longo do Tempo")

# Carregar dados
df = carregar_dados()
df_ano = media_anual(df)

# Gráfico de linha da extensão diária com faixas sazonais e anotações
st.subheader("Extensão Diária do Gelo Marinho com Análise Sazonal (1979–2024)")
fig1, ax1 = plt.subplots(figsize=(13, 4))
ax1.plot(df["Date"], df["Extent"], color="navy", linewidth=0.5)

# Faixas sazonais com contraste otimizado
for year in df["Date"].dt.year.unique():
    ax1.axvspan(f"{year}-01-01", f"{year}-03-31", color='#d95f02', alpha=0.2,
                label="Verão" if year == df["Date"].dt.year.min() else "")
    ax1.axvspan(f"{year}-07-01", f"{year}-09-30", color='#2166ac', alpha=0.2,
                label="Inverno" if year == df["Date"].dt.year.min() else "")

# Anotações visuais com contraste
ano_ref = 2010
ax1.annotate("↓ Verão: derretimento (mínimo de gelo)",
             xy=(pd.to_datetime(f"{ano_ref}-02-15"), 4.5),
             xytext=(pd.to_datetime(f"{ano_ref}-01-01"), 6.5),
             arrowprops=dict(arrowstyle="->", color="#d95f02"),
             fontsize=9, color="#d95f02", weight="bold")

ax1.annotate("↑ Inverno: congelamento (máximo de gelo)",
             xy=(pd.to_datetime(f"{ano_ref}-08-15"), 15),
             xytext=(pd.to_datetime(f"{ano_ref}-06-01"), 13),
             arrowprops=dict(arrowstyle="->", color="#2166ac"),
             fontsize=9, color="#2166ac", weight="bold")

ax1.set_xlabel("Ano")
ax1.set_ylabel("Extensão (milhões km²)")
ax1.set_title("Extensão Diária do Gelo Marinho com Análise Sazonal (1979–2024)")
ax1.grid(True)
ax1.legend(loc="upper right")
st.pyplot(fig1)

st.markdown("""
🔍 **O que esse gráfico mostra:**  
Este gráfico exibe a extensão diária do gelo marinho na Antártica de 1979 a 2024.  
As **faixas azuis** indicam o **inverno (julho a setembro)** — período de **máximo congelamento**.  
As **faixas laranjas** indicam o **verão (janeiro a março)** — período de **derretimento máximo**.  
As setas no gráfico ajudam a identificar claramente os picos e vales sazonais.
""")

# Gráfico de média anual interativo
st.subheader("Média anual da extensão do gelo marinho")
fig2 = px.line(df_ano, x="Year", y="Extent", markers=True,
               labels={"Extent": "Extensão média (milhões km²)", "Year": "Ano"},
               title="Média Anual da Extensão do Gelo Marinho")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
📊 **O que esse gráfico mostra:**  
Este gráfico mostra a média anual da extensão do gelo em milhões de km².  
É possível observar uma **tendência de queda** ao longo das décadas, especialmente **após 2016**, o que reforça a tese de alterações climáticas nos desertos polares.
""")

# Bloco explicativo e interativo
st.markdown("---")
with st.expander("🧠 Ajuda para interpretar os gráficos"):
    st.markdown("""
### 📘 Como interpretar os gráficos:

#### 📈 Extensão Diária do Gelo Marinho

- Este gráfico usa os dados de **extensão do gelo marinho registrados diariamente**, de 1979 a 2024.
- A linha representa os valores **medidos a cada dia**. **Não é uma média**.
- O gráfico sobe e desce em forma de onda porque o gelo **aumenta no inverno** e **derrete no verão** todos os anos.
- As **faixas azuis (inverno)** destacam os períodos de **congelamento máximo** (geralmente julho a setembro).
- As **faixas laranjas (verão)** mostram os períodos de **mínimo de gelo** (janeiro a março).

🧠 Importante: O eixo X mostra os anos, mas os dados são **diários e contínuos**.  
Os marcadores de ano aparecem a cada 10 anos apenas para facilitar a leitura visual.

#### 📊 Extensão Média Anual

- Mostra a média da extensão de gelo em cada ano.
- Ajuda a identificar **tendências de longo prazo**.
- Após 2016, há uma queda mais visível — um possível reflexo do agravamento do aquecimento global.

---

🌍 A Antártica funciona como um espelho climático:  
menos gelo = mais absorção de calor = mais aquecimento = mais desertificação.
    """)
