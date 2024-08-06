# Import python packages
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_str = ' '.join(ingredients_list)

    insert_btn = st.button('Submit Order')
    
    if insert_btn:
        session.sql(f'''
            insert into smoothies.public.orders
            values ('{ingredients_str}', '{name_on_order}')
        ''').collect()

        st.success(f'Your smoothie is ordered, {name_on_order}!')
