//#include <SoftwareSerial.h>
#include <TimerOne.h>

//SoftwareSerial mySerial(10, 11);
long strt;
bool flag;
String out;
String former_tmp;
bool tone_hl;

void send_data() {
  out = " ";
  String tmp;
  if (flag)
    tmp = "000000" + String(millis() - strt);
  else
    tmp = former_tmp;
  former_tmp = tmp;
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
  //mySerial.begin(9600);
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
    delay(100);
  }
}
