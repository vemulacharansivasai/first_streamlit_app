
import streamlit
import pandas
import requests

streamlit.title(' My Moms New Healthy Diner')

streamlit.header(' Breakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry oatmeal')
streamlit.text(' 🥗Kale,Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))


streamlit.dataframe(my_fruit_list)

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("please select a fruit to get information.")
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()



import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.head("The fruit load list contains:")
streamlit.dataframe(my_data_rows)






my_cur.execute("insert into fruit_load_list values('from streamlit')")
