#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import os
from dotenv import *
import requests as req
from pprint import pprint
import datetime as dt
from flight_data import FlightData
from data_manager import DataManager
from flight_search import FlightSearch
from twilio.rest import Client
from notification_manager import NotificationManager

load_dotenv()


# Updating the price regularly

flightprice = DataManager().updatePrice()

notify = NotificationManager()

notify.send()






