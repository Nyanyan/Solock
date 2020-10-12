const int magnet_threshold = 50;
const long turn_steps = 800;
const int step_dir[4] = {9, 14, 11, 7};
const int step_pul[4] = {10, 15, 12, 8};
//const int step_dir[4] = {11, 9, 14, 7};
//const int step_pul[4] = {12, 10, 15, 8};

char buf[30];
int idx = 0;
long data[7];

void move_motor(long spd, long deg1, long deg2, int motor0, int motor1, int motor2, int motor3) {
  bool hl1 = true;
  bool hl2 = true;
  if (deg1 < 0) hl1 = false;
  if (deg2 < 0) hl2 = false;
  if (deg1) {
    if (motor0) digitalWrite(step_dir[0], hl1);
    if (motor1) digitalWrite(step_dir[1], hl1);
    if (motor2) digitalWrite(step_dir[2], hl1);
    if (motor3) digitalWrite(step_dir[3], hl1);
  }
  if (deg2) {
    if (!motor0) digitalWrite(step_dir[0], hl2);
    if (!motor1) digitalWrite(step_dir[1], hl2);
    if (!motor2) digitalWrite(step_dir[2], hl2);
    if (!motor3) digitalWrite(step_dir[3], hl2);
  }
  long steps1 = abs(deg1) * turn_steps / 360;
  long steps2 = abs(deg2) * turn_steps / 360;
  long avg_time = 1000000 * 60 / turn_steps / spd;
  bool motor_hl = false;
  for (int i = 0; i < max(steps1, steps2); i++) {
    motor_hl = !motor_hl;
    if (i < steps1) {
      if (motor0) digitalWrite(step_pul[0], motor_hl);
      if (motor1) digitalWrite(step_pul[1], motor_hl);
      if (motor2) digitalWrite(step_pul[2], motor_hl);
      if (motor3) digitalWrite(step_pul[3], motor_hl);
    }
    if (i < steps2) {
      if (!motor0) digitalWrite(step_pul[0], motor_hl);
      if (!motor1) digitalWrite(step_pul[1], motor_hl);
      if (!motor2) digitalWrite(step_pul[2], motor_hl);
      if (!motor3) digitalWrite(step_pul[3], motor_hl);
    }
    delayMicroseconds(avg_time);
  }
  /*
    long max_time = 1500;
    long slope = 50;
    bool motor_hl = false;
    long accel = min(steps / 2, max(0, (max_time - avg_time) / slope));
    for (int i = 0; i < accel; i++) {
    motor_hl = !motor_hl;
    if (motor0) digitalWrite(step_pul[0], motor_hl);
    if (motor1) digitalWrite(step_pul[1], motor_hl);
    if (motor2) digitalWrite(step_pul[2], motor_hl);
    if (motor3) digitalWrite(step_pul[3], motor_hl);
    delayMicroseconds(max_time - slope * i);
    }
    for (int i = 0; i < steps * 2 - accel * 2; i++) {
    motor_hl = !motor_hl;
    if (motor0) digitalWrite(step_pul[0], motor_hl);
    if (motor1) digitalWrite(step_pul[1], motor_hl);
    if (motor2) digitalWrite(step_pul[2], motor_hl);
    if (motor3) digitalWrite(step_pul[3], motor_hl);
    delayMicroseconds(avg_time);
    }
    for (int i = 0; i < accel; i++) {
    motor_hl = !motor_hl;
    if (motor0) digitalWrite(step_pul[0], motor_hl);
    if (motor1) digitalWrite(step_pul[1], motor_hl);
    if (motor2) digitalWrite(step_pul[2], motor_hl);
    if (motor3) digitalWrite(step_pul[3], motor_hl);
    delayMicroseconds(max_time - slope * accel + accel * (i + 1));
    }
  */
}

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(step_dir[i], OUTPUT);
    pinMode(step_pul[i], OUTPUT);
  }
  Serial.begin(115200);
}

void loop() {
  while (1) {
    if (Serial.available()) {
      buf[idx] = Serial.read();
      if (buf[idx] == '\n') {
        buf[idx] = '\0';
        data[0] = atoi(strtok(buf, " "));
        for (int i = 1; i < 7; i++)
          data[i] = atoi(strtok(NULL, " "));
        move_motor(data[0], data[1], data[2], data[3], data[4], data[5], data[6]);
        idx = 0;
      }
      else {
        idx++;
      }
    }
  }
}
