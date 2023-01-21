#define BLYNK_PRINT Serial

#define BLYNK_TEMPLATE_ID "Enter template ID here"
#define BLYNK_DEVICE_NAME "Enter device name here"
#define BLYNK_AUTH_TOKEN "Enter Auth token here"

//define NeoPixel Pin and Number of LEDs
#define PIN 14
#define NUM_LEDS 90

//define the power for sound sensor
#define SOUNDPOWER 4

// define mode
#define NORMAL_LIGHT 1
#define SOUND_REACTIVE 2

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <Adafruit_NeoPixel.h>

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "WIFI SSID";
char pass[] = "WIFI PASSWORD";
char auth[] = BLYNK_AUTH_TOKEN;

//create a NeoPixel strip
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

// initialize rgb, brightness and mode
int red = 255;
int green = 255;
int blue = 255;
int brightness = 255;
bool isOff = true;
int lightMode = NORMAL_LIGHT;

BlynkTimer timer;

void setup()
{
  Serial.begin(9600);
  
  // Setup strip
  strip.begin();
  strip.setPixelColor(1  , strip.Color(106, 90, 205)); 
  strip.show();

  // Declare pin to power sound sensor
  pinMode(SOUNDPOWER, OUTPUT);
    
  Blynk.begin(auth, ssid, pass);

  timer.setInterval(200L, displayRGB);
}

void loop()
{ 
  Blynk.run();
  timer.run();
}

// on/off
BLYNK_WRITE(V0)
{
  isOff = param.asInt() == 0;
}

// Red
BLYNK_WRITE(V1)
{
  red = param.asInt();
}

// Green
BLYNK_WRITE(V2)
{
  green = param.asInt();
}

// Blue
BLYNK_WRITE(V3)
{
  blue = param.asInt();
}

// Mode
BLYNK_WRITE(V4)
{
  if (param.asInt() == 0) {
    lightMode = NORMAL_LIGHT;
  } else {
    lightMode = SOUND_REACTIVE;
  }
}

// Brightness
BLYNK_WRITE(V5)
{
  brightness = param.asInt();
}


// Check the mode to run
void displayRGB()
{
  if (isOff) {
    offMode();
    return;
  }
  
  switch (lightMode) 
  {
    case NORMAL_LIGHT:
      rgbMode();
      break;
    case SOUND_REACTIVE:
      soundMode();
      break;
  }
}


//set entire strip to same color
static void showColor(uint32_t c) {
  for(uint16_t i=0; i < strip.numPixels() + 4; i++) {
    strip.setPixelColor(i  , c); // Draw new pixel
  }
  strip.show();
}

// OFF mode
static void offMode() {
  digitalWrite(SOUNDPOWER, LOW);
  strip.setBrightness(0);

  showColor(strip.Color(0, 0, 0));
}


// RGB mode
static void rgbMode() {
  digitalWrite(SOUNDPOWER, LOW);
  strip.setBrightness(brightness);
  
  showColor(strip.Color(red, green, blue));
}

// Sound mode
static void soundMode() {
  digitalWrite(SOUNDPOWER, HIGH);
  strip.setBrightness(brightness);
  
  int red = map(analogRead(12), 0, 1023, 0, 255);
  delay(5);
  int green = map(analogRead(12), 0, 1023, 0, 255);
  delay(5);
  int blue = map(analogRead(12), 0, 1023, 0, 255);
  delay(5);
  showColor(strip.Color(red, green, blue));
  delay(100);
}
