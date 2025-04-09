# Importar paquetes Python
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
from datetime import datetime

# Conexión a Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Título de la aplicación
st.title("🍹 Sistema de Pedidos de Smoothies")
st.write("Crea pedidos personalizados de smoothies")

# Función para crear pedidos
def create_order(customer_name, fruits, is_filled=False):
    ingredients_str = ' '.join(fruits)
    
    insert_stmt = f"""
    INSERT INTO smoothies.public.orders(
        NAME_ON_ORDER,
        INGREDIENTS,
        ORDER_FILLED,
        ORDER_TS
    ) VALUES (
        '{customer_name}',
        '{ingredients_str}',
        {is_filled},
        CURRENT_TIMESTAMP()
    )
    """
    session.sql(insert_stmt).collect()
    return True

# Sección 1: Pedido de Kevin (No completado)
with st.expander("Pedido de Kevin (Manzana, Lima, Ximenia)"):
    fruits = ['Apple', 'Lime', 'Ximenia']
    st.write("Creando pedido para Kevin con:", ", ".join(fruits))
    
    if st.button("Crear Pedido de Kevin"):
        if create_order("Kevin", fruits, is_filled=False):
            st.success("✅ Pedido de Kevin creado (no completado)")

# Sección 2: Pedido de Divya (Completado)
with st.expander("Pedido de Divya (Fruta del Dragón, Guayaba, Higos, Jackfruit, Arándanos)"):
    fruits = ['Dragon Fruit', 'Guava', 'Figs', 'Jackfruit', 'Blueberries']
    st.write("Creando pedido para Divya con:", ", ".join(fruits))
    
    if st.button("Crear Pedido de Divya"):
        if create_order("Divya", fruits, is_filled=True):
            st.success("✅ Pedido de Divya creado y marcado como completado")

# Sección 3: Pedido de Xi (Completado)
with st.expander("Pedido de Xi (Fruta Vainilla, Nectarina)"):
    fruits = ['Vanilla Fruit', 'Nectarine']
    st.write("Creando pedido para Xi con:", ", ".join(fruits))
    
    if st.button("Crear Pedido de Xi"):
        if create_order("Xi", fruits, is_filled=True):
            st.success("✅ Pedido de Xi creado y marcado como completado")

# Sección adicional: Crear pedido personalizado
with st.expander("➕ Crear Nuevo Pedido Personalizado"):
    custom_name = st.text_input("Nombre del Cliente")
    fruit_options = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
    fruit_list = [row['FRUIT_NAME'] for row in fruit_options]
    
    selected_fruits = st.multiselect(
        "Selecciona frutas para el smoothie",
        fruit_list
    )
    
    is_filled = st.checkbox("¿Pedido completado?")
    
    if st.button("Crear Pedido Personalizado") and custom_name and selected_fruits:
        if create_order(custom_name, selected_fruits, is_filled):
            st.success(f"✅ Pedido para {custom_name} creado exitosamente!")
