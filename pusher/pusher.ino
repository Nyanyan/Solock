const int pushers[8] = {7, 8, 9, 10, 11, 12, 14, 15};
char buf[30];
int idx = 0;
long data[4];

void push(int sol0, int sol1, int sol2, int sol3) {
  if (sol0)digitalWrite(pushers[0], HIGH);
  if (sol1)digitalWrite(pushers[1], HIGH);
  if (sol2)digitalWrite(pushers[2], HIGH);
  if (sol3)digitalWrite(pushers[3], HIGH);
  delay(100);
  for (int i = 0; i < 4; i++)
    digitalWrite(pushers[i], LOW);
}

void setup() {
  for (int i = 0; i < 4; i++)
    pinMode(pushers[i], OUTPUT);
}

void loop() {
  while (1) {
    if (Serial.available()) {
      buf[idx] = Serial.read();
      if (buf[idx] == '\n') {
        buf[idx] = '\0';
        data[0] = atoi(strtok(buf, " "));
        for (int i = 1; i < 4; i++)
          data[i] = atoi(strtok(NULL, " "));
        push(data[0], data[1], data[2], data[3]);
        idx = 0;
      }
      else {
        idx++;
      }
    }
  }
}
