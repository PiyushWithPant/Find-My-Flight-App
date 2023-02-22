import requests as req
import os
from dotenv import *
from pprint import pprint

from flight_search import FlightSearch


load_dotenv()

flightSearch = "https://api.tequila.kiwi.com"



class DataManager:
    
    def __init__(self):
        self.myCity = {}
        self.flightApikey = os.getenv("tequilaKey")
        self.sheetyEndpoint = os.getenv("sheetyEndpoint")
        
    def getCode(self, city):
        """To get the IATA code of a country"""
        flightParams = {
            "term": city
        }
        
        flightHeaders = {
            "apikey": self.flightApikey,
        }
        res = req.get(url = f"{flightSearch}/locations/query", params=flightParams, headers=flightHeaders)
        
        code = res.json()["locations"][0]["code"]
        
        return code
        
    
    
    def getData(self):
        """To get the data from excel to find city codes and to store city and citycode in dictionary"""
        
        # To get data
        res= req.get(url=self.sheetyEndpoint)

        # pprint(res.json())

        data = res.json()["data"]   # List
    
        
        for dict in data:
            city = dict["city"]
            cityCode = self.getCode(city)
            # print(cityCode)
            # now we will store both of them in our dictinary
            self.myCity[city] = cityCode
        
        # print(self.myCity)
        
    def updateCodes(self):
        
        
        id = 2  # 1= heading of table, so data starts from 2 
        for (city, code) in self.myCity.items():
            
            newEndpoint = f"{self.sheetyEndpoint}/{id}"
            
            codeData={
               "datum":{
                   "city":city,
                    "iataCode": code
                }
            }
            
            # updating endpoint
            id += 1
            
            res= req.put(url=newEndpoint, json= codeData)
            print(res.status_code)
          
          
            
    def updatePrice(self):
        
        
        getData= req.get(url=self.sheetyEndpoint)
        data = getData.json()["data"]   # List

        self.codeList  = [item["iataCode"] for item in data]

        
        flight = FlightSearch()
        
        priceList = []
        
        for cityCode in self.codeList:
            
            flightPrice = flight.getPriceForCity(cityCode)
            
            priceList.append(flightPrice)
            
        
        for id in range(2, 8):

            newEndpoint = f"{self.sheetyEndpoint}/{id}"
            codeData={
                "datum":{
                    "flightPrice": priceList[id-2]  # so that the id can start from 0
                    }
            }
            priceUpdateResponse = req.put(url=newEndpoint, json= codeData)
            print("Price Updated")
            
        
    
            
            
        
            
        
        
        
        
        
        
        
# d= DataManager()

# d.updatePrice()

# d.getData()
# d.updateCodes()