import serial.tools.list_ports
from pymongo.mongo_client import MongoClient
import time

# Establish a connection to MongoDB
uri = "mongodb+srv://<username>:<password>cluster0.8hewqd1.mongodb.net/"

client = MongoClient(uri)

db = client['sensorreadings']
collection = db['readings']

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input("select port: ")

for x in range(0, len(portList)):
    if portList[x].startswith("/dev/" + str(val)):
        portVar = "/dev/" + str(val)
        print(portList[x])

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

while True:
    if serialInst.in_waiting:
        packet = serialInst.readline()
        try:
            decoded_packet = packet.decode('utf-8')
            print(decoded_packet)
            
            # Extract temperature and humidity values
            temperature_start = decoded_packet.find(":") + 1
            temperature_end = decoded_packet.find("°C")
            temperature_str = decoded_packet[temperature_start:temperature_end].strip()
            
            humidity_start = decoded_packet.find("Humidity:") + len("Humidity:")
            humidity_end = decoded_packet.find("%")
            humidity_str = decoded_packet[humidity_start:humidity_end].strip()
            
            # Print the values
            print("Temperature Value:", temperature_str, "°C")
            print("Humidity Value:", humidity_str, "%")
            
            # Convert temperature and humidity to float if possible
            try:
                temperature = float(temperature_str)
                humidity = float(humidity_str)
            except ValueError:
                print("Invalid temperature or humidity value")
                continue
            
            # Prepare the data to be sent
            data = {
                'temperature': temperature,
                'humidity': humidity
            }
            
            # Insert the data into the MongoDB collection
            collection.insert(data)
            time.sleep(2)
                
        except UnicodeDecodeError:
            decoded_packet = packet.decode('latin-1')
            print(decoded_packet)
            
# Close the MongoDB connection
client.close()