import streamlit as st
import pandas as pd
import numpy as np
import requests
import altair as alt
import random

st.set_page_config(
    page_title="Dashboard - Streamlit",
    page_icon=":sauropod:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def inflation(api_key):
    country = 'Germany'
    api_url = 'https://api.api-ninjas.com/v1/inflation?country={}'.format(country)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return pd.DataFrame(data)
    else:
        print("Error:", response.status_code, response.text)

def fetch_random_character():
    url = 'https://rickandmortyapi.com/api/character/'
    response = requests.get(url)
    data = response.json()
    character_count = data['info']['count']
    random_character_id = random.randint(1, character_count)
    random_character_url = f'{url}{random_character_id}'
    response = requests.get(random_character_url)
    character_data = response.json()
    return character_data

def get_random_kitten_image():
    url = 'https://placekitten.com/200/300'
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.content
    else:
        print("Error:", response.status_code, response.text)

def get_crypto_data():
    url = 'https://api.coincap.io/v2/assets'
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data['data']
    else:
        print("Error:", response.status_code, response.text)

def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

def make_donut_chart(data):
    df = pd.DataFrame(data)
    df['marketCapUsd'] = df['marketCapUsd'].astype(float)
    df = df.sort_values(by='marketCapUsd', ascending=False)
    top_10 = df.head(10)

    source = pd.DataFrame({
        'Currency': top_10['id'],
        'Market Cap (USD)': top_10['marketCapUsd']
    })

    chart = alt.Chart(source).mark_arc().encode(
        theta='Market Cap (USD)',
        color='Currency'
    ).properties(
        width=500,
        height=500
    )

    return chart

def main():
    st.title("Weather")

    inflation_api_key = 'Hj5ZKIpU5sysDLglGp9Tew==CCpkqlHOokQ2qLYI'

    # Embed weather widget
    st.components.v1.html("""
    <a class="weatherwidget-io" href="https://forecast7.com/en/40d71n74d01/new-york/" data-label_1="NEW YORK" data-label_2="WEATHER" data-font="Roboto" data-icons="Climacons Animated" data-theme="original" >NEW YORK WEATHER</a>
    <script>
    !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
    </script>
    """)

    random_character = fetch_random_character()

    col1, col2, col3 = st.columns([1, 3, 1])
    # Display the character's name and image
    col1.subheader("Random Character")
    #col1.write(random_character['name'])
    col1.image(random_character['image'])

    #Display crypto data
    col2.subheader("Crypto Data")
    crypto_data = get_crypto_data()
    col2.dataframe(crypto_data)

    #display random kitten
    col3.subheader("Random Kitten")
    kitten_image = get_random_kitten_image()
    col3.image(kitten_image)

    #call the api
    col1.subheader("Inflation Rate of Germamy")
    data = inflation(inflation_api_key)
    monthly_rate = data['monthly_rate_pct']

    #change the data type to string
    monthly_rate = monthly_rate.astype(str)

    #extract just the percentage value 
    percentage_value = monthly_rate.iloc[0].split('%')[0].strip()

    #convert the decimal to percentage
    percentage = round(float(percentage_value) * 100)
    inflationchart = make_donut(percentage, 'Inflation Rate', 'blue')
    col1.altair_chart(inflationchart)

    #second chart
    crypto_data = get_crypto_data()

    col2.subheader("Top 10 Cryptocurrencies by Market Cap")
    col2.altair_chart(make_donut_chart(crypto_data))


if __name__ == "__main__":
    main()