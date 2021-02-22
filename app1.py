from flask import Flask, request, render_template
import numpy as np
import re
import requests
import json
import csv
import pandas as pd
app = Flask(__name__)

def check(output):
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"

    querystring = {"country":output}

    headers = {
        'x-rapidapi-key': "43c148b330mshc12403643be54b7p1bcf37jsnb2253c16d193",
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
  
    value = response.text
    output=json.loads(value)
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/stats')
def stats():
    return render_template('stats.html')
    
@app.route('/statistics', methods=['POST'])
def statistics():
    total=0
    output = request.form['country']
    print(output)
    essay = check(output)
    print(essay['data'])
    data_file = open('data_file.csv', 'w') 
    csv_writer = csv.writer(data_file) 
    count = 0
    for emp in essay['data']: 
        print(emp)
        if count == 0: 
            # Writing headers of CSV file   
            header = ['Status','Cases']
            csv_writer.writerow(header) 
            count += 1
    # Writing data of CSV file 
    
        if(emp=="recovered" or emp=="deaths" or emp=="confirmed"):
            d = [emp,essay['data'][emp]]
            total = total + essay['data'][emp]
            print(d)
            csv_writer.writerow(d) 
    data_file.close() 
    df = pd.read_csv("data_file.csv")
    temp = df.to_dict('records')
    columnNames = df.columns.values
    recovered = essay['data']['recovered'] * 100/total
    deaths = essay['data']['deaths'] * 100/total
    confirmed = essay['data']['confirmed'] * 100/total
    
    return render_template('result.html',essay=essay['data']['location'],records=temp, colnames=columnNames,recover_percentage=recovered,death_percentage=deaths,confirmed_percentage=confirmed)
 
 

    
if __name__ == "__main__":
    app.run(debug=True)
