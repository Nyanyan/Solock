const int pushers[8] = {9, 10, 12, 11, 7, 8, 15, 14};
//const int pushers[8] = {9, 10, 11, 12, 15, 14, 7, 8};
char buf[30];
int idx = 0;
long data[4];

void push(int sol0, int sol1, int sol2, int sol3) {
  for (int i = 0; i < 3; i++) {
    if (sol0) {
      digitalWrite(pushers[0], HIGH);
    } else {
      digitalWrite(pushers[4], HIGH);
    }
    if (sol1) {
      digitalWrite(pushers[1], HIGH);
    } else {
      digitalWrite(pushers[5], HIGH);
    }
    if (sol2) {
      digitalWrite(pushers[2], HIGH);
    } else {
      digitalWrite(pushers[6], HIGH);
    }
    if (sol3) {
      digitalWrite(pushers[3], HIGH);
    } else {
      digitalWrite(pushers[7], HIGH);
    }
    delay(50);
    for (int j = 0; j < 8; j++)
      digitalWrite(pushers[j], LOW);
    delay(50);
  }
}

void setup() {
  for (int i = 0; i < 8; i++)
    pinMode(pushers[i], OUTPUT);
  Serial.begin(115200);
  Serial.println("begin");
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
