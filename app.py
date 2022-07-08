import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import folium
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from geopy.distance import geodesic

st.title("Où sont les musées les plus proches !!!") 

loc_button = Button(label="Me geolocaliser")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)


if(result != None):

    st.write("lat : " + str(result['GET_LOCATION']['lat']))
    st.write("lon : " + str(result['GET_LOCATION']['lon']))







    title = st.text_input('Artiste')
    st.write(title)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="musee2"
    )

    mycursor = mydb.cursor()

    # mycursor.execute('SELECT * FROM oeuvre_artiste,oeuvre,artiste,geo WHERE oeuvre_artiste.id_oeuvre =  oeuvre.id AND oeuvre_artiste.id_artiste = artiste.id AND oeuvre.id_geo = geo.id AND artiste.name in ("'+ title +'") OR oeuvre.name in ("'+ title +'")  ')

    mycursor.execute("SELECT oeuvre.name as titre , artiste.name as auteur , geo.lat as lat , geo.lon as lon FROM oeuvre_artiste,oeuvre,artiste,geo WHERE oeuvre_artiste.id_oeuvre =  oeuvre.id AND oeuvre_artiste.id_artiste = artiste.id AND oeuvre.id_geo = geo.id AND artiste.name= '"+ title +"' Limit 100")

    # mycursor.execute("SELECT * FROM oeuvre_artiste,oeuvre,artiste,geo WHERE oeuvre_artiste.id_oeuvre =  oeuvre.id AND oeuvre_artiste.id_artiste = artiste.id AND oeuvre.id_geo = geo.id  Limit 100")

    myresult = mycursor.fetchall()

    latlong = []
    distance = []

    columns = ["titre" , "auteur" , "lat" , "lon" , "distance"]
    data = []

    def renvoi_distance(coord1_1, coord1_2 , coord2_1 , coord2_2):
    #les coordonnées sont stockées en string nous devons donc les transformer en tuple
        ville1=(float(coord1_1) , float(coord1_2))
        ville2=(float(coord2_1) , float(coord2_2))
        return geodesic(ville1, ville2).km

    for x in myresult:
    #   st.text(x)
        data2 = []
        data2.append(x[0])
        data2.append(x[1])
        data2.append(x[2])
        data2.append(x[3])
        # latlong.append([float(x[10]),float(x[11])])
        if(result != None):
        # st.text(renvoi_distance(result['GET_LOCATION']['lat'],result['GET_LOCATION']['lon'], x[2] , x[3] ))
            data2.append(renvoi_distance(result['GET_LOCATION']['lat'],result['GET_LOCATION']['lon'], x[2] , x[3] ))
    
        data.append(data2)

    # df = pd.DataFrame(
    #      latlong,
    #      columns=['lat', 'lon'])
    df = pd.DataFrame(data=data,columns=columns)

    df = df.sort_values(by=['distance'])

    df['lat'] = df['lat'].astype('float')
    df['lon'] = df['lon'].astype('float')


# st.text(latlong)
    st.dataframe(df)
    st.map(df[['lat','lon']])







