import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])

# Display the table on the page.
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
     streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


  
def add_fruit(newfruit):
  streamlit.text("1")
  with my_cnx.cursor() as my_cur1:
    my_cur1.execute("Insert Into fruit_load_list values ('newfruit')")
    streamlit.text("2")
    return "Added" + newfruit + "successfully"

if streamlit.button('Add Fruit'):
    new_fruit_choice = streamlit.text_input('What fruit would you like to add?')
    if not new_fruit_choice:
     streamlit.error("Please type a fruit.")
    else:
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_add_function = add_fruit(new_fruit_choice)
      streamlit.text(back_from_add_function)

streamlit.stop()
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Select * From fruit_load_list")
    return my_cur.fetchall()
  
streamlit.header("List of Fruits loaded in snowflake:")
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  my_cnx.close()
