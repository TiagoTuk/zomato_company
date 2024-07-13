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


st.set_page_config( page_title='Cuisines', layout='wide', page_icon='🍴' )

#============================================================
#Funções
#============================================================

def plot_cuisine_ratings(df, ascending=False, color_continuous_scale='Blues'):
    df_aux = ( df1.loc[:, ['cuisines', 'aggregate_rating']]
             .groupby(['cuisines'])
             .mean()
             .sort_values('aggregate_rating', ascending=ascending)
             .reset_index() )
        
    df_aux_top = df_aux.head(10)

    fig = px.bar(df_aux_top,
                 x='cuisines',
                 y='aggregate_rating',
                 text= 'aggregate_rating',
                 labels={'cuisines': 'Tipo de Culinária', 'aggregate_rating': 'Média de Avaliação Média'},
                 color='aggregate_rating',
                 color_continuous_scale=color_continuous_scale)

    fig.update_layout(xaxis_title='Tipo de Culinária',
                      yaxis_title= 'Média de Avaliação Média',
                      showlegend=False)

    return fig
    

def top_restaurants_by_rating(df_aux):
    df_aux = ( df2.loc[:, ['restaurant_id', 'restaurant_name','country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating']]
                  .groupby(['restaurant_id'])
                  .max()
                  .sort_values('aggregate_rating', ascending=False)
                  .reset_index() )
    
    df_aux_top = df_aux.head(rest_slider)
    df_aux_top['restaurant_id'] = df_aux_top['restaurant_id'].apply(lambda x: f'{int(x):d}')

    return df_aux_top
    
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


rest_slider = st.sidebar.slider(
    'Selecione a quantidade de Restaurantes que deseja visualizar', 
    value=10,
    min_value=1,
    max_value=20)

cuisines_options = st.sidebar.multiselect(
    'Escolha os Tipos de Culinária',
    ['Italian','European','Filipino','American','Korean','Pizza','Taiwanese','Japanese','Coffee','Chinese','Seafood','Singaporean','Vietnamese','Latin American','Healthy Food','Cafe','Fast Food','Brazilian','Argentine','Arabian','Bakery','Tex-Mex','Bar Food','International','French','Steak','German','Sushi','Grill','Peruvian','North Eastern','Ice Cream','Burger','Mexican','Vegetarian','Contemporary','Desserts','Juices','Beverages','Spanish','Thai','Indian','Mineira','BBQ','Mongolian','Portuguese','Greek','Asian','Author','Gourmet Fast Food','Lebanese','Modern Australian','African','Coffee and Tea','Australian','Middle Eastern','Malaysian','Tapas','New American','Pub Food','Southern','Diner','Donuts','Southwestern','Sandwich','Irish','Mediterranean','Cafe Food','Korean BBQ','Fusion','Canadian','Breakfast','Cajun','New Mexican','Belgian','Cuban','Taco','Caribbean','Polish','Deli','British','California','Others','Eastern European','Creole','Ramen','Ukrainian','Hawaiian','Patisserie','Yum Cha','Pacific Northwest','Tea','Moroccan','Burmese','Dim Sum','Crepes','Fish and Chips','Russian','Continental','South Indian','North Indian','Salad','Finger Food','Mandi','Turkish','Kerala','Pakistani','Biryani','Street Food','Nepalese','Goan','Iranian','Mughlai','Rajasthani','Mithai','Maharashtrian','Gujarati','Rolls','Momos','Parsi','Modern Indian','Andhra','Tibetan','Kebab','Chettinad','Bengali','Assamese','Naga','Hyderabadi','Awadhi','Afghan','Lucknowi','Charcoal Chicken','Mangalorean','Egyptian','Malwani', 'Armenian','Roast Chicken','Indonesian','Western', 'Dimsum','Sunda','Kiwi','Asian Fusion','Pan Asian','Balti','Scottish','Cantonese','Sri Lankan','Khaleeji','South African','Drinks Only','Durban','World Cuisine','Izgara','Home-made','Giblets','Fresh Fish','Restaurant Cafe','Kumpir','Döner','Turkish Pizza','Ottoman','Old Turkish Bars','Kokoreç'],
    default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian'])

# Filtro de culinária
linhas_selecionadas = df1['cuisines'].isin(cuisines_options)
df2 = df1.loc[linhas_selecionadas, :]

df1_tratado = df2

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
st.header('🍴 Visão Tipos de Cusinhas')
with st.container():
    st.markdown('### Melhores Restaurantes dos Principais tipos Culinários')
    col1, col2, col3, col4, col5 = st.columns( 5 )
    
    df_top_restaurants = (df2.loc[:, ['restaurant_name', 'cuisines', 'aggregate_rating']]
                          .sort_values('aggregate_rating', ascending=False)
                          .head(5))
    
    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        if idx < len(df_top_restaurants):
            cuisine = df_top_restaurants.iloc[idx]['cuisines']
            restaurant = df_top_restaurants.iloc[idx]['restaurant_name']
            rating = df_top_restaurants.iloc[idx]['aggregate_rating']
            col.markdown(f"""
                <div style="text-align: center;">
                <span style="font-size: 16px;"><strong>{cuisine} - {restaurant}</strong></span><br>
                <span style="font-size: 24px; color: #4CAF50;"><strong>{rating}/5.0</strong></span>
                </div>
                """, unsafe_allow_html=True)
        
with st.container():
    st.header('Top Restaurante')
    
    df_aux_top = top_restaurants_by_rating(df2)
    st.dataframe(df_aux_top)
    

with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        st.markdown('Top 10 melhores tipos de culinária')
        fig = plot_cuisine_ratings(df1, ascending=False, color_continuous_scale='Blues')
        
        st.plotly_chart (fig, use_container_width=True)
        
        
    with col2:
        st.markdown('Top 10 piores tipos de culinária')
        fig = plot_cuisine_ratings(df1, ascending=True, color_continuous_scale=[(0, 'darkred'), (1, 'lightcoral')])
                
        st.plotly_chart (fig, use_container_width=True)