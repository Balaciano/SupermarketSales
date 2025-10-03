import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide") #Ocupa todo o espaço horizontal da página

#O QUE QUEREMOS ANALISAR (com uma visão mensal)
    #Faturamento por unidade
    # tipo de produto mais vendido
    #Contribuição por filial
    #Desempenho das formas de pagamento
    #Como estão as avaliações das filiais?
    

#Serve para ler um arquivo CSV (se fosse um Excel, seria pd.read_excel)
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",") 

df["Date"] = pd.to_datetime(df["Date"])  #Converter o texto em Data
df = df.sort_values(by="Date") #Ordenar por data 
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
#df["Month"] --> Ta criando uma coluna de mês


#Cria o filtro de selecionar pelo mes e ano
months = ["Todos"] + list(df["Month"].unique())
month = st.sidebar.selectbox("Mês", months)
if month != "Todos":
    df_filtered = df[df["Month"] == month]
else:
    #Sem filtro
    df_filtered = df


df

#Ele pega de cima para baixo (Igual em dev Web) e vai dividindo os frames em colunas que você chama
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)


fig_date = px.bar(df_filtered, x="Date", y="Total", title="Faturamento por dia", color="City")
col1.plotly_chart(fig_date)



product_date = px.bar(df_filtered, x="Date", y="Product line", title="Tipo de produto mais vendido", color="Product line", orientation="h")
col2.plotly_chart(product_date)



city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
City_date =  px.bar(df_filtered, x="City", y="Total", title="Faturamento por filial")
col3.plotly_chart(City_date)


fig_Kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_Kind)



city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(df_filtered, x="City", y="Rating", title="Avaliação", orientation="v")
col5.plotly_chart(fig_rating)