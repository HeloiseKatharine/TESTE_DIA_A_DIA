# -*- coding: utf-8 -*-
"""
Dashboard de Análise de Dados de uma empresa de atacarejo.
Feito por Heloise Katharine
"""

import pandas as pd
import chardet
import matplotlib.pyplot as plt
import streamlit as st
from insights import insights

st.title("Dashboard de análise de dados de uma empresa de atacarejo.")

def decodificacao_arquivo():
    # Usada para identificar a decodificação do arquivo customer_data.csv
    with open("customer_data.csv", "rb") as f:
        res = chardet.detect(f.read())
        print(res)

def carrega_dados():
    # Carrega os conjuntos de dados
    sales_data = pd.read_csv("sales_data.csv", sep=";", encoding="utf-8")
    customer_data = pd.read_csv("customer_data.csv", sep=";", encoding="ISO-8859-1")
    customer_sales_data = pd.read_csv("customer_sales_data.csv", sep=";", encoding="utf-8")
    
    return sales_data, customer_data, customer_sales_data

def AED(sales_data, customer_data, customer_sales_data):
    # Análise Exploratória dos Dados
    print("Informações gerais:")
    print(sales_data.info())
    print(customer_data.info())
    print(customer_sales_data.info())
       
    print("Colunas:")
    print(sales_data.columns)
    print(customer_data.columns)
    print(customer_sales_data.columns)
       
    print("Head:")
    print(sales_data.head())
    print(customer_data.head())
    print(customer_sales_data.head())

def valores_ausentes(sales_data, customer_data, customer_sales_data):
    # Verifica se possui valores ausentes
    print(f'sales_data = {sales_data.isnull().sum()}')
    print(f'\ncustomer_data = {customer_data.isnull().sum()}')
    print(f'\ncustomer_sales_data = {customer_sales_data.isnull().sum()}')

def resgistros_duplicados(sales_data, customer_data, customer_sales_data):
    # Verifica se possui registros duplicados
    print(f'sales_data = {sales_data.duplicated().sum()}')
    print(f'customer_data = {customer_data.duplicated().sum()}')
    print(f'customer_sales_data = {customer_sales_data.duplicated().sum()}')

def limpar_dados(sales_data, customer_data, customer_sales_data):
    # Limpeza dos dados (Tipos de dados e conversão)
        
    # print(f'sales_data =\n{sales_data.dtypes}')
    sales_data["Data"] = pd.to_datetime(sales_data["Data"])
    sales_data["Data"] = sales_data["Data"].dt.floor("s")
    print(f'\nsales_data =\n{sales_data.dtypes}')

    # print(f'\ncustomer_data =\n{customer_data.dtypes}')
    customer_data["Data_Cadastro"] = pd.to_datetime(customer_data["Data_Cadastro"])
    customer_data["Data_Cadastro"] = customer_data["Data_Cadastro"].dt.floor("s")
    customer_data["Cidade"] = customer_data["Cidade"].replace(r'^Vicente.*Pir[?£]s$', 'Vicente Pires', regex=True)
    print(f'\ncustomer_data =\n{customer_data.dtypes}')

    # print(f'\ncustomer_sales_data =\n{customer_sales_data.dtypes}')

    customer_sales_data["Data"] = pd.to_datetime(customer_sales_data["Data"])
    customer_sales_data["Data"] = customer_sales_data["Data"].dt.floor("s")
    customer_sales_data["Valor_Unitário"] = customer_sales_data["Valor_Unitário"].replace('27reais', '27', regex=True)
    customer_sales_data["Valor_Unitário"] = customer_sales_data["Valor_Unitário"].astype(float)
    print(f'\ncustomer_sales_data =\n{customer_sales_data.dtypes}')

    # pd.set_option('display.max_rows', None)
    # customer_sales_data
    
    return sales_data, customer_data, customer_sales_data

def describe_dados(sales_data, customer_data, customer_sales_data):
    sales_data.describe()
    customer_data.describe()
    customer_sales_data.describe()

@st.cache_data
def analise_vendas(sales_data):

    df = pd.DataFrame(sales_data)
    df['Valor_Total'] = df['Quantidade'] * df['Valor_Unitário']

    vendas_agrupadas = df.groupby('Produto').agg({'Quantidade': 'sum', 'Valor_Total': 'sum'}).reset_index()
    vendas_agrupadas = vendas_agrupadas.sort_values(by='Quantidade', ascending=False)

    st.write("""# Análise dos dados de vendas""")

    st.write("""## Produtos mais vendidos""")
    # tabela de vendas
    st.write(vendas_agrupadas)

    # Gráficos das vendas agrupadas
    plt.figure(figsize=(19, 9))

    # Gráfico de produtos mais vendidos (Quantidade)
    plt.subplot(1, 2, 1)
    plt.barh(vendas_agrupadas['Produto'], vendas_agrupadas['Quantidade'], color='skyblue')
    plt.title('Produtos mais vendidos (Quantidade).', fontsize=16)
    plt.xlabel('Quantidade vendida', fontsize=16)
    plt.ylabel('Produto', fontsize=16)
    plt.xticks(fontsize=14)        
    plt.yticks(fontsize=14)   
    
    # Gráfico de valor total dos produtos mais vendidos
    plt.subplot(1, 2, 2)
    plt.barh(vendas_agrupadas['Produto'], vendas_agrupadas['Valor_Total'], color='lightgreen')
    plt.title('Produtos mais vendidos (Valor).', fontsize=16)
    plt.xlabel('Valor total vendido (R$)', fontsize=16)
    plt.ylabel('Produto', fontsize=16)
    plt.xticks(fontsize=14)        
    plt.yticks(fontsize=14)
    
    st.pyplot(plt)
    plt.tight_layout()

    st.write("""## Vendas por canal de vendas""")

    # Calcula a quantidade de produtos mais vendidos mais vendidos por canais de vendas (Quantidade e valor total)
    canais_vendas_agrupadas = df.groupby('Canal_Venda').agg({'Quantidade': 'sum', 'Valor_Total': 'sum'}).reset_index()
    canais_vendas_agrupadas = canais_vendas_agrupadas.sort_values(by='Quantidade', ascending=False)

    # tabela canal de vendas
    st.write(canais_vendas_agrupadas)

    # Gráfico de produtos mais vendidos por cada canal de venda
    plt.figure(figsize=(19, 9))
    plt.subplot(1, 2, 1)
    plt.barh(canais_vendas_agrupadas['Canal_Venda'], canais_vendas_agrupadas['Quantidade'], color='skyblue')
    plt.title('Distribuição da quantidade de produtos vendidos por canal de vendas.', fontsize=16)
    plt.xlabel('Quantidade de produtos vendidos', fontsize=16)
    plt.ylabel('Canal de vendas', fontsize=16)
    plt.xticks(fontsize=14)        
    plt.yticks(fontsize=14)

    # Gráfico de valor total dos produtos mais vendidos (canal de vendas)
    plt.subplot(1, 2, 2)
    plt.barh(canais_vendas_agrupadas['Canal_Venda'], canais_vendas_agrupadas['Valor_Total'], color='lightgreen')
    plt.title('Distribuição do valor total de produtos vendidos por canal de vendas.', fontsize=16)
    plt.xlabel('Valor total de produtos vendidos (R$)', fontsize=16)
    plt.ylabel('Canal de vendas', fontsize=16)
    plt.xticks(fontsize=14)        
    plt.yticks(fontsize=14)

    plt.tight_layout()
    st.pyplot(plt)

    # Calcular a participação percentual de cada canal
    total_vendas = canais_vendas_agrupadas['Valor_Total'].sum()
    canais_vendas_agrupadas['Percentual'] = (canais_vendas_agrupadas['Valor_Total'] / total_vendas) * 100

    st.subheader("Gráfico de participação percentual de vendas por canal de venda.")
    plt.figure(figsize=(8, 8))
    plt.pie(canais_vendas_agrupadas['Percentual'], labels=canais_vendas_agrupadas['Canal_Venda'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    # plt.title('Participação percentual de vendas por canal de venda',fontsize=14)

    plt.axis('equal')
    # plt.show()
    st.pyplot(plt)

    st.write("""## Vendas ao longo do tempo (Sazonalidade)""")

    # Calcula a quantidade de produtos vendidos por dia (mostrando somente os 10 dias que mais vedem produtos)
    datas_agrupadas = df.groupby('Data').agg({'Quantidade': 'sum', 'Valor_Total': 'sum', 'Produto':  lambda x: ', '.join(x.unique())}).reset_index()
    datas_agrupadas = datas_agrupadas.sort_values(by='Quantidade', ascending=False)

    # Seleciona apenas as 10 primeiras
    top_10_datas = datas_agrupadas.head(10)
    top_10_datas['Data'] = pd.to_datetime(top_10_datas['Data']).dt.strftime('%d/%m/%Y')
  
    st.write("""#### Top 10 datas com maior quantidade de produtos vendidos.""")
    
    top_10_datas

    fig, ax = plt.subplots(figsize=(10, 6))

    # Gráfico de produtos mais vendidos (Quantidade)
    ax.barh(top_10_datas['Data'], top_10_datas['Quantidade'], color='skyblue')
    ax.set_title('Top 10 datas com maior quantidade de produtos vendidos', fontsize=16)
    ax.set_xlabel('Quantidade Vendida', fontsize=16)
    ax.set_ylabel('Datas', fontsize=16)

    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)
    
    df['Data'] = pd.to_datetime(datas_agrupadas['Data']).dt.strftime('%m/%Y')
    datas_agrupadas = df.groupby('Data').agg({'Quantidade': 'sum', 'Valor_Total': 'sum', }).reset_index()

    datas_agrupadas = datas_agrupadas.sort_values(by='Data', ascending=False)
    
    # datas_agrupadas

    datas_agrupadas['Data'] = pd.to_datetime(datas_agrupadas['Data']).dt.strftime('%m/%Y')

    st.write("""## Gráficos sobre vendas ao longo do tempo""")
    plt.figure(figsize=(19, 7))

    plt.subplot(1, 2, 1)
    plt.plot(datas_agrupadas['Data'], datas_agrupadas['Valor_Total'], color='skyblue')
    plt.title('Valor total de vendas ao longo do tempo.', fontsize=16)
    plt.xlabel('Data', fontsize=16)
    plt.ylabel('Valor total', fontsize=16)
    # plt.xticks(fontsize=14)        
    # plt.yticks(fontsize=14)

    plt.subplot(1, 2, 2)
    plt.plot(datas_agrupadas['Data'], datas_agrupadas['Quantidade'], color='skyblue')
    plt.title('Quantidade total de vendas ao longo do tempo.', fontsize=16)
    plt.xlabel('Data', fontsize=16)
    plt.ylabel('Quantidade', fontsize=16)
    # plt.xticks(fontsize=14)        
    # plt.yticks(fontsize=14)

    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)

@st.cache_data
def analise_clientes_vendas(customer_data, customer_sales_data):
 
    df_customer_data = pd.DataFrame(customer_data)
    df_customer_sales_data = pd.DataFrame(customer_sales_data)

    df_customer_merged = pd.merge(customer_data, customer_sales_data, on='ID_Cliente')
    df_customer_merged['Valor_Total'] = df_customer_merged['Quantidade'] * df_customer_merged['Valor_Unitário']

    # df_customer_merged

    cidades_agrupadas = df_customer_merged.groupby('Cidade').agg({'ID_Cliente':  'nunique', 'Valor_Total': 'sum'}).reset_index()
    cidades_agrupadas = cidades_agrupadas.sort_values(by='Cidade', ascending=False)
      
    """
    # Análise dos dados de vendas por cliente
    ## Análise Geográfica
    """
    
    cidades_agrupadas
   
    left_column, right_column = st.columns(2)
    fig, ax = plt.subplots(figsize=(10, 6))

    # Gráfico de cidades com a maior receita
    ax.bar(cidades_agrupadas['Cidade'], cidades_agrupadas['Valor_Total'], color='coral')
    ax.set_title('Valor total de produtos por cidade.', fontsize=16)
    ax.set_xlabel('Cidades', fontsize=16)
    ax.set_ylabel('Valor total de produtos', fontsize=16)

    plt.tight_layout()
    left_column.pyplot(plt)

    # Gráfico contendo a quantidade de clientes por cidade
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(cidades_agrupadas['Cidade'], cidades_agrupadas['ID_Cliente'], color='lightcoral')
    ax.set_title('Valor total de clientes por cidade.', fontsize=16)
    ax.set_xlabel('Cidades', fontsize=16)
    ax.set_ylabel('Valor total de clientes', fontsize=16)

    plt.tight_layout()
    right_column.pyplot(plt)

    """## Análise de Clientes"""

    clientes_agrupados = df_customer_merged.groupby('ID_Cliente').agg({'Valor_Total': 'sum', 'Data': 'nunique'}).reset_index()
    clientes_agrupados = clientes_agrupados.sort_values(by='Data', ascending=False)
    
    clientes_agrupados
    
    top_10_clientes_valor_total = clientes_agrupados.head(10)
    
    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(top_10_clientes_valor_total['ID_Cliente'], top_10_clientes_valor_total['Data'], color='skyblue')
    plt.title('Top 10 clientes que mais compraram', fontsize=16)
    plt.xlabel('ID do Cliente', fontsize=16)
    plt.ylabel('Quantidade de Compras (Dias Únicos)', fontsize=16)
    plt.tight_layout()
    st.pyplot(plt)

    # escolher os 10 clientes que mais compram
    
def main():
    # Carregar dados
    sales_data, customer_data, customer_sales_data = carrega_dados()
    
    # Análise exploratória
    AED(sales_data, customer_data, customer_sales_data)
    
    # Limpar dados
    sales_data, customer_data, customer_sales_data = limpar_dados(sales_data, customer_data, customer_sales_data)
    
    # Criar gráficos de vendas
    analise_vendas(sales_data)
    
    # Criar gráficos geográficos
    analise_clientes_vendas(customer_data, customer_sales_data)

    insights()


if __name__ == "__main__":
    main()