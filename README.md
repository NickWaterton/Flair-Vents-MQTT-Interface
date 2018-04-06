Flair Vents MQTT Interface
==========================

Interface to flair Smart vents and pucks via MQTT

This is version 1.0 so it may be buggy!
**NOTE: This is a python 2.7 program**
If you want to use it with python 3.xx some work will need to be done.

## Introduction
This program has the following features
* Read all Flair vents values
* Read all flair puck values
* read historical data for vents/pucks
* publish the above to the topic and MQTT broker of your choice
* set vent % open
* Set puck values (room occupied, set_point_c, clear hold) are built in, others could be added
* set up for openhab2 interface by default
* auto timezone correction of time/dates
* optionally save values in config file

The set values are updated by publishing the value to eg `topic/flair/command/puck/name/occupied ON` (or OFF) where topic is the topic you have selected, name is the name of the puck. See *Usage* below

## Pre-Requisites
To use this program, you will need to have requested access to the Flair API (email hello@flair.co) you will get:

* CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
* CLIENT_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

You then need to enter these on the command line.
You will also need to know your house_id - this is a number (usually 4 digits) identifying your house.
In the Flair web page showing your devices, it's usually the number at the end of the URL.
eg https://my.flair.co/h/1234 where 1234 is your house id.

## Dependencies
The Flair python API client module is required. You can install it by following the instructions here:
https://github.com/flair-systems/flair-api-client-py
This works with Python 2.7 (despite what it says).

you will also need the paho-mqtt python library, you can get it by following the instructions here: https://www.eclipse.org/paho/clients/python/

## Install
First you need python 2.7 installed. **This program will not work with Python 3.x without some work**
Make sure you have the Flair API-Client installed
Make sure you have paho-mqtt installed

now clone it from GitHub
```bash
git clone git clone https://github.com/NickWaterton/Flair-Vents-MQTT-Interface.git
cd Flair-Vents-MQTT-Interface
```
You should now have the program `vents_bridge.py` - make sure the file is executable

No need to install anything, you can just run the program as is.

run `./vents_bridge.py -h` (or `python vents_bridge.py -h` if you are on windows)

```
usage: vents_bridge.py [-h] [-id HOUSE_ID] [-cid CLIENT_ID]
                       [-cs CLIENT_SECRET] [-n COUNT] [-t T] [-b BROKER]
                       [-p PORT] [-u USER] [-pw PASSWORD] [-m TOPIC] [-l LOG]
                       [-C] [-D] [-V]

Read Flair Smart Vents/Pucks Values and Sensors, publish via MQTT

optional arguments:
  -h, --help            show this help message and exit
  -id HOUSE_ID, --house_id HOUSE_ID
                        flair house id (default=None)
  -cid CLIENT_ID, --client_id CLIENT_ID
                        flair API CLIENT ID (default=None)
  -cs CLIENT_SECRET, --client_secret CLIENT_SECRET
                        flair API CLIENT SECRET (default=None)
  -n COUNT              Number of times to loop data, 0=forever
  -t T                  time between polling default=60s
  -b BROKER, --broker BROKER
                        mqtt broker to publish sensor data to.
                        (default=127.0.0.1)
  -p PORT, --port PORT  mqtt broker port (default=1883)
  -u USER, --user USER  mqtt broker username. (default=none)
  -pw PASSWORD, --password PASSWORD
                        mqtt broker password. (default=None)
  -m TOPIC, --topic TOPIC
                        topic to publish sensor data to.
                        (default=openhab/sensors)
  -l LOG, --log LOG     main log file. (default=~/Scripts/flair_vents.log)
  -C, --config          use config File
  -D, --debug           debug mode
  -V, --version         show program's version number and exit

```

## Quick Start
With your house_id, API CLIENT_ID and API CLIENT_SECRET in hand, enter
```bash
./vents_bridge.py -id house_id -cid CLIENT_ID -cs CLIENT_SECRET -l flair_vents.log
```

If your MQTT broker is on a different host, or port, or you have an mqtt username and password configured, you will have to enter them also.
Otherwise the default is for the broker to be on the same machine, with the default port and no username or password configured.

You should see something like this:
```
****** Program Started ********
Authenticating
Subscribed: 1 (0,)
Authenticated for 3600s
Authentication expires in: 3599s
got data for 7 vents
Vent: Nick's Office-5384, Latest Reading: {
  "Pressure": 98.58,
  "RSSI": -75,
  "Temperature": 21.78,
  "bat_percent": "100",
  "battery": 3.26,
  "date": "2018-04-06T11:57:00.321765-04:00",
  "online": true,
  "percent_open": 0,
  "set_by": "Algo"
}
Vent: Hallway-9e65, Latest Reading: {
  "Pressure": 98.55,
  "RSSI": -82,
  "Temperature": 23.07,
  "bat_percent": "100",
  "battery": 3.49,
  "date": "2018-04-06T11:57:00.304557-04:00",
  "online": true,
  "percent_open": 99,
  "set_by": "Algo"
}
```

This will refresh every 60 seconds (default), and will publish the values to the mqtt topic `openhab/sensors`. Details will be logged to `./flair_vents.log`.
Times are in ISO format, and from the flair API are in UTC time. These are automatically converted to local time using the timezone set on your computer, the offset from UTC is given (depending on your local timezone).
If you want UTC, you are welcome to fiddle with the program, timezones are a pain! I have no idea if the DST correction is right or not.

If you see errors like this:

```bash
404
{u'errors': [{u'status': u'404', u'detail': u'Could not find structures', u'title': u'Not Found'}]}
ApiError<HTTP Response: 404>
```
Then you have something wrong, house_id, CLIENT_ID or CLIENT_SECRET. Check again...

## Usage
Here are the command line options explained
### ID
This is the flair house_id, usually a 4 digit number identifying your house, you can see it at the end of the flair URL when you log in to your flair web page: eg `https://my.flair.co/h/1234` where 1234 is your house id.
This is a required entry, the program will not work without it.
### CLIENT_ID
This is the CLIENT_ID you obtained from Flair by requesting access to the API via hello@flair.co. It is required. you can enter it on the command line.
### CLIENT_SECRET
This is the CLIENT_SECRET you obtained from Flair by requesting access to the API via hello@flair.co. It is required. you can enter it on the command line.
### COUNT
Number of times to loop data, 0=forever
### T
Time in seconds between polling default=60s. I don't reccomend setting this to less than 60 seconds, as that's how often the pucks/vents update anyway.
### BROKER
MQTT broker ip address or domain name. Default is 127.0.0.1 which is the local loopback address, 'localhost' or '' also means the current machine.
### PORT
MQTT broker port number (default 1883) enter your MQTT broker port here if it is different from the default (eg 8883 for secure MQTT access)
### USER
MQTT broker username. This is configured on the broker, and may not be used. If not used leave as is (None) and no authentication will be used
### PASSWORD
MQTT broker password, to be used un conjunction with the username. If not used leave as is (None) and no authentication will be used
### TOPIC
MQTT topic to publish data to. this is the stub, the data will be published to the `stub/type/name/value_name` where type is `puck` or `vent`, name is the device name, and `value_name` is `percent_open` and so on. This is also the stub for sending command to the vents/pucks. you publish a command to `stub/flair/command/type/name/value_name` to update a setting.
Current supported items that can be updated:
* occupied
* set_temp
* set_point_manual
* percent_open

You publish to the vent or puck in question (or in the case of a puck, the room).

For example, publishing to the default topic `openhab/sensors`, here is some output:
```
****** Program Started ********
Authenticating
Subscribed: 1 (0,)
Authenticated for 3600s
Authentication expires in: 3599s
got data for 7 vents
Vent: Nick's Office-5384, Latest Reading: {
  "Pressure": 98.58,
  "RSSI": -75,
  "Temperature": 21.78,
  "bat_percent": "100",
  "battery": 3.26,
  "date": "2018-04-06T11:57:00.321765-04:00",
  "online": true,
  "percent_open": 0,
  "set_by": "Algo"
}
...
Puck: Family Room-97b2, Latest Reading: {
  "Humidity": 44.0,
  "Pressure": 98.36,
  "RSSI": -67,
  "Temperature": 21.5,
  "active": true,
  "bat_percent": "95",
  "battery": 2.97,
  "date": "2018-04-06T16:25:02.734683-04:00",
  "hold_reason": null,
  "hold_until": null,
  "light": 41,
  "occupied": true,
  "online": true,
  "room_name": "Family Room",
  "set_by": "Algo",
  "set_point_c": 22.0,
  "set_point_manual": false,
  "set_temp": 22.0
}
```

This is published to:
```
openhab/sensors/flair/vent/Nick's Office-5384/LastUpdate Fri Apr  6 16:26:24 2018
openhab/sensors/flair/vent/Nick's Office-5384/Pressure 98.41
openhab/sensors/flair/vent/Nick's Office-5384/set_by Algo
openhab/sensors/flair/vent/Nick's Office-5384/bat_percent 100
openhab/sensors/flair/vent/Nick's Office-5384/Temperature 38.23
openhab/sensors/flair/vent/Nick's Office-5384/online True
openhab/sensors/flair/vent/Nick's Office-5384/date 2018-04-06T16:25:51.552208-04:00
openhab/sensors/flair/vent/Nick's Office-5384/RSSI -74
openhab/sensors/flair/vent/Nick's Office-5384/percent_open 0
openhab/sensors/flair/vent/Nick's Office-5384/battery 3.26
....
openhab/sensors/flair/puck/Family Room-97b2/LastUpdate Fri Apr  6 16:25:22 2018
openhab/sensors/flair/puck/Family Room-97b2/set_by Algo
openhab/sensors/flair/puck/Family Room-97b2/bat_percent 95
openhab/sensors/flair/puck/Family Room-97b2/Temperature 21.5
openhab/sensors/flair/puck/Family Room-97b2/battery 2.97
openhab/sensors/flair/puck/Family Room-97b2/light 41
openhab/sensors/flair/puck/Family Room-97b2/set_point_c 22.0
openhab/sensors/flair/puck/Family Room-97b2/online True
openhab/sensors/flair/puck/Family Room-97b2/room_name Family Room
openhab/sensors/flair/puck/Family Room-97b2/set_point_manual False
openhab/sensors/flair/puck/Family Room-97b2/Humidity 44.0
openhab/sensors/flair/puck/Family Room-97b2/Pressure 98.36
openhab/sensors/flair/puck/Family Room-97b2/occupied True
openhab/sensors/flair/puck/Family Room-97b2/date 2018-04-06T16:25:02.734683-04:00
openhab/sensors/flair/puck/Family Room-97b2/RSSI -67
openhab/sensors/flair/puck/Family Room-97b2/active True
openhab/sensors/flair/puck/Family Room-97b2/set_temp 22.0
```
The `date` is the date/time of the reading (ie when the puck/vent reported the value) converted to a local time, the `LastUpdate` is the date/time that it was published (in text, not ISO format), also a local time.
To update the Office vent to 100% open, you would publish the following:
```
openhab/sensors/flair/command/vent/Nick's Office-5384/percent_open 100
```
On an Ubuntu 14.04 system using `mosquitto-clients`
Enter:
```bash
mosquitto_pub -t "openhab/sensors/flair/command/vent/Nick's Office-5384/percent_open" -m 100
```
if your broker is on a different host/port, you will have to specify using `-h host` and `-p port` also optional username and password.
This isn't an MQTT tutorial, I'm assuming you are familiar with MQTT or you wouldn't want to be using this...

If you update the set_point temperature (in this case in degrees C), this creates a hold.
```
openhab/sensors/flair/command/puck/Family Room-97b2/set_temp 22.5
```

To cancel a hold on a room temperature, publish:
```
openhab/sensors/flair/command/puck/Family Room-97b2/set_point_manual false
```
You can actually publish anything you want to this topic, it's the act of publishing to it that cancels the hold, not what you send.

You will notice there is some confusion between Pucks and Rooms, most items are read from pucks, but only Rooms (not pucks) can be updated. It's a bit confusing, but if you only have one puck per room. it's not a problem. So if you have two pucks in one room, and you update the `occupied` setting for one puck, then the Room actually gets updated, so both pucks for the room will show `inactive`. Same for `set_temp`.
Vents are much simpler, you just update the `percent-open` per vent.
### LOG
pathname of the log file (default=~/Scripts/flair_vents.log). if you enter `None` for the log file pathname, then no logging is performed.
### D
Debug mode - just gives more messages
### C
Use configuration file.
entering all this stuff on the command line every time is a PITA, so if you include -C on the command line, all the settings will be saved to a configuration file called `config.ini`
now if you start the program and just use -C as the argument, like this:
```bash
./vents_bridge.py -C -l flair_vents.log
```
Then all the values will be read from the config file. Notice the log file pathname is not stored, you still have to specify that.
Now you can edit these values in the config file (it's just a text file), or if you run the command line with an updated value, the config.ini file will be updated with the new value.
like this:
```bash
./vents_bridge.py -id 4321 -C -l flair_vents.log
```
Here the house_id would be updated from 1234 to 4321 (or whatever).

## Security
**Do NOT share your house_id, CLIENT_ID or CLIENT_SECRET** This includes the **confing.ini** file. This seems obvious, but it will give anyone access to your home settings if you do.
Likewise, **Do NOT share your MQTT broker ip, port, username or password** as it will also give anyone access to your home settings.

## OpenHab
I have some custom icons (vent32 for example) so you will have to invent your own icons for vents, I have also customised `switch.map`. Items that are charted need to be in persistence also.
This is just for one vent, puck etc. you will need to customise this for however many vents/pucks you have and their unique names. For instance, you won't have a vent called `Master Bedroom-d7df` you have to substitute whatever your vent is called (as shown by the program).
In this case `Proliant` is my MQTT server as defined for OpenHab.
I'm using OpenHab 2.2 (a SNAPSHOT build) but it should work on any version of OH2. No doubt OH2.3 (or whatever) will break everything again, but I'll update here if it does.
Here are my example items, rules and sitemap for vent control:
### Items
```
/* Flair Vents and Pucks */
Group flairnetwork "Flair Network"  <network> (Sensors)
Group Flair_Temperature "Flair Temperature"  <temperature>   (gCharts)
Group Flair_Vent_Temperature "Flair Vent Temperature"  <temperature>   (Flair_Temperature)
Group Flair_Puck_Temperature "Flair Room Temperature"  <temperature>   (Flair_Temperature)
Group Flair_Humidity "Flair Humidity"  <humidity>   (gCharts)
Group Flair_Pressure "Flair Pressure"  <pressure>   (gCharts)
Group Flair_Vent_Pressure "Flair Vent Pressure"  <pressure>   (gCharts)
Group Flair_Light "Flair Light"  <sun>   (gCharts)
Group Flair_Open "Flair open"  <vent32>   (gCharts)
Group Flair_Volts "Flair Voltages"  <battery>   (gCharts)
Group Flair_Battery "Flair Battery" <battery>  (gCharts)
Group Flair_Volts_Mains "Flair Voltages (mains)"  <battery>   (gCharts)
Group Flair_Battery_Mains "Flair Battery (mains)" <battery>  (gCharts)
String flairLastUpdate "Last Update [%s]" <clock>  (flairnetwork)   {mqtt="<[proliant:openhab/sensors/flair/LastUpdate:state:default]"}
/* Flair Vents */
Group flairvents "Flair Vents"  <network> (flairnetwork)

//Vents
/* 1 is Master Bedroom-d7df */
Switch flairvent1Online "FV1(MB) online [%s]" <network> (flairvents) {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/online:state:MAP(switch.map)]"}
Number flairvent1Temp "FV1(MB) Duct Temp [%.2f °C]" <temperature>  (flairvents, Flair_Vent_Temperature, Flair_Temperature)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/Temperature:state:default]"}
//Number flairvent1Humidity "FV1(MB) Duct Humidity [%.2f%%]" <humidity>  (flairvents, Flair_Humidity)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/Humidity:state:default]"}
Number flairvent1Pressure "FV1(MB) Duct Pressure [%.2fkPa]" <pressure>  (flairvents, Flair_Pressure)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/Pressure:state:default]"}
//Dummy item Set By rule, difference between room and vent pressure
Number flairvent1Pressure_diff "FV1(MB) Duct Pressure Diff [%.2fPa]" <pressure>  (flairvents, Flair_Vent_Pressure)
Dimmer flairvent1Open "FV1(MB) Vent [%d%%]" <vent32>  (flairvents, Flair_Open)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/percent_open:state:default],>[proliant:openhab/sensors/flair/command/vent/Master Bedroom-d7df/percent_open:command:*:${command}]"}
Number flairvent1BatteryVolt "FV1(MB) Battery Voltage [%.2f V]" <batteryfull>  (flairvents, Flair_Volts)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/battery:state:default]"}
Number flairvent1Battery "FV1(MB) Battery [%d%%]" <battery>  (flairvents, Battery, Flair_Battery)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/bat_percent:state:default]"}
DateTime flairvent1Date "FV1(MB) Last Reading [%1$ta %1$tR]" <clock>  (flairvents)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/date:state:default]"}
Number flairvent1Rssi "FV1(MB) RSSI [%d dBm]" <network>  (flairvents)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/RSSI:state:default]"}
String flairvent1Set_By "FV1(MB) Set By [%s]" <msg>  (flairvents)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/set_by:state:default]"}
String flairvent1LastUpdate "FV2(MB) Last Update [%s]" <clock>  (flairvents)   {mqtt="<[proliant:openhab/sensors/flair/vent/Master Bedroom-d7df/LastUpdate:state:default]"}

//Pucks
/* 1 is Master Bedroom-0b07 */
Switch flairpuck1Online "FP1(MB) online [%s]" <network> (flairpucks) {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/online:state:MAP(switch.map)]"}
Switch flairpuck1Occupied "FP1(MB) Occupied [%s]" <parents> (flairpucks) {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/occupied:state:MAP(switch.map)],>[proliant:openhab/sensors/flair/command/puck/Master Bedroom-0b07/occupied:command:*:${command}]"}
Number flairpuck1Temp "FP1(MB) Room Temp [%.2f °C]" <temperature>  (flairpucks, Flair_Puck_Temperature, Flair_Temperature)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/Temperature:state:default]"}
Number flairpuck1Humidity "FP1(MB) Room Humidity [%.2f%%]" <humidity>  (flairpucks, Flair_Humidity)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/Humidity:state:default]"}
Number flairpuck1Pressure "FP1(MB) Room Pressure [%.2fkPa]" <pressure>  (flairpucks, Flair_Pressure)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/Pressure:state:default]"}
Number flairpuck1Light "FP1(MB) Room Light [%.2f]" <sun>  (flairpucks, Flair_Light)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/light:state:default]"}
Number flairpuck1Set "FP1(MB) Set Temperature [%.2f °C]" <temperature>  (flairpucks)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/set_temp:state:default],>[proliant:openhab/sensors/flair/command/puck/Master Bedroom-0b07/set_temp:command:*:${command}]"}
Number flairpuck1BatteryVolt "FP1(MB) Battery Voltage [%.2f V]" <batteryfull>  (flairpucks, Flair_Volts_Mains)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/battery:state:default]"}
Number flairpuck1Battery "FP1(MB) Battery [%d%%]" <battery>  (flairpucks, Battery, Flair_Battery_Mains)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/bat_percent:state:default]"}
DateTime flairpuck1Date "FP1(MB) Last Reading [%1$ta %1$tR]" <clock>  (flairpucks)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/date:state:default]"}
Number flairpuck1Rssi "FP1(MB) RSSI [%d dBm]" <network>  (flairpucks)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/RSSI:state:default]"}
String flairpuck1Set_By "FP1(MB) Set By [%s]" <msg>  (flairpucks)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/set_by:state:default]"}
Switch flairpuck1Set_Point_Manual "FP1(MB) Manual Override [%s]" (flairpucks)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/set_point_manual:state:MAP(switch.map)],>[proliant:openhab/sensors/flair/command/puck/Master Bedroom-0b07/set_point_manual:command:OFF:${command}]", autoupdate="false"}
String flairpuck1Hold_Reason "FP1(MB) Hold Reason [%s]" <msg>  (flairpucks)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/hold_reason:state:default]"}
DateTime flairpuck1Hold_Until "FP1(MB) Hold Until [%1$ta %1$tR]" <clock>  (flairpucks)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/hold_until:state:default]"}
String flairpuck1LastUpdate "FP1(MB) Last Update [%s]" <clock>  (flairpucks)   {mqtt="<[proliant:openhab/sensors/flair/puck/Master Bedroom-0b07/LastUpdate:state:default]"}
```
### Sitemap
```
Frame item=flairnetwork label="Family Room" {
    Switch item=flairpuck2Occupied visibility=[flairpuck2Online==ON]
    Text item=flairpuck2Set_By visibility=[flairpuck2Online==ON]
    Text item=flairpuck2Online label="FP2(FR) puck [Offline]" labelcolor=[OFF="#ff0000"]  valuecolor=["#ff0000"]  visibility=[flairpuck2Online==OFF]
    Text item=flairpuck2Date valuecolor=[>300="red",>120="orange",<=120="green"] //visibility=[flairpuck2Date>120] //bug makes this not work currently
    Text item=flairpuck2Temp visibility=[flairpuck2Online==ON]
    Switch item=flairpuck2Set_Point_Manual mappings=[ON="HOLDING", OFF="CLEAR"] visibility=[flairpuck2Set_Point_Manual==ON] valuecolor=["red"]
    Text item=flairpuck2Hold_Reason visibility=[flairpuck2Set_Point_Manual==ON]
    Text item=flairpuck2Hold_Until visibility=[flairpuck2Set_Point_Manual==ON]
    Setpoint item=flairpuck2Set label="FP2(FR) Target Temperature [%.1f °C]" minValue=15 maxValue=30 step=0.5 visibility=[flairpuck2Online==ON]
    Text item=flairvent2Temp visibility=[flairvent2Online==ON]
    Text item=flairpuck2Humidity visibility=[flairpuck2Online==ON]
    Text item=flairvent2Pressure_diff visibility=[flairvent2Online==ON]
    Text item=flairvent2Set_By visibility=[flairvent2Online==ON]
    Slider item=flairvent2Open labelcolor=[flairvent2Online==OFF="#ff0000"] valuecolor=[flairvent2Online==OFF="#ff0000"] visibility=[flairvent2Online==ON]
    Text item=flairvent2Open labelcolor=[flairvent2Online==OFF="#ff0000"] valuecolor=[flairvent2Online==OFF="#ff0000"] visibility=[flairvent2Online==OFF]
    Text item=flairvent2Date valuecolor=[>300="red",>120="orange",<=120="green"] //visibility=[flairvent2Date>120] //bug makes this not work currently
    Text item=flairvent2aTemp visibility=[flairvent2aOnline==ON]
    Text item=flairvent2aPressure_diff visibility=[flairvent2aOnline==ON]
    Text item=flairvent2aSet_By visibility=[flairvent2aOnline==ON]
    Slider item=flairvent2aOpen labelcolor=[flairvent2aOnline==OFF="#ff0000"] valuecolor=[flairvent2aOnline==OFF="#ff0000"] visibility=[flairvent2aOnline==ON]
    Text item=flairvent2aOpen labelcolor=[flairvent2aOnline==OFF="#ff0000"] valuecolor=[flairvent2aOnline==OFF="#ff0000"] visibility=[flairvent2aOnline==OFF]
    Text item=flairvent2aDate valuecolor=[>300="red",>120="orange",<=120="green"] //visibility=[flairvent2aDate>120] //bug makes this not work currently
    Text item=flairvent2aDate label="Last Reading [%1$ta %1$tR]" valuecolor=[>300="red",>30="orange",<=30="green"] visibility=[flairvent2Date < 120, flairvent2aDate < 120, flairpuck2Date < 120]
}
```
### Rules
```
rule "Vent 2 (Family Room - patio doors) Received Pressure update"
when
    Item flairvent2Pressure received update
then
    var vent_pressure = flairvent2Pressure.state as DecimalType
    var room_pressure = flairpuck2Pressure.state as DecimalType
    var diff = (vent_pressure - room_pressure) * 1000.0
    logInfo("Flair Vent", "Family Room (doors) Pressure Diff: " + diff)
    postUpdate(flairvent2Pressure_diff, diff)
end
```
### Transforms
switch.map:
```
ON=ON
OFF=OFF
0=OFF
1=ON
True=ON
False=OFF
true=ON
false=OFF
-=Unknown
NULL=Unknown
```