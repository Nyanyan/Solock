# Solock

A Rubik’s Clock Solving Robot

**日本語は下にあります**

## About

This robot solves a rubik’s clock in under 1 second.

## Files

### basic_functions.py

Functions in this file are used in a lot of other files.

### controller.py

a function in this file sends commands to Arduino and controls robot.

### pusher

This is a program for Arduino. Using this code, an Arduino pushes 8 solenoids and controls pins of clock.

### rotator

This is a program for Arduino. Using this code, an Arduino controls 4 stepper motors and rotate the puzzle.

### detector.py

Using a funtion in this file, the robot can read the puzzle.

### create_array.py

This code must be executed before executing main.py. This code creates csv files

### solver.py

A function in this file finds a solution to a clock.

### XXX.csv

These files are used in solver.py and created by create_array.py

### main.py

main program

### log.txt

log

### legacy

legacy

## 解説

このロボットはルービッククロックという種類のパズルを1秒未満で解きます。

## ファイル

### basic_functions.py

基本関数。様々なファイルで使われる。

### controller.py

Arduinoにコマンドを送り、ロボットを制御する部分。

### pusher

Arduinoのプログラム。8つのソレノイドを制御してパズルのピンを動かす。

### rotator

Arduinoのプログラム。4つのステッピングモーターを動かしてパズルを回す。

### detector.py

パズルの状態を取得する関数。

### create_array.py

このコードはmain.pyの前に実行する必要があり、解法探索に使うcsvファイルを作る。

### solver.py

解法探索を行う。

### XXX.csv

solver.pyで使われるファイルで、create_array.pyによって作られる。

### main.py

メインプログラム

### log.txt

ログ

### legacy

過去の産物

