import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# FruityVice API call
streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information on it')
    else:
        return_data = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(return_data)
        
except URLError as e:
    streamlit.error()

# Fruit list
streamlit.text("The fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list (FRUIT_NAME) VALUES ('" + fruit_to_add + "')")
        return 'Thanks for adding ' + fruit_to_add

fruit_to_add = streamlit.text_input('What fruit would you like to add?','')
if streamlit.button('Add Fruit To List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    func_return = insert_row_snowflake()
    my_cnx.close()
    streamlit.text(func_return)
