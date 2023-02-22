import os
from dotenv import *
from twilio.rest import Client
from flight_search import FlightSearch

load_dotenv()

smsAcc = os.getenv("SMS_ACC")
smsApi = os.getenv("SMS_API")
smsNum = os.getenv("SMS_NUM")
myNum = os.getenv("My_NUM")





myFlight = FlightSearch()

flight= myFlight.search()


class NotificationManager:
    
    def send(self):
        
        client = Client(smsAcc, smsApi)

        msg = f"\n\n\nFlight from {(flight.frm).upper()} to {(flight.to).upper()} in just Rs. {flight.price}.\n\n\nBy Piyush Pant"       
        msg = client.messages.create( 
            body= msg, 
            from_=smsNum, 
            to=myNum, 
        )
        print("Notification sent successfully!")


    
