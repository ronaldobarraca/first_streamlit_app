
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s new Healthy Dinner');

streamlit.header('Breakfast Favorites');
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal');
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie');
streamlit.text('🐔 Hard-Boiled Free-Range Egg');
streamlit.text('🥑🍞 Avocado Toast');
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇');

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
#novo indice da lista
my_fruit_list = my_fruit_list.set_index('Fruit');
#multiselect
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries']);

fruits_to_show = my_fruit_list.loc[fruits_selected];
# display the table on page
streamlit.dataframe(fruits_to_show);

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice);
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json());
  return fruityvice_normalized;


streamlit.header('Fruityvice Fruit Advice!');
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon");
#streamlit.text(fruityvice_response.json());
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?');
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information");
  else:
      back_from_function = get_fruityvice_data(fruit_choice);
      streamlit.dataframe(back_from_function);
except URLError as e:
  streamlit.error();
  


streamlit.header("The Fruit Load List Contains:")
#snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()
  
#add a button to load fruits
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    
