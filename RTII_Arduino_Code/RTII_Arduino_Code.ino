#define heaterSelPin A1
const int trigPin = 7;
const int echoPin = 3;

void setup() {

  Serial.begin (9600);

  // Configure the pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(heaterSelPin, OUTPUT);

  digitalWrite(trigPin, LOW);
  digitalWrite(heaterSelPin, LOW);
}

void loop()
{
  float sensor_volt;
  float RS_air = 100.0f;
  float RS_gas; // Get value of RS in a GAS
  float ratio; // Get ratio RS_GAS/RS_air
  int sensorValue = analogRead(A0);
  sensor_volt = (float)sensorValue / 1024 * 5.0;
  RS_gas = sensor_volt / 5.0 - sensor_volt; // omit *R16
  ratio = RS_gas / RS_air; // ratio = RS/R0

  long duration, distance;
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration / 58;


  if (RS_gas >= -1.8f) {
    Serial.println(2);
  } else {
    Serial.println(3);
  }


  if (distance >= 5 && distance <= 15)
  {
    Serial.println(1);
  }
  else
  {
    Serial.println(0);
  }

  delay(500);
}
