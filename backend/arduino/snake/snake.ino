#include <TM1638plus.h>
#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978
// 定义TM1638连接的引脚
#define STB_PIN A2
#define CLK_PIN A1
#define DIO_PIN A0

// 定义HW-504摇杆的引脚
#define VRX_PIN A3
#define VRY_PIN A4
#define SW_PIN 2

// 定义蜂鸣器的引脚
#define BUZZER_PIN 9

// 创建TM1638对象
TM1638plus module(STB_PIN,CLK_PIN, DIO_PIN, false);

// 定义变量
int displayValue = 0;
bool isPlayingMusic = false;
char lastDirection = 'U';

// 定义《欢乐颂》的音符和节拍
int melody[] = 
{
  NOTE_E4, NOTE_E4, NOTE_F4, NOTE_G4, NOTE_G4, NOTE_F4, NOTE_E4, NOTE_D4, NOTE_C4, NOTE_C4, NOTE_D4, NOTE_E4, NOTE_E4, NOTE_D4, NOTE_D4,
  NOTE_E4, NOTE_E4, NOTE_F4, NOTE_G4, NOTE_G4, NOTE_F4, NOTE_E4, NOTE_D4, NOTE_C4, NOTE_C4, NOTE_D4, NOTE_E4, NOTE_D4, NOTE_C4, NOTE_C4
};

int noteDurations[] = {
  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
};

void setup() {
  // 初始化串口通信
  Serial.begin(115200);

  // 设置摇杆的引脚模式
  pinMode(VRX_PIN, INPUT);
  pinMode(VRY_PIN, INPUT);
  pinMode(SW_PIN, INPUT_PULLUP);

  // 设置蜂鸣器的引脚模式
  pinMode(BUZZER_PIN, OUTPUT);

  // 初始化TM1638显示屏
  module.displayBegin();
  module.displayIntNum(displayValue, false);
}

void loop() {
  // 检查是否有来自Python程序的输入
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'A') {
      // 增加TM1638显示屏的读数
      displayValue++;
      module.displayIntNum(displayValue, false);
    } else if (command == 'B') {
      // 切换蜂鸣器播放状态
      isPlayingMusic = !isPlayingMusic;
      if (isPlayingMusic) {
        playBackgroundMusic();
      } else {
        stopBackgroundMusic();
      }
    }
  }

  // 读取摇杆状态并发送给Python程序
  char joystickDirection = readJoystickDirection();
  if (joystickDirection != 'S') {
    if (joystickDirection != lastDirection) {
      Serial.println(joystickDirection);
      lastDirection = joystickDirection;
    }
  } else {
    Serial.println("N");
    delay(10);
  }

  // 如果正在播放音乐，继续播放
  if (isPlayingMusic) {
    playBackgroundMusic();
  }
}

char readJoystickDirection() {
  int xValue = analogRead(VRX_PIN);
  int yValue = analogRead(VRY_PIN);

  if (yValue < 300) {
    return 'U';  // 上
  } else if (yValue > 700) {
    return 'D';  // 下
  } else if (xValue < 300) {
    return 'L';  // 左
  } else if (xValue > 700) {
    return 'R';  // 右
  }

  return 'S';
}

void playBackgroundMusic() {
  static int currentNote = 0;
  static unsigned long previousMillis = 0;
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= 1000 / noteDurations[currentNote]) {
    previousMillis = currentMillis;
    tone(BUZZER_PIN, melody[currentNote], 1000 / noteDurations[currentNote]);
    currentNote++;
    if (currentNote >= sizeof(melody) / sizeof(melody[0])) {
      currentNote = 0;
    }
  }
}

void stopBackgroundMusic() {
  noTone(BUZZER_PIN);  // 停止播放音乐
}