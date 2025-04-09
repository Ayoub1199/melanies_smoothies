# Import python packages
import streamlit as st
import requests

# Write directly to the app
st.title("Customize Your Smoothie!:cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
)

# Initialize ingredients_string outside the if block
ingredients_string = ''

if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        try:
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
            smoothiefroot_response.raise_for_status()  # Check for HTTP errors
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching nutrition data for {fruit_chosen}: {e}")

# Prepare the SQL statement (now safe because ingredients_string exists)
if ingredients_string.strip():  # Only proceed if not empty
    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients)
            VALUES ('""" + ingredients_string.strip() + """')"""
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"Error submitting order: {e}")
else:
    st.warning("Please select at least one ingredient to order")

