import requests
import streamlit as st
from snowflake.snowpark.functions import col


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
fruits = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
st.dataframe(data=fruits, use_container_width=True)

pd_df = fruits.to_pandas()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    fruits,
    max_selections=5,
)

if ingredients_list:

    INGREDIENTS_STRING = " ".join(ingredients_list)
    for fruit in ingredients_list:
        st.subheader(f"{fruit} Nutrition Information")
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + INGREDIENTS_STRING + """','""" + name_on_order + """')"""

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order} !', icon="✅")


