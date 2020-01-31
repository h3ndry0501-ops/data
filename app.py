from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

def scrap(url):
    #This is fuction for scrapping
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    #Find the key to get the information
    table = soup.find('table', attrs={'class':'table'})
    tr = table.find_all('tr')

    temp = [] #initiating a tuple

    temp = [] #initiating a tuple

    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]

        #get tanggal
        tanggal = row.find_all('td')[0].text
        tanggal = tanggal.strip() #for removing the excess whitespace

        #get kurs beli
        kurs_beli = row.find_all('td')[1].text
        kurs_beli = kurs_beli.strip() #for removing the excess whitespace

        #get kurs jual
        kurs_jual = row.find_all('td')[2].text
        kurs_jual = kurs_jual.strip() #for removing the excess whitespace

        temp.append((tanggal,kurs_beli,kurs_jual)) 
   
    temp = temp[::-1] #remove the header

    df = pd.DataFrame(temp, columns = ('tanggal','kurs_beli','kurs_jual')) #creating the dataframe
   #data wranggling -  try to change the data type to right data type

    df['tanggal'] = df['tanggal'].replace('Januari', 'January', regex=True)
    df['tanggal'] = df['tanggal'].replace('Februari', 'February', regex=True)
    df['tanggal'] = df['tanggal'].replace('Maret', 'March', regex=True)
    df['tanggal'] = df['tanggal'].replace('April', 'April', regex=True)
    df['tanggal'] = df['tanggal'].replace('Mei', 'May', regex=True)
    df['tanggal'] = df['tanggal'].replace('Juni', 'June', regex=True)
    df['tanggal'] = df['tanggal'].replace('Juli', 'July', regex=True)
    df['tanggal'] = df['tanggal'].replace('Agustus', 'August', regex=True)
    df['tanggal'] = df['tanggal'].replace('September', 'September', regex=True)
    df['tanggal'] = df['tanggal'].replace('Oktober', 'October', regex=True)
    df['tanggal'] = df['tanggal'].replace('November', 'November', regex=True)
    df['tanggal'] = df['tanggal'].replace('Desember', 'December', regex=True)

    df['tanggal'] = df['tanggal'].astype('datetime64')

    df['kurs_beli'] = df['kurs_beli'].replace(',', '.', regex=True)
    df['kurs_jual'] = df['kurs_jual'].replace(',', '.', regex=True)

    df['kurs_beli'] = df['kurs_beli'].astype('float')
    df['kurs_jual'] = df['kurs_jual'].astype('float')

    df= df.set_index('tanggal')

   #end of data wranggling

    return df

@app.route("/")
def index():
    df = scrap('https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019') #insert url here

    #This part for rendering matplotlib
    fig = plt.figure(figsize=(5,2),dpi=300)
    df.plot()
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df, result=result)


if __name__ == "__main__": 
    app.run()
