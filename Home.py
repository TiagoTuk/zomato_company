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


st.set_page_config( page_title='Main Page', layout='wide', page_icon='📊' )

#============================================================
#Funções
#============================================================

def country_maps(df1):
    mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(mapa)
    
    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['restaurant_name'],
            icon=folium.Icon(color=row['rating_color'])  # Usar a cor da coluna 'rating_color'
            ).add_to(marker_cluster)
    
    folium_static(mapa, width=1024, height=600)
    
    return None

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

st.markdown ('# Fome Zero!')
st.header('O Melhor lugar para encontrar seu mais novo restaurante favorito!')

st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
with st.container():
    col1, col2, col3, col4, col5 = st.columns( 5 )
    with col1:
        #st.markdown('Restaurantes Cadastrados')
        qt_restaurantes = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados', qt_restaurantes)
        
    with col2:
        #st.markdown('Países Cadastrados')
        qt_country = df1['country_code'].nunique()
        col2.metric('Países Cadastrados', qt_country)
        
    with col3:
        #st.markdown('Cidades Cadastradas')
        qt_city = df1['city'].nunique()
        col3.metric('Cidades Cadastradas', qt_city)
        
    with col4:
        #st.markdown('Avaliações Feitas na Plat')
        total_avaliacao = df1['votes'].sum()
        col4.metric('Avaliações Feitas na Plat', total_avaliacao)
        
    with col5:
        #st.markdown('Tipos de Culinárias Oferecida')
        tipo_culinaria = df1['cuisines'].nunique()
        col5.metric('Tipos de Culinárias Oferecida', tipo_culinaria)
        
with st.container():
    country_maps(df1)
    
    