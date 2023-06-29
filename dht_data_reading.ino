#include <DHT.h>

#define DHTPIN 2      // Pin where the DHT11 sensor is connected
#define DHTTYPE DHT11 // DHT sensor type (DHT11 for this case)

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  delay(2000); // Allow time for the sensor to stabilize
}

void loop() {
  float temp = dht.readTemperature();
  float humid = dht.readHumidity();

  if (isnan(temp) || isnan(humid)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print(" °C\t");
  Serial.print("Humidity: ");
  Serial.print(humid);
  Serial.println(" %");

  delay(2000); // Delay between sensor readings
}
