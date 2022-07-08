import pandas as pd
import numpy as np
import mysql.connector

data = pd.read_csv('base-joconde-extrait.csv', sep=";" , low_memory=False)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE musee2")

# ------------------------------------------- création des tables ---------------------------------------------------

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="musee2"
)

mycursor.execute("CREATE TABLE artiste ( id int(11) NOT NULL, name text DEFAULT NULL)")
mycursor.execute("CREATE TABLE oeuvre ( id int(11) NOT NULL, name text DEFAULT NULL, id_geo int(11) FOREIGN KEY REFERENCES geo(id)")
mycursor.execute("CREATE TABLE geo (  id int(11) NOT NULL,  lat text DEFAULT NULL,  lon text DEFAULT NULL,  region text DEFAULT NULL,  ville text DEFAULT NULL)")
mycursor.execute("CREATE TABLE oeuvre_artiste (  id int(11) NOT NULL,  id_oeuvre int(11) FOREIGN KEY REFERENCES oeuvre(id),  id_artiste int(11) FOREIGN KEY REFERENCES artiste(artiste))")


# ------------------------------------ insert table -------------------------------------------------

# insert geo

geo = data[['POP_COORDONNEES','REGION','Ville_']]
geo = geo.dropna()
geo['POP_COORDONNEES'] = geo['POP_COORDONNEES'].astype('string')
geo = geo[geo['POP_COORDONNEES'] != '0.0,0.0']
geo.drop_duplicates(keep = 'first', inplace=True)

for index, row in geo.iterrows():
    
        lat , long = row['POP_COORDONNEES'].split(",")
        mycursor = mydb.cursor()
        sql = 'INSERT INTO geo (lat,lon,region,ville) VALUES (%s, %s,%s, %s)'
        val = (lat,long,row['REGION'],row['Ville_'])
        mycursor.execute(sql,val)

        mydb.commit()


# insert artiste

auteur = data[['POP_COORDONNEES','Auteur']]
auteur = geo.dropna()
auteur['POP_COORDONNEES'] = geo['POP_COORDONNEES'].astype('string')
auteur = geo[geo['POP_COORDONNEES'] != '0.0,0.0']
auteur.drop_duplicates(keep = 'first', inplace=True)

for index, row in geo.iterrows():
    
       
        mycursor = mydb.cursor()
        sql = 'INSERT INTO artiste (name) VALUES (%s)'
        val = (row['Auteur'])
        mycursor.execute(sql,val)

        mydb.commit()

# insert oeuvre

oeuvre = data[['POP_COORDONNEES','Titre','Ville_']]
oeuvre = geo.dropna()
oeuvre['POP_COORDONNEES'] = geo['POP_COORDONNEES'].astype('string')
oeuvre = geo[geo['POP_COORDONNEES'] != '0.0,0.0']
oeuvre.drop_duplicates(keep = 'first', inplace=True)

for index, row in geo.iterrows():
    lat , long = row['POP_COORDONNEES'].split(",")
    mycursor = mydb.cursor()
    mycursor.execute('SELECT id FROM geo WHERE lat ='+str(lat)+' AND lon = '+str(long)+' AND ville =  "'+str(row['Ville_'])+'"')

    myresult = mycursor.fetchall()
    
    

    for x in myresult:

        
        
        
      
        mycursor2 = mydb.cursor()
        sql = "INSERT INTO oeuvre (name,id_geo) VALUES (%s, %s)"
        val = (row['Titre'], x[0])
        mycursor2.execute(sql, val)

        mydb.commit()


# insert oeuvre_artiste

oeuvre_artiste = data[['POP_COORDONNEES','Auteur','Titre']]
oeuvre_artiste = geo.dropna()
oeuvre_artiste['POP_COORDONNEES'] = geo['POP_COORDONNEES'].astype('string')
oeuvre_artiste = geo[geo['POP_COORDONNEES'] != '0.0,0.0']
oeuvre_artiste.drop_duplicates(keep = 'first', inplace=True)

for index, row in geo.iterrows():
    
#     lat , long = row['POP_COORDONNEES'].split(",")
    mycursor = mydb.cursor()
    mycursor.execute('SELECT id FROM artiste WHERE name = "'+row['Auteur']+'"')
    myresult = mycursor.fetchall()
    
    for x in myresult:
        
        mycursor1 = mydb.cursor()
        mycursor1.execute('SELECT id FROM oeuvre WHERE name ="'+row['Titre']+'"') 

        myresult1 = mycursor1.fetchall()
        
        for y in myresult1:
            
            mycursor2 = mydb.cursor()
            
            sql = "INSERT INTO oeuvre_artiste (id_oeuvre,id_artiste) VALUES (%s, %s)"
            val = (y[0], x[0])
            mycursor2.execute(sql, val)

            mydb.commit()


