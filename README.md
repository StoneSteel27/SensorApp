Sensor-App
==========

**This cross-platform app was generated by** `Briefcase` **part of**
`The BeeWare Project`.

A Sensor Data Displaying/Streaming Android App built with Beeware tools.

## Features
- Real-Time Display of Sensor Data
- Fast Real-Time Sensor Data Streaming via TCP Sockets

## Data Stream Setup
- This Repository contains `sensor-server.py` python file which provides a simple way for creating the Server.
- The Communication between the App and the Server will happen on port-`5678`.
- Start the server using:
```bash
$ python sensor-server.py
```
- Obtain your server's local IP address and enter in the App to Start the Data Stream.

## App's Preview
<img src="https://raw.githubusercontent.com/StoneSteel27/SensorApp/main/pictures/App-UI.jpeg" width="300">

## Building From Source
- First, Clone the Repo
```bash
$ git clone https://github.com/StoneSteel27/SensorApp
$ cd SensorApp
```
- Install `Briefcase`
```bash
$ pip install briefcase
```
- Start the Building Process with:
```bash
$ briefcase build android
```
- Finally, the last line of build process, will contain the path to the `apk` file

## Background
- Sensor-App was created to aid Computer Programmers, Data Scientists with Real-Time Sensor Data, for various applications like VR and AR.
- It was also made as a Introductory Project of using Tools of `Beeware`.
