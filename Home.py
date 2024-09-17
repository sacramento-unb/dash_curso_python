import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import folium_static
import geopandas as gpd

GEO_DATA = 'dados/estados.geojson'

st.title('Dashboard Python GeoDev')

st.text('Este é um dashboard de estudo curso Python Geodev')

st.sidebar.title('Sidebar')

arquivo_subido = st.sidebar.file_uploader('Faça o upload do arquivo a ser analisado')

df = pd.read_csv(arquivo_subido)

year = st.sidebar.selectbox('Selecione a coluna de ano',df.columns)

ano = st.sidebar.multiselect('Selecione o ano a ser visulizado',df[year].sort_values(ascending=True).unique())

elemento = st.sidebar.radio('Selecione o elemento a ser visulizado',['Cabeçalho','Resumo','Gráfico','Gráfico interativo','Mapa'])

if arquivo_subido:
    df = df[df[year].isin(ano)].sort_values(by='sigla_uf', ascending=True)
    
    def cabecalho():
        st.header('Cabeçalho do dataframe')
        st.write(df.head())

    def resumo_estatistico():
        st.header('Resumo estatístico do dataframe')
        st.write(df.describe())

    def grafico():
        fig, ax = plt.subplots(1,1)
        ax.scatter(x=df['sigla_uf'],y=df['soja_area_nao_desmat'])
        ax.set_xlabel('Estados')
        ax.set_ylabel(f'Soja nos anos de {ano}(ha)')

        st.pyplot(fig)

    def grafico_interativo():

        col1,col2 = st.columns(2)

        x_val = col1.selectbox('Selecione o eixo X', options=df.columns)

        y_val = col2.selectbox('Selecione o eixo Y', options=df.columns)

        plot = px.scatter(df, x=x_val, y=y_val)

        st.plotly_chart(plot, use_container_width=True)

    def mapa():

        meumapa = folium.Map(location=[-14,-54],zoom_start=4, tiles='CartoDB positron')

        choropleth = folium.Choropleth(
            geo_data=GEO_DATA,
            data=df,
            columns=('sigla_uf','soja_area_nao_desmat'),
            key_on='feature.properties.sigla_uf',
            highlight=True,
            nan_fill_color='grey',
            fill_opacity=0.5,
            line_opacity=0.2,
            legend_name='Soja Brasil',
            show=False
        )
        
        choropleth.geojson.add_to(meumapa)


        def style_function(feature):
            return{
                'fillColor': 'green',
                'color': 'green',
                'weight': 0.1,
                'fillOpacity':0.1,
                'opacity':0.3
            }

        data=(gpd.read_file((GEO_DATA)))

        data = data[data['year'] == str(ano[0])]

        col1,col2 = st.columns(2)

        x_val = col1.selectbox('Selecione o valor a ser plotado', options=data.columns)

        folium.GeoJson(
            data=data,
            tooltip=folium.GeoJsonTooltip(
                columns=('sigla_uf','soja_area_nao_desmat'),
                key_on='feature.properties.sigla_uf',
                fields=['sigla_uf',x_val],
                aliases=['Estado',x_val],
                localize=True,
                show=False
            ),style_function=style_function
        ).add_to(meumapa)


        folium_static(meumapa, width=950, height=500)

else:
    st.warning('Arquivo não subido')

if elemento == 'Cabeçalho':
    cabecalho()
elif elemento == 'Resumo':
    resumo_estatistico()
elif elemento == 'Gráfico':
    grafico()
elif elemento == 'Gráfico interativo':
    grafico_interativo()
elif elemento == 'Mapa':
    mapa()