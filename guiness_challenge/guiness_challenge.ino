#include <TimerOne.h>

long strt;
bool flag;
String out;
String former_tmp;
bool tone_hl;
String tmp;

void send_data() {
  out = " ";
  char checksum = 64;
  int l = tmp.length();
  for (int i = 6; i >= 1; i--) {
    out += tmp[l - i];
    checksum += int(tmp[l - i]) - 48;
  }
  out += checksum;
  Serial.print(out);
  Serial.print(char(10));
  Serial.print(char(13));
}

void setup() {
  pinMode(13, OUTPUT);
  pinMode(12, INPUT);
  Serial.begin(1200);
  flag = false;
  tone_hl = false;
  former_tmp = "000000";
  Timer1.initialize(111111);
  Timer1.attachInterrupt(send_data);
  Timer1.start();
}

void loop() {
  if (digitalRead(12)) {
    if (!flag)
      strt = millis();
    flag = !flag;
    tone(13, 440, 300);
    while (digitalRead(12));
  }
  if (flag)
    tmp = "000000" + String(millis() - strt);
  else
    tmp = former_tmp;
  former_tmp = tmp;
}
