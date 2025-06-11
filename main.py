import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Criar a pasta de saída
output_dir = "resultados"
os.makedirs(output_dir, exist_ok=True)

# Leitura dos arquivos
df_vendas = pd.read_csv("C:/Users/Lucas Soares/Documents/Tudo Vira Dados/Codigos/Vendas x Clima/Vendas_7dias.csv")
df_clima = pd.read_csv("C:/Users/Lucas Soares/Documents/Tudo Vira Dados/Codigos/Vendas x Clima/Clima_7dias.csv")

# Conversão de datas
df_vendas["data"] = pd.to_datetime(df_vendas["data"])
df_clima["data"] = pd.to_datetime(df_clima["data"])

# Mescla
df_merged = pd.merge(df_vendas, df_clima, on=["data", "cidade"])

# Faixas de temperatura
df_merged["faixa_temp"] = pd.cut(
    df_merged["temperatura_media"],
    bins=[0, 20, 25, 30, 40],
    labels=["Frio", "Agradável", "Quente", "Muito Quente"]
)

# Gráfico 1 – Média de Vendas por Faixa
media_por_faixa = df_merged.groupby("faixa_temp", observed=False)["vendas"].mean()
correlacao = df_merged[["temperatura_media", "vendas"]].corr().iloc[0, 1]

plt.figure(figsize=(8, 5))
media_por_faixa.plot(kind="bar", color="#007ACC")
plt.title(f"Média de Vendas por Faixa de Temperatura (Correlação: {correlacao:.2f})")
plt.ylabel("Vendas Médias")
plt.xlabel("Faixa de Temperatura")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(f"{output_dir}/grafico1_media_vendas_por_faixa.png")
plt.close()

# Gráfico 2 – Percentual por Produto
vendas_por_faixa = df_merged.groupby(["faixa_temp", "produto"], observed=False)["vendas"].sum().unstack().fillna(0)
vendas_percentuais = vendas_por_faixa.div(vendas_por_faixa.sum(axis=1), axis=0) * 100

vendas_percentuais.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="tab20")
plt.title("Distribuição Percentual de Vendas por Produto em Cada Faixa")
plt.ylabel("% de Vendas")
plt.xlabel("Faixa de Temperatura")
plt.xticks(rotation=0)
plt.legend(title="Produto", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{output_dir}/grafico2_percentual_vendas_por_faixa.png")
plt.close()

# Gráfico 3 – Boxplot Cidade x Produto
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_merged, x="cidade", y="vendas", hue="produto")
plt.title("Distribuição de Vendas por Cidade e Produto")
plt.xlabel("Cidade")
plt.ylabel("Vendas")
plt.tight_layout()
plt.savefig(f"{output_dir}/grafico3_boxplot_vendas_cidade_produto.png")
plt.close()

# Gráfico 4 – Vendas Totais por Produto em Cada Cidade
produtos_por_cidade = df_merged.groupby(["cidade", "produto"])["vendas"].sum().unstack().fillna(0)
produtos_por_cidade.plot(kind="bar", figsize=(10, 6), colormap="tab10")
plt.title("Vendas Totais por Produto em Cada Cidade")
plt.ylabel("Total de Vendas")
plt.xlabel("Cidade")
plt.xticks(rotation=0)
plt.legend(title="Produto", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{output_dir}/grafico4_vendas_produto_por_cidade.png")
plt.close()

# Gráfico 5 – Tendência Semanal por Produto
tendencia = df_merged.groupby(["data", "produto"])["vendas"].sum().unstack().fillna(0)
tendencia.plot(marker="o", figsize=(12, 6))
plt.title("Tendência de Vendas por Produto na Semana")
plt.xlabel("Data")
plt.ylabel("Vendas")
plt.xticks(rotation=45)
plt.legend(title="Produto", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{output_dir}/grafico5_tendencia_vendas_semana.png")
plt.close()
