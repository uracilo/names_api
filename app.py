from flask import Flask, request
from flask_cors import CORS

import requests
import json


app = Flask(__name__)
CORS(app)

def get_country_name(name):
    nationalize = "https://api.nationalize.io?name=" + name
    validated_api =requests.get(nationalize)
    response_api = validated_api.json()
    country_code = response_api['country'][0]['country_id']
    value_percent = response_api['country'][0]['probability']
    percentage = "{:.2%}".format(value_percent)
    country_name = 'https://restcountries.eu/rest/v2/alpha?codes=' + country_code
    validated_api_country =requests.get(country_name)
    response_api_country = validated_api_country.json()
    country_name = response_api_country[0]['name']
    final_response= "Name from " + str(country_name) + " with " + percentage + " accurrate"
    return country_name,percentage


@app.route('/')
def index():
    return 'health check! '

@app.route("/names",methods=['GET','POST'])
def names_data():
    names = request.form['name']
    names_data = [{"value": get_country_name(names)}]
    names_json = json.dumps(names_data)
    return(names_json)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)