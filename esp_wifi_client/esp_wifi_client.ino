#include <WiFi.h>
#include "esp_camera.h"

//Camera Pins Defined
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// WiFi network name and password 
const char * ssid = "aswinSreekumar";
const char * pwd = "aswinsree";

//Local IP Address of Server and Port
const char * udpAddress = "192.168.161.37";
const int udpPort = 12345;

bool initCamera()
{
  // camera configuration
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG; 
  config.frame_size = FRAMESIZE_SVGA;
  config.jpeg_quality = 10;
  config.fb_count = 1;
    
  esp_err_t result = esp_camera_init(&config);

  //Check if camera is initialsed
  if (result != ESP_OK) 
  return false;
  return true;
}



void setup(){
  Serial.begin(115200);

  if(!initCamera())
  { 
    Serial.printf("Failed to initialize camera...");
    return;  
  }
  
  //Connect to the WiFi network
  WiFi.begin(ssid, pwd);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  delay(1000);
  
}

void loop()
{
  //declare WiFi client object
  WiFiClient client;
  client.connect(udpAddress,udpPort);

  //decalare a pointer to struct of type camera_fb_t which has pixel data , length and width of the image
  camera_fb_t * frame = NULL;
  frame = esp_camera_fb_get();
    
  //transfer pixel data
  client.write((const uint8_t *)frame->buf, frame->len);
  
  Serial.println(frame->len);
  Serial.println(frame->width);
  Serial.println(frame->height);

  //reuse frame
  esp_camera_fb_return(frame);

  //stop transaction
  client.stop();
  
  delay(2000);
}
