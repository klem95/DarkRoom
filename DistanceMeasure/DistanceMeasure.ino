const int trigPin = 7;
const int echoPin = 3;

void setup() {

  Serial.begin (9600);

  // Configure the pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Trigger set to low
  digitalWrite(trigPin, LOW);
}

void loop() {

  long duration, distance;
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration / 58;

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
