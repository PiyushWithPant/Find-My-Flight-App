import requests as req
import os
from dotenv import *
from pprint import pprint
import datetime as dt
from flight_data import FlightData


load_dotenv()

flightSearch = "https://api.tequila.kiwi.com"


class FlightSearch:
    
    def __init__(self):
        self.flightApikey = os.getenv("tequilaKey")
        self.sheetyEndpoint = os.getenv("sheetyEndpoint")
        self.cities = ""
        self.flights =[]
        
    def getPriceForCity(self, cityCode):
        headers ={
            "apikey": self.flightApikey,
        }
        
        params={
            "fly_from": "IN",
            "fly_to":cityCode,
            "date_from": dt.datetime.now().strftime("%d/%m/%Y"),
            "date_to":(dt.datetime.now() + dt.timedelta(days=180)).strftime("%d/%m/%Y"),
            "curr":"INR"
        }
        
        
        try:
        
            res = req.get(url=f"{flightSearch}/v2/search", params=params, headers=headers).json()
 
        
        except IndexError:
            print("No Flight found!")
            return None
        
        else:
            
            flightPrice = res["data"][0]["price"]
            
            return flightPrice

    
    
        
    def search(self):

        sheetData= req.get(url=self.sheetyEndpoint).json()["data"]
        codeList = []
        for dict in sheetData:
            codeList.append(dict["iataCode"])
         
        self.cities = ",".join(codeList)
        
        
        
        headers ={
            "apikey": self.flightApikey,
        }
        
        params={
            "fly_from": "IN",
            "fly_to":self.cities,
            "date_from": dt.datetime.now().strftime("%d/%m/%Y"),
            "date_to":(dt.datetime.now() + dt.timedelta(days=180)).strftime("%d/%m/%Y"),
            "curr":"INR"
            
            
            
        }
        
        try:
        
            res = req.get(url=f"{flightSearch}/v2/search", params=params, headers=headers).json()
            for i in range(6):
                flight = res["data"][i]
                self.flights.append(flight)
                
            
        except IndexError:
            print("No Flight found!")
            return None
        else:
            
            myFlight = FlightData(
                frm = self.flights[0]["cityFrom"],
                to = self.flights[0]["cityTo"],
                price= self.flights[0]["price"],
            )

            return myFlight
        
