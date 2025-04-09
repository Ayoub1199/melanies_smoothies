# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# App title
st.title("🍹 Smoothie Order System")
st.write("Create custom smoothie orders below")

# Section 1: Kevin's Order (Not Filled)
with st.expander("Kevin's Order (Apples, Lime, Ximenia)"):
    fruits = ['Apple', 'Lime', 'Ximenia']
    st.write("Creating order for Kevin with:", ", ".join(fruits))
    
    if st.button("Create Kevin's Order"):
        insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, customer_name, is_filled)
        VALUES ('{" ".join(fruits)}', 'Kevin', FALSE)
        """
        session.sql(insert_stmt).collect()
        st.success("Kevin's order created (not filled)")

# Section 2: Divya's Order (Filled)
with st.expander("Divya's Order (Dragon Fruit, Guava, Figs, Jackfruit, Blueberries)"):
    fruits = ['Dragon Fruit', 'Guava', 'Figs', 'Jackfruit', 'Blueberries']
    st.write("Creating order for Divya with:", ", ".join(fruits))
    
    if st.button("Create Divya's Order"):
        insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, customer_name, is_filled)
        VALUES ('{" ".join(fruits)}', 'Divya', TRUE)
        """
        session.sql(insert_stmt).collect()
        st.success("Divya's order created and marked filled")

# Section 3: Xi's Order (Filled)
with st.expander("Xi's Order (Vanilla Fruit, Nectarine)"):
    fruits = ['Vanilla Fruit', 'Nectarine']
    st.write("Creating order for Xi with:", ", ".join(fruits))
    
    if st.button("Create Xi's Order"):
        insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, customer_name, is_filled)
        VALUES ('{" ".join(fruits)}', 'Xi', TRUE)
        """
        session.sql(insert_stmt).collect()
        st.success("Xi's order created and marked filled")
