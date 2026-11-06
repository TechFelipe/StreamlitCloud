import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Afazeres Domésticos - PNAD",
    page_icon="📊",
    layout="wide"
)

st.title("🏠 Afazeres Domésticos e Economia do Cuidado")
st.markdown("""
### Startup de Análise de Dados

**Personas:**
- Maria (Bahia)
- Fátima (Pernambuco)
- Antônio (Amazonas)
- Luíza (Ceará)

Objetivo: analisar a distribuição das horas semanais dedicadas aos cuidados de pessoas e afazeres domésticos por sexo, raça e estado.
""")

# =====================================================
# UPLOAD
# =====================================================

st.sidebar.header("📂 Upload")

arquivo = st.sidebar.file_uploader(
    "Selecione o arquivo XLS",
    type=["xls", "xlsx"]
)

arquivo = r"Tabela 1.1.1.xls"

if arquivo is None:
    st.warning("Faça upload do arquivo Tabela 1.1.1.xls")
    st.stop()

# =====================================================
# LEITURA DOS DADOS
# =====================================================

bruto = pd.read_excel(
    arquivo,
    engine="xlrd",
    header=None
)

indicador_1 = bruto.iloc[8:41].copy()

indicador_1.columns = [
    "uf_regiao",
    "total",
    "total_branca",
    "total_preta_parda",
    "homem_branca",
    "homem_preta_parda",
    "mulher_branca",
    "mulher_preta_parda",
]

indicador_1 = indicador_1.reset_index(drop=True)

for col in indicador_1.columns[1:]:
    indicador_1[col] = pd.to_numeric(
        indicador_1[col],
        errors="coerce"
    )

# Ano manual (altere conforme necessário)
indicador_1["ano"] = 2022

# =====================================================
# FILTROS
# =====================================================

st.sidebar.header("Filtros")

estados = st.sidebar.multiselect(
    "Estado / Região",
    indicador_1["uf_regiao"].unique(),
    default=["Bahia", "Pernambuco", "Ceará", "Amazonas"]
)

grupos = {
    "Homens Brancos":"homem_branca",
    "Homens Pretos/Pardos":"homem_preta_parda",
    "Mulheres Brancas":"mulher_branca",
    "Mulheres Pretas/Pardas":"mulher_preta_parda"
}

grupo_escolhido = st.sidebar.selectbox(
    "Grupo",
    list(grupos.keys())
)

coluna = grupos[grupo_escolhido]

dados = indicador_1[
    indicador_1["uf_regiao"].isin(estados)
]

# =====================================================
# KPIs
# =====================================================

st.header("📈 Indicadores")

homens = dados[
    ["homem_branca","homem_preta_parda"]
].mean().mean()

mulheres = dados[
    ["mulher_branca","mulher_preta_parda"]
].mean().mean()

diferenca = mulheres - homens

c1, c2, c3 = st.columns(3)

c1.metric(
    "Média dos Homens",
    f"{homens:.1f} h"
)

c2.metric(
    "Média das Mulheres",
    f"{mulheres:.1f} h"
)

c3.metric(
    "Diferença",
    f"{diferenca:.1f} h"
)

# =====================================================
# GRAFICO DE BARRAS
# =====================================================

st.header("📊 Comparação por Sexo e Raça")

fig_bar = px.bar(
    dados,
    x="uf_regiao",
    y=[
        "homem_branca",
        "homem_preta_parda",
        "mulher_branca",
        "mulher_preta_parda"
    ],
    barmode="group",
    title="Horas Semanais por Estado"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# =====================================================
# BOXPLOT
# =====================================================

st.header("📦 Distribuição das Horas")

dados_long = dados.melt(
    id_vars=["uf_regiao"],
    value_vars=[
        "homem_branca",
        "homem_preta_parda",
        "mulher_branca",
        "mulher_preta_parda"
    ],
    var_name="grupo",
    value_name="horas"
)

fig_box = px.box(
    dados_long,
    x="grupo",
    y="horas",
    color="grupo",
    title="Distribuição das Horas Semanais"
)

st.plotly_chart(
    fig_box,
    use_container_width=True
)

# =====================================================
# RANKING
# =====================================================

st.header("🏆 Ranking")

ranking = dados.sort_values(
    coluna,
    ascending=False
)

fig_rank = px.bar(
    ranking,
    x=coluna,
    y="uf_regiao",
    orientation="h",
    color=coluna,
    title=f"Ranking - {grupo_escolhido}"
)

st.plotly_chart(
    fig_rank,
    use_container_width=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.header("💡 Insights Automáticos")

estado_maior = ranking.iloc[0]["uf_regiao"]
valor_maior = ranking.iloc[0][coluna]

estado_menor = ranking.iloc[-1]["uf_regiao"]
valor_menor = ranking.iloc[-1][coluna]

st.success(
    f"""
    🔹 Maior média: {estado_maior}
    ({valor_maior:.1f} horas)

    🔹 Menor média: {estado_menor}
    ({valor_menor:.1f} horas)
    """
)

st.info(
    f"""
    As mulheres dedicam em média
    {diferenca:.1f} horas a mais
    que os homens aos cuidados e afazeres domésticos.
    """
)

# =====================================================
# DADOS
# =====================================================

st.header("📋 Base de Dados")

st.dataframe(
    dados,
    use_container_width=True
)

csv = dados.to_csv(index=False)

st.download_button(
    "⬇️ Baixar CSV",
    csv,
    file_name="afazeres_domesticos.csv",
    mime="text/csv"
)

# =====================================================
# REPORTAGENS
# =====================================================

st.header("📰 Economia do Cuidado")

st.image(
    "https://images.unsplash.com/photo-1581578731548-c64695cc6952",
    use_container_width=True
)

st.markdown("""
### O que é Economia do Cuidado?

A economia do cuidado engloba todas as atividades de cuidado com pessoas e afazeres domésticos realizadas dentro dos lares.

Apesar de fundamentais para a sociedade, essas atividades são realizadas majoritariamente por mulheres e geralmente não são remuneradas.

### Carga Mental Feminina

Além das tarefas domésticas, muitas mulheres assumem o planejamento e organização das atividades da casa, fenômeno conhecido como carga mental feminina.

Esse fator amplia desigualdades de gênero e impacta oportunidades de trabalho e renda.
""")

# =====================================================
# CONCLUSÃO
# =====================================================

st.header("🎯 Conclusão")

st.markdown("""
Este dashboard permite:

✅ Comparar homens e mulheres

✅ Comparar grupos raciais

✅ Ranking dos estados

✅ Analisar discrepâncias

✅ Explorar os dados por filtros

✅ Fazer upload de novos arquivos

✅ Gerar insights para políticas públicas
""")