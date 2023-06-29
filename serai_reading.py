import serial.tools.list_ports
import requests

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
            temperature = float(decoded_packet[temperature_start:temperature_end].strip())
            
            humidity_start = decoded_packet.find("Humidity:") + len("Humidity:")
            humidity_end = decoded_packet.find("%")
            humidity = float(decoded_packet[humidity_start:humidity_end].strip())
            
            # Print the values
            print("Temperature Value:", temperature, "°C")
            print("Humidity Value:", humidity, "%")
            
            # Prepare the data to be sent
            data = {
                'temperature': temperature,
                'humidity': humidity
            }
                
        except UnicodeDecodeError:
            decoded_packet = packet.decode('latin-1')
            print(decoded_packet)
