# Smart Parking System
Vision based Smart Parking system using ESP32-CAMs, Raspberry Pi and cloud deployed NodeJS web-server. 

### Designed and Developed by
- [Kailash Hari](https://github.com/kailashhari)
- [Satish Kumar L](https://github.com/Satish-Kumar-L)
- [Greeshwar R S](https://github.com/greesh02)
- [Aswin Sreekumar](https://github.com/aswin-sreekumar)

### Contents
- [Problem statement](#Problem-statement)
- [Solution proposed](#Solution-proposed)
- [Segments involved](#Segments-involved)
- [Technical stack](#Technical-stack)
- [Technical explanation](#Technical-explanation)
- [Flowchart of system](#Flowchart-of-system)
- [Gallery](#Gallery)

## Problem statement
- Parking has always been an issue in metropolitan cities.  Let it be a shop or a public place, parking wastes time, fuel and sometimes breaks sweat to get it done.
- Drivers tend to circle around the place searching for parking spots. This increases traffic congestions, wastes fuel and increases pollution. It escalates to a risky scale during festival times.
- Unable to find proper parking spots, some vehicles are parked in narrow spaces causing traffic jams.

## Solution proposed
- The project proposes to install low cost camera modules in multiple parking lots across the city, which streams live image to the corresponding remote server 
- The remote server processes the data from the camera module and decides on the number of vacant parking spaces available in the parking lot
- The remote server updates the number of vacant parking slots and number of filled parking slots in a cloud database
- The number of vacant parking slots and their location is displayed in a web application accessible to general public and free to use.
- The database is updated continuously , ensuring a pristine user experience

## Segments involved
- Decentralized server (Raspberry Pi) for image processing, computation and network management.
- ESP32-CAM hardware setup for wireless image transmission and reception by server.
- Object detection and updation of database
- Cloud Deployed and completely scalable Website and Cloud Database management.

## Technical stack
- Processing server
  - Raspberry Pi 4B 
  - Raspbian 32-bit OS
  - SSH access - PuTTy, FileZilla
  - Auto run on boot-up
  - TCP Sockets
  - PIL Library
- ESP32-CAM setup
  - Arduino IDE
  - ESP32 board 
  - socket library
  - TCP Protocol
- Website
  - Node.js(Express)
  - HTML5/CSS3
  - MongoDB
  - Google Maps API services
- Object detection and updation
  - Python
  - OpenCV library
  - pyMongo library
  - Numpy library
  - OS module

## Technical explanation
### The Website
- The website is a scalable, cloud deployed, responsive web application accessible to general public and free to use.
- Depending on the functionality desired, the user can either search for parking lots near their current location(Mode 1) or a desired destination(Mode 2).
- The application uses geolocation technology to find the device location and prints out an interactive map with the 10 closest parking lots and the availability.
- The user can click on the parking slot in the map which links to google maps for directions to that parking lot from the user location(in Mode 1) or from the destination(in Mode 2)
- It uses Node Js as the back end environment and Express as the server technology. 

### ESPCAM setup
- ESP32 CAM is used to take pictures in regular intervals and transmit it to a remote server which is in the same WiFi network.
- Camera pins are defined , camera settings are configured and is initialised.
- ESP32 cam connects to LAN.
- ESP32 cam establishes connection with remote server.
- A frame is captured from the camera and stored in a camera_fb_t pointer , which holds the pixel data , height , width of the image.
- Pixel data is transmitted to the server through TCP protocol.
- Since the size of pixel data exceeds the size limit of single TCP socket, pixel data is broken up into chunks and sent individually.
- The process repeats for every two seconds approximately.

### The Server
- Raspberry Pi 4B is used as local server for image reception, processing, slot computation and updation to cloud.
- PuTTy is used to connect wirelessly to the Pi over SSH and FileZilla was used to transfer the file over SFTP. 
- The ESP32 image reception and object detection python scripts run on boot-up. This was implemented by modifying the .bashrc script to execute the python scripts on boot-up or when a terminal is launched.
- The ESP32 script receives pixel data of the image as a chunk of bytes. It is stored in a byte array and is converted into a JPEG image using Pillow library. 
- The script then stores each image under proper naming convention (ESP_XX_CHN_X_time) and stores in the respective directory
- The Pi is connected to the same local network as the ESP32 CAMs through WiFi. internet is also enabled to perform updation to the cloud.

### Object detection and computation
- It processes the Images obtained from parking lots one after the other and identifies the bounding boxes of the objects (cars and bikes) utilizing a pretrained model(MobileNet SSD model) in OpenCV DNN module.
- Based on Intersection Over Union calculation between the predicted bounding boxes and manually drawn bounding boxes representing parking areas Occupancy of respective parking lots gets updated in the server.
- After processing, the image gets deleted automatically to avoid reprocessing.


## Flowchart of system
![Romain-flowchart](https://user-images.githubusercontent.com/63254914/145010041-10b53ae5-b5e7-4cda-89e6-7fe81f6e233d.png)

## Gallery
### ESPCAM module
![cam_1_cropped](https://user-images.githubusercontent.com/63254914/145010285-d185392d-0e51-41ad-ac15-070f8f7f719d.jpg)

### Object detection


### Website




