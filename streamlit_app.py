# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in custom smoothie
    """
)

name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your smoothie is", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list=st.multiselect('Select 5 ingredients',my_dataframe,max_selections=6)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string=''
    for x in ingredients_list:
        ingredients_string+=x+' '
        st.subheader('Nutrition information of' +x)
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


