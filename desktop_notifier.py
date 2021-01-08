import os
import datetime
import time
import requests
from plyer import notification

dir_path = os.path.dirname(os.path.realpath(__file__))
# Getting corona virus data for Azerbaijan
url = 'https://corona-rest-api.herokuapp.com/Api/Azerbaijan/'

data = None
try:
    data = requests.get(url)
except:
    print("Something went wrong.")

if data != None:
    json_data = data.json()['Success']

    while True:
        notification.notify(
            title = f"Covid Stats in Azerbaijan on {datetime.date.today()}",
            message = "Total cases : {totalcases}\nToday cases : {todaycases}\nToday deaths :{todaydeaths}\nTotal active :{active}".format(
                        totalcases = json_data['cases'],
                        todaycases = json_data['todayCases'],
                        todaydeaths = json_data['todayDeaths'],
                        active = json_data["active"]),

            app_icon = dir_path + "/Paomedia-Small-N-Flat-Bell.ico",
            timeout = 50
        )

        time.sleep(60*60*4)
        