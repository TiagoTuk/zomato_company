# Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import inflection
import numpy as np


st.set_page_config( page_title='Cities', layout='wide', page_icon='🏢' )


#============================================================
#Funções
#============================================================


def city_cuisines(df1):
    df_aux = ( df1.loc[:, ['city', 'cuisines']]
             .groupby(['city'])
             .nunique()
             .sort_values('cuisines', ascending=False)
             .reset_index() )
    
    df_aux_top10 = df_aux.head(10)
    
    fig = px.bar(df_aux_top10,
                 x='city',
                 y='cuisines',
                 text='cuisines',
                 labels={'city': 'Cidade', 'cuisines': 'Tipos de culinária'},
                 color='cuisines',
                 color_continuous_scale=px.colors.sequential.Viridis)
    
    fig.update_layout(xaxis_title='Cidade',
                      yaxis_title= 'Qt tipos de culinária',
                      showlegend=False)
    
    return fig


def plot_top_cities(df, rating_threshold, comparison_operator):
    if comparison_operator == 'greater':
        df_aux = (df1.loc[df['aggregate_rating'] > rating_threshold, ['city', 'restaurant_id']]
                  .groupby(['city'])
                  .nunique()
                  .sort_values('restaurant_id', ascending=False)
                  .reset_index())
    elif comparison_operator == 'less':
        df_aux = (df1.loc[df['aggregate_rating'] < rating_threshold, ['city', 'restaurant_id']]
                  .groupby(['city'])
                  .nunique()
                  .sort_values('restaurant_id', ascending=False)
                  .reset_index())
    
    df_aux_top10 = df_aux.head(10)
    
    fig = px.bar(df_aux_top10,
                 x='city',
                 y='restaurant_id',
                 text='restaurant_id',
                 color='city',
                 labels={'city': 'Cidade', 'restaurant_id': 'Quantidade de Restaurantes'})
    
    fig.update_layout(xaxis_title='Cidade',
                      yaxis_title='Qt Restaurantes',
                      showlegend=False)
    
    return fig


def city_top_rest(df1):
    df_aux = ( df1.loc[:, ['city', 'restaurant_id']]
             .groupby(['city'])
             .nunique()
             .sort_values('restaurant_id', ascending=False)
             .reset_index() )
    
    df_aux_top10 = df_aux.head(10)
    
    fig = px.bar(df_aux_top10,
                 x= 'city',
                 y= 'restaurant_id',
                 text= 'restaurant_id',
                 labels={'city': 'Cidade', 'restaurant_id': 'Quantidade de Restaurantes'},
                 color_discrete_sequence=['#1E3A8A'])
        
    fig.update_layout(xaxis_title='Cidade',
                      yaxis_title= 'Qt Restaurantes',
                      showlegend=False)
    return fig
    

# Ajustando colunas

def clean_code(dataframe):
    # alterando o dataframe (Country Code, Price range e Rating color)
    for i in range(len ( df )):
        df.loc[i, 'country_code'] = country_name(df.loc[i, 'country_code'])
        df.loc[i, 'price_range'] = create_price_tye(df.loc[i, 'price_range'])
        df.loc[i, 'rating_color'] = color_name(df.loc[i, 'rating_color'])
    
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else x)
    
    return df

#Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

#Criação do nome das Cores
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]

#Criação do Tipo de Categoria de Comida
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


#Preenchimento do nome dos países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]



##===========================================================Inicio da Estrutura lógica do código============================================================
#============================================================
# Import dataset
#============================================================
df = pd.read_csv( 'dataset/zomato.csv' )
df = rename_columns(df)

df1 = clean_code(df)

#============================================================
# Barra Lateral - Streamlit
#============================================================

#image_path = 'C:\\Users\\Tiago\\repos\\ftc_programacao_python\\meta.png' # por se tratar de windows tenho que usar barra dupla
image = Image.open( 'food.png' )

st.sidebar.image(image, width=60)

st.sidebar.markdown( '# Fome Zero' )
st.sidebar.markdown( '## Filtros' )


country_options = st.sidebar.multiselect(
    'Escolha os Países que Deseja visualizar os Restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
     'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 
     'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'],
    default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

# Filtro de país
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

df1_tratado = df1

st.sidebar.markdown( '## Dados Tratados' )

csv = df1_tratado.to_csv(index=False)

st.sidebar.download_button(
    label="📥 Dowload",
    data=csv,
    file_name='dados_tratados.csv',
    mime='text/csv')



#============================================================
# Layout do Streamlit
#============================================================
with st.container():
    st.header('Top 10 cidades com mais restaurantes na Base de Dados')

    fig = city_top_rest(df1)
    
    st.plotly_chart (fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        st.markdown('Top 10 cidades com Restaurantes com média de avaliação acima de 4.0')
        
        fig = plot_top_cities(df1, rating_threshold=4.0, comparison_operator='greater')        
        st.plotly_chart (fig, use_container_width=True)
        
    with col2:
        st.markdown('Top 10 cidades com Restaurantes com média de avaliação abaixo de 2.5')
        
        fig = plot_top_cities(df1, rating_threshold=2.5, comparison_operator='less') 
        st.plotly_chart (fig, use_container_width=True)
        
with st.container():
    st.header('Top 10 Cidades com mais restaurantes com tipos culinários distintos')
    
    fig = city_cuisines(df1)
    
    st.plotly_chart (fig, use_container_width=True)
        
        
                 