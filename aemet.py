import requests
import json
import datetime
import conf_management as ConfMgt


def get_weather(token):
    now = datetime.datetime.now()    

    return_text = ''

    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/" + ConfMgt.get_city_id()

    payload = {}
    headers = {
        'api_key': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code != 200:
        return False, 0

    y = json.loads(response.content)

    """
    La llamada anterior me da un json con una url donde están los datos.
    Obtengo la nueva url y vuelvo a hacer un GET
    """
    url = y['datos']

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code != 200:
        return False, return_text

    y = json.loads(response.content.decode('latin-1'))

    prediction = None

    for day in y[0]['prediccion']['dia']:
        date_consult = datetime.datetime.strptime(day['fecha'], '%Y-%m-%dT%H:%M:%S')

        if date_consult.day == now.day:
            prediction = day
            break

    prob = prediction['probPrecipitacion'][0]['value']

    return_text = '######## PREVISIÓN METEOROLÓGICA ########\n\n'
    return_text += 'Probabilidad de lluvia en ' + y[0]['nombre'] + ' es de: ' + str(prob) + ' %'

    sky_state = prediction['estadoCielo'][0]['descripcion']

    if sky_state != '':
        return_text += '\nEl estado del cielo es: ' + sky_state

    maximum_temperature = prediction['temperatura']['maxima']
    minimum_temperature = prediction['temperatura']['minima']

    temperature_text = '\nLa temperatura máxima será de ' + str(maximum_temperature) + ' ºC y la mínima de ' + str(minimum_temperature) + ' ºC'

    return_text += temperature_text

    return True, return_text
