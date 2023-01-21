# RGB Light

This contains the codes to control a RGB lightstrip using a NodeMCU v3 using blynk 

# Setting up blynk
1) Setup an account with blynk and register a device
2) Retrieve the relevant info and replace the following lines in `rgb.ino`
``` 
#define BLYNK_TEMPLATE_ID "Enter template ID here"
#define BLYNK_DEVICE_NAME "Enter device name here"
#define BLYNK_AUTH_TOKEN "Enter Auth token here"
```
3) Update your wifi credentials as well.
```
char ssid[] = "WIFI SSID";
char pass[] = "WIFI PASSWORD";
```
4) Plug in the following 
* NeoPixel LED t0 PIN 14
* Sound sensor analog pin to PIN 12
* Sound sensor power to PIN 4

