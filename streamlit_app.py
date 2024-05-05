import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be ", name_on_order)

session = get_active_session()
fruits = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
st.dataframe(data=fruits, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    fruits,
    max_selections=5,
)

if ingredients_list:

    INGREDIENTS_STRING = " ".join(ingredients_list)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + INGREDIENTS_STRING + """','""" + name_on_order + """')"""

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order} !', icon="✅")

