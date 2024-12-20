import streamlit as st
from langchain_helper import generate_restaurant_name_and_items

st.title("Restaurant Name Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine",("Indian","Italian","Mexican","Pakistani"))

# def generate_restaurant_name_and_items(cuisine):
#     return {
#         'restaurant_name':'Curry Delight',
#         'menu_items':'samosa,paneer tikka'
#     }

if cuisine:
    response = generate_restaurant_name_and_items(cuisine)
    st.header(response['restaurant_name'].strip())
    menu_items = response['menu_items'].strip().split(",")
    st.write("****Menu items****")
    for item in menu_items:
        st.write("-",item)




    