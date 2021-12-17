# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# link:  https://dados.gov.br/dataset/corridas-do-taxigov#
#
# Nono digito significado: https://www.gov.br/receitafederal/pt-br/assuntos/educacao-fiscal/educacao_fiscal/folhetos-orientativos/cadastros-dig.pdf

# %% [markdown]
# __Bibliotecas necessárias__

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# __Carrega os dados__

# %%
df = pd.read_csv("http://repositorio.dados.gov.br/seges/taxigov/taxigov-passageiros-solicitantes-mes.zip",
                 compression='zip')

# %%
df.info()

# %%
df.describe().transpose()

# %% [markdown]
# __Checa se há algum valor nulo no dataframe__

# %%
df.isna().sum()

# %%
df[df['km_total'].isna()]

# %% [markdown]
# Cria clounas **mes** e **ano** a partir da coluna **mes_ano**

# %%
df['ano'] = df['ano_mes'].apply(lambda x: int(str(x)[:-2]))
df['mes'] = df['ano_mes'].apply(lambda x: int(str(x)[-2:]))

# %%
df.drop('ano_mes',axis=1,inplace=True)

# %% [markdown]
# __Checa os registros no quais o nome do solicitante é diferente do nome do passageiro__
#

# %%
df[df['nome_solicitante']!=df['nome_passageiro']]

# %% [markdown]
# __Converte nomes em letras maísculas e limpa caracteres de espaço__

# %%
df['nome_solicitante'] = df['nome_solicitante'].apply(lambda x: x.upper().strip())

# %%
df['nome_passageiro'] = df['nome_passageiro'].apply(lambda x: x.upper().strip())

# %%
df[df['nome_solicitante']!=df['nome_passageiro']]


# %% [markdown]
# __CPFs ausentes__

# %%
df[df['cpf_solicitante'].apply(lambda x: len(x)<11)]

# %% [markdown]
# __Número de solicitantes distintos na base de dados__

# %%
df[df['cpf_solicitante'].apply(lambda x: len(x)>11)]['cpf_solicitante'].nunique()

# %% [markdown]
# __Valor total gasto em corridas (em Milhões de reais) em todo o período registrado__

# %%
df['valor_corridas'].sum()/1e6

# %% [markdown]
# __Quantidade total das corridas em todo o período registrado__

# %%
df['quantidade_corridas'].sum()

# %% [markdown]
# __Quantidade total de km (em milhões) em todo o período registrado__

# %%
df['km_total'].sum()/1e6

# %% [markdown]
# __Passageiro com maior valor de corridas registrada num dado mês__

# %%
df[(df['valor_corridas']==df['valor_corridas'].max())]

# %% [markdown]
# __Passageiro com maior quantidade de solicitações de corrida registrada num dado mês__

# %%
df[df['quantidade_corridas']==df['quantidade_corridas'].max()]

# %% [markdown]
# Todas as corridas solicitadas por esse passageiro ao longo dos meses

# %%
df[df['cpf_solicitante']=='***.313.061-**'].groupby(['ano','mes']).sum()['quantidade_corridas'].plot(kind='bar')
plt.ylabel('Qtd Corridas')
plt.xlabel('Ano, Mês')
plt.tight_layout()

# %% [markdown]
# __As 10 maiores quantidades de corridas solicitadas__

# %%
df['quantidade_corridas'].nlargest(10).values

# %%
frames=[]
for each in df['quantidade_corridas'].nlargest(10):
    frames.append(df[df['quantidade_corridas']==each])
    qt_corridas_10 = pd.concat(frames)
qt_corridas_10

# %% [markdown]
# __Os 10 maiores valores de corridas solicitadas__

# %%
df['valor_corridas'].nlargest(10).values

# %%
frames=[]
for each in df['valor_corridas'].nlargest(10):
    frames.append(df[df['valor_corridas']==each])
    qt_corridas_10 = pd.concat(frames)
qt_corridas_10

# %% [markdown]
# __Os maiores valores de corridas por ano e seus respectivos solicitantes__
# ____

# %%
df.groupby('ano')['valor_corridas'].max()

# %%
frames=[]
for each in df.groupby('ano')['valor_corridas'].max():
    frames.append(df[df['valor_corridas']==each])
    mv = pd.concat(frames)
# mv

# %%
df[df['cpf_solicitante']=='***.507.801-**'].groupby(['ano','mes']).sum()['valor_corridas'].plot(kind='bar')
plt.ylabel('Valor Corridas')
plt.xlabel('Ano, Mês')
plt.title('JOAO MARCUS OKUMURA')
plt.tight_layout()

# %%
df[df['cpf_solicitante']=='***.424.877-**'].groupby(['ano','mes']).sum()['valor_corridas'].plot(kind='bar')
plt.ylabel('Valor Corridas')
plt.xlabel('Ano, Mês')
plt.title('JOSINALDO DA SILVA')
plt.tight_layout()

# %%
df[df['cpf_solicitante']=='***.916.547-**'].groupby(['ano','mes']).sum()['valor_corridas'].plot(kind='bar')
plt.ylabel('Valor Corridas')
plt.xlabel('Ano, Mês')
plt.title('ANTONIO CARLOS VIEIRA DOS SANTOS')
plt.tight_layout()


# %% [markdown]
# ___
# __Total de km, valor e quantidade de corridas por ano e mes__

# %%
df_ano_mes = df.groupby(['ano','mes']).sum()
df_ano_mes 

# %%
plt.figure(figsize=(10,4))
df.groupby(['ano','mes']).sum()[['km_total']].plot()
plt.ylabel('Total Km')
plt.xlabel('Ano, Mês')
plt.tight_layout()

# %%
df.groupby(['ano','mes']).sum()[['valor_corridas']].plot()
plt.ylabel('Valor Corridas')
plt.xlabel('Ano, Mês')
plt.tight_layout()

# %%
df.groupby(['ano','mes']).sum()[['quantidade_corridas']].plot()
plt.ylabel('Qtd Corridas')
plt.xlabel('Ano, Mês')
plt.tight_layout()

# %%
df.groupby(['ano']).sum()[['valor_corridas']].plot(kind='bar')
plt.ylabel('Valor Corridas')
plt.xlabel('Ano')
plt.tight_layout()

# %%
df.groupby(['mes']).sum()[['valor_corridas']].plot(kind='bar')
plt.ylabel('Valor Corridas')
plt.xlabel('Mês')
plt.tight_layout()

# %%
plt.figure(figsize=(10,4))
df.groupby(['ano']).sum()[['quantidade_corridas']].plot(kind='bar')
plt.ylabel('Qtd Corridas')
plt.xlabel('Mês, Ano')
plt.tight_layout()

# %%
df.groupby(['mes']).sum()[['quantidade_corridas']].plot(kind='bar')
plt.ylabel('Qtd Corridas')
plt.xlabel('Mês')
plt.tight_layout()

# %%
df_ano_mes.reset_index(inplace=True)

# %%
plt.figure(figsize=(12,4))
sns.barplot(x='mes',y='valor_corridas',data=df_ano_mes,hue='ano',palette='Set2')

# %%
sns.lmplot(x='mes',y='valor_corridas',data=df_ano_mes,col='ano')

# %%
gasto_corridas = df.groupby(['ano','mes']).sum()['valor_corridas'].unstack()

# %%
plt.figure(figsize=(10,6))
sns.heatmap(gasto_corridas,cmap='coolwarm')
