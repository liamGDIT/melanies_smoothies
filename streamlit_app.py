# Import python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write('Choose the fruits you want in your custom Smoothie!')

name_on_order = st.text_input('Name on Smoothe:')
if name_on_order:
    st.write('The name on the Smoothie will be:', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))

pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_str = ''
    
    for ingredient in ingredients_list:
        ingredients_str += ingredient + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]
        st.write('SCREW YOU', ingredient, 'is', search_on)
        
        st.subheader(ingredient+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ingredient.lower())
        st.write("https://fruityvice.com/api/fruit/"+ingredient.lower())
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        

    insert_btn = st.button('Submit Order')
    
    if insert_btn:
        session.sql(f'''
            insert into smoothies.public.orders
            values (order_seq.nextval, false, '{ingredients_str}', '{name_on_order}', current_timestamp)
        ''').collect()

        st.success(f'Your smoothie is ordered, {name_on_order}!')
