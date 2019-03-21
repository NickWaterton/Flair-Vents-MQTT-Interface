#!/usr/bin/env python

'''
api calls are to https://my.flair.co/api/structures/1234 (1234 is our house_id)
all other calls are to links from this structure
Oauth 2 authentication is required first (see id and secret below)

N Waterton 6th April 2018 V 1.0 Initial release
N Waterton 21st march 2019 V 1.1 Updated to support python 2 or 3.
'''

from flair_api import make_client, Resource
from flair_api.client import ApiError
from requests import ConnectionError
import json
from datetime import datetime, timedelta, tzinfo
import time
import os,sys
import logging
from logging.handlers import RotatingFileHandler
import paho.mqtt.client as paho
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

API_ROOT = 'https://api.flair.co'
__VERSION__ = "1.1"

class t_zone(tzinfo):
    '''
    tzinfo derived UTC with offset
    timezones are such a pain...
    '''
    def __init__(self, offset=0, name='UTC'):
        self.offset = timedelta(seconds=offset)
        self.name = name

    def utcoffset(self, dt):
        return self.offset

    def tzname(self, dt):
        return self.name

    def dst(self, dt):
        return timedelta(0)

class Room(Resource):
    '''
    "type": "rooms"
    
    "name": "Francesca's Bedroom",
    "room-type": null,
    "humidity-away-min": 10,
    "hold-until": null,
    "created-at": "2018-03-09T19:24:39.076533+00:00",
    "temp-away-max-c": 22.5,
    "pucks-inactive": "Active",
    "humidity-away-max": 80,
    "updated-at": "2018-03-27T13:38:22.909098+00:00",
    "set-point-manual": false,
    "occupancy-mode": "Flair Auto",
    "level": null,
    "preheat-precool": true,
    "room-away-mode": "Smart Away",
    "set-point-c": 22,
    "current-humidity": 47,
    "frozen-pipe-pet-protect": true,
    "windows": null,
    "hold-reason": "ApiActive",
    "air-return": false,
    "temp-away-min-c": 16,
    "active": true,
    "current-temperature-c": 21.6408333333333
    '''
    @property
    def name(self):
        return self.attributes['name']
        
    @property
    def room_type(self):
        return self.attributes['room-type']
        
    @property
    def humidity_away_min(self):
        return self.attributes['humidity-away-min']
        
    @property
    def hold_until_string(self):
        return self.attributes['hold-until']
        
    @property
    def hold_until(self):
        try:
            return datetime.strptime(
                self.attributes['hold-until'], 
                '%Y-%m-%dT%H:%M:%S.%f+00:00'
            )
        except TypeError:
            return None
        
    @property
    def local_hold_until_string_iso(self):
        try:
            return datetime.strptime(
                self.attributes['hold-until'], 
                '%Y-%m-%dT%H:%M:%S.%f+00:00'
            ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()
        except TypeError:
            return None
    
    @property
    def date_created(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        )
        
    @property
    def date_string_created(self):
        return self.attributes['created-at']
                  
    @property
    def date_string_created_iso(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()  
            
    @property
    def temp_away_max_c(self):
        return self.attributes['temp-away-max-c']
                
    @property
    def pucks_inactive(self):
        return self.attributes['pucks-inactive']
                
    @property
    def humidity_away_max(self):
        return self.attributes['humidity-away-max']
        
    @property
    def date(self):
        return datetime.strptime(
            self.attributes['updated-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        )
        
    @property
    def date_string(self):
        return self.attributes['updated-at']
            
    @property
    def local_date_string_iso(self):
        return datetime.strptime(
            self.attributes['updated-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()
                
    @property
    def set_point_manual(self):
        return self.attributes['set-point-manual']
                
    @property
    def occupancy_mode(self):
        return self.attributes['occupancy-mode']
                
    @property
    def level(self):
        return self.attributes['level']
                
    @property
    def preheat_precool(self):
        return self.attributes['preheat-precool']
                
    @property
    def room_away_mode(self):
        return self.attributes['room-away-mode']
                
    @property
    def set_point_c(self):
        return self.attributes['set-point-c']
                
    @property
    def current_humidity(self):
        return self.attributes['current-humidity']
                
    @property
    def frozen_pipe_pet_protect(self):
        return self.attributes['frozen-pipe-pet-protect']
                
    @property
    def windows(self):
        return self.attributes['windows']
                    
    @property
    def hold_reason(self):
        return self.attributes['hold-reason']  
        
    @property
    def air_return(self):
        return self.attributes['air-return'] 
        
    @property
    def temp_away_min_c(self):
        return self.attributes['temp-away-min-c'] 
        
    @property
    def active(self):
        return self.attributes['active'] 
        
    @property
    def current_temperature_c(self):
        return self.attributes['current-temperature-c'] 

class Vent(Resource):
    '''
    "type": "vents"
    
    "name": "Master Bedroom-d7df",
    "created-at": "2017-08-14T18:31:50.699633+00:00",
    "updated-at": "2018-03-01T09:56:19.333264+00:00",
    "inactive": false,
    "setup-lightstrip": 1,
    "percent-open": 100
    '''
    @property
    def name(self):
        return self.attributes['name']
    
    @property
    def date(self):
        return datetime.strptime(
            self.attributes['updated-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        )
        
    @property
    def date_string(self):
        return self.attributes['updated-at']
            
    @property
    def local_date_string_iso(self):
        return datetime.strptime(
            self.attributes['updated-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()
        
    @property
    def inactive(self):
        return self.attributes['inactive']
        
    @property
    def percent_open(self):
        return self.attributes['percent-open']

class VentState(Resource):
    '''
    "type": "vent-states"
    
    "reporting-interval-ms": null,
    "sub-ghz-radio-tx-power-mw": null,
    "changeset": [
    "percent_open"
    ],
    "created-at": "2018-03-01T09:56:19.326962+00:00",
    "set-by": "Algo",
    "lightstrip": null,
    "motor-open-duty-cycle-percent": null,
    "read": true,
    "percent-open": 100,
    "motor-max-rotate-time-ms": null,
    "motor-close-duty-cycle-percent": null,
    "demo-mode": null
    '''
    @property
    def date(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        )
        
    @property
    def date_string(self):
        return self.attributes['created-at']
            
    @property
    def local_date_string_iso(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()
    
    @property
    def motor_open_duty_cycle_percent(self):
        return self.attributes['motor-open-duty-cycle-percent']
    
    @property
    def set_by(self):
        return self.attributes['set-by']
        
    @property
    def motor_max_rotate_time_ms(self):
        return self.attributes['motor-max-rotate-time-ms']
        
    @property
    def sub_ghz_radio_tx_power_mw(self):
        return self.attributes['sub-ghz-radio-tx-power-mw']
        
    @property
    def motor_close_duty_cycle_percent(self):
        return self.attributes['motor-close-duty-cycle-percent']
        
    @property
    def percent_open(self):
        return self.attributes['percent-open']
    
class VentSensorReading(Resource):
    '''
    "type": "vent-sensor-readings"
    
    "motor-run-time": 950,
    "lights": null,
    "created-at": "2018-03-01T15:11:03.078465+00:00",
    "firmware-version-s": null,
    "system-voltage": 3.3,
    "duct-pressure": 99.51,
    "rssi": -62,
    "duct-temperature-c": 21.47,
    "percent-open": 100
    ''' 
    @property
    def firmware_version_s(self):
        return self.attributes['firmware-version-s']
    
    @property
    def date(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        )
        
    @property
    def date_string(self):
        return self.attributes['created-at']
            
    @property
    def local_date_string_iso(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()
    
    @property
    def lights(self):
        return self.attributes['lights']
    
    @property
    def percent_open(self):
        return self.attributes['percent-open']
        
    @property
    def rssi(self):
        return self.attributes['rssi']
        
    @property
    def duct_pressure(self):
        return self.attributes['duct-pressure']
        
    @property
    def system_voltage(self):
        return self.attributes['system-voltage']
        
    @property
    def duct_temperature_c(self):
        return self.attributes['duct-temperature-c']
        
    @property
    def motor_run_time(self):
        return self.attributes['motor-run-time']
        
class Puck(Resource):
    '''
    "type": "pucks"
    
    "inactive": false,
    "created-at": "2018-02-28T16:24:36.919078+00:00",
    "updated-at": "2018-03-01T02:56:11.806463+00:00",
    "drop-rate": 1.01291666666667,
    "sub-ghz-radio-tx-power-mw": null,
    "humidity-offset": null,
    "puck-display-color": "white",
    "current-humidity": 48,
    "display-number": "97b2",
    "temperature-offset-override-c": null,
    "current-temperature-c": 22.2823076923077,
    "beacon-interval-ms": 4095,
    "bluetooth-tx-power-mw": 500,
    "demo-mode": 0,
    "is-gateway": false,
    "name": "Family Room-97b2",
    "oauth-app-assigned-at": null,
    "ir-setup-enabled": null,
    "reporting-interval-ds": 255,
    "temperature-offset-c": null,
    "orientation": "standing",
    "ir-download": false,
    "current-rssi": -66.7692307692308
    '''
    @property
    def name(self):
        return self.attributes['name']
        
    @property
    def display_number(self):
        return self.attributes['display-number']
        
    @property
    def inactive(self):
        return self.attributes['inactive']
    
    @property
    def date(self):
        return datetime.strptime(
            self.attributes['updated-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        )
        
    @property
    def date_string(self):
        return self.attributes['updated-at']
            
    @property
    def local_date_string_iso(self):
        return datetime.strptime(
            self.attributes['updated-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()
    
    @property
    def temperature_offset_override_c(self):
        return self.attributes['temperature-offset-override-c']
        
    @property
    def temperature_offset_c(self):
        return self.attributes['temperature-offset-c']
        
    @property
    def rssi(self):
        return self.attributes['current-rssi']
        
    @property
    def current_temperature_c(self):
        return self.attributes['current-temperature-c']
        
    @property
    def bluetooth_tx_power_mw(self):
        return self.attributes['bluetooth-tx-power-mw']
        
    @property
    def is_gateway(self):
        return self.attributes['is-gateway']
        
    @property
    def reporting_interval_ds(self):
        return self.attributes['reporting-interval-ds']
        
    @property
    def sub_ghz_radio_tx_power_mw(self):
        return self.attributes['sub-ghz-radio-tx-power-mw']
        
    @property
    def drop_rate(self):
        return self.attributes['drop-rate']
        
    @property
    def beacon_interval_ms(self):
        return self.attributes['beacon-interval-ms']
        
    @property
    def humidity_offset(self):
        return self.attributes['humidity-offset']
        
    @property
    def current_humidity(self):
        return self.attributes['current-humidity']
        
    @property
    def orientation(self):
        return self.attributes['orientation']
        
class PuckState(Resource):
    '''
    "type": "puck-states"
    
    "puck-display-color": "white",
    "bluetooth-tx-power-mw": 500,
    "ir-download": false,
    "ir-setup": false,
    "beacon-interval-ms": 4095,
    "temperature-offset-c": 0,
    "firmware-version-s": 0,
    "changeset": [
    "desired_temperature"
    ],
    "ir-dispatch": {},
    "display-image": null,
    "operation-mode": "h",
    "read": true,
    "created-at": "2018-03-01T02:56:11.739601+00:00",
    "firmware-version-b": 0,
    "sub-ghz-radio-tx-power-mw": null,
    "desired-temperature": 2200,
    "orientation": "standing",
    "display-text": null,
    "setup-mode": false,
    "display-ttl-ms": null,
    "demo-mode": 0,
    "reporting-interval-ds": 255,
    "firmware-version-w": 0,
    "temperature-display-scale": "C",
    "set-by": "Algo"
    '''      
    @property
    def operation_mode(self):
        return self.attributes['operation-mode']
        
    @property
    def temperature_display_scale(self):
        return self.attributes['temperature-display-scale']
        
    @property
    def temperature_offset_c(self):
        return self.attributes['temperature-offset-c']
        
    @property
    def firmware_version_b(self):
        return self.attributes['firmware-version-b']
        
    @property
    def firmware_version_w(self):
        return self.attributes['firmware-version-w']
        
    @property
    def firmware_version_s(self):
        return self.attributes['firmware-version-s']
    
    @property
    def date(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        )
        
    @property
    def date_string(self):
        return self.attributes['created-at']
              
    @property
    def local_date_string_iso(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()
    
    @property
    def desired_temperature(self):
        return self.attributes['desired-temperature']
    
    @property
    def set_by(self):
        return self.attributes['set-by']
        
    @property
    def bluetooth_tx_power_mw(self):
        return self.attributes['bluetooth-tx-power-mw']
        
    @property
    def reporting_interval_ds(self):
        return self.attributes['reporting-interval-ds']
        
    @property
    def sub_ghz_radio_tx_power_mw(self):
        return self.attributes['sub-ghz-radio-tx-power-mw']
        
    @property
    def beacon_interval_ms(self):
        return self.attributes['beacon-interval-ms']
        
    @property
    def orientation(self):
        return self.attributes['orientation']
        
class PuckSensorReading(Resource):
    '''
    "type": "sensor-readings"
    
    "room-pressure": 99.48,
    "rotary-encoded-clicks": 0,
    "humidity": 45,
    "created-at": "2018-03-01T15:10:37.130427+00:00",
    "firmware-version-b": 1,
    "die-temperature": 3864,
    "current-offset": -500,
    "button-pushes": 0,
    "firmware-version-s": 93,
    "temperature": 2536,
    "message-version": 0,
    "firmware-version-w": 95,
    "desired-temperature-c": 22,
    "system-voltage": 3.41,
    "light": 1,
    "is-gateway": true,
    "room-temperature-c": 20.36,
    "rssi": 0
    ''' 
    @property
    def firmware_version_b(self):
        return self.attributes['firmware-version-b']
        
    @property
    def firmware_version_w(self):
        return self.attributes['firmware-version-w']
        
    @property
    def firmware_version_s(self):
        return self.attributes['firmware-version-s']
    
    @property
    def date(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        )
        
    @property
    def date_string(self):
        return self.attributes['created-at']
        
    @property
    def local_date_string_iso(self):
        return datetime.strptime(
            self.attributes['created-at'], 
            '%Y-%m-%dT%H:%M:%S.%f+00:00'
        ).replace(tzinfo=t_zone()).astimezone(Local_tz).isoformat()
    
    @property
    def light(self):
        return self.attributes['light']
    
    @property
    def current_offset(self):
        return self.attributes['current-offset']
        
    @property
    def die_temperature(self):
        return self.attributes['die-temperature']
    
    @property
    def temperature(self):
        return self.attributes['temperature']
        
    @property
    def desired_temperature_c(self):
        return self.attributes['desired-temperature-c']   
        
    @property
    def rssi(self):
        return self.attributes['rssi']
        
    @property
    def room_pressure(self):
        return self.attributes['room-pressure']
        
    @property
    def system_voltage(self):
        return self.attributes['system-voltage']
        
    @property
    def room_temperature_c(self):
        return self.attributes['room-temperature-c']   
        
    @property
    def is_gateway(self):
        return self.attributes['is-gateway']
        
    @property
    def humidity(self):
        return self.attributes['humidity']
        
        
#setup logging
def setup_logger(logger_name, log_file, level=logging.DEBUG, console=False):
    try: 
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s] (%(threadName)-10s) %(message)s')
        if log_file is not None:
            fileHandler = logging.handlers.RotatingFileHandler(log_file, mode='a', maxBytes=2000000, backupCount=5)
        fileHandler.setFormatter(formatter)
        if console == True:
          streamHandler = logging.StreamHandler()

        l.setLevel(level)
        if log_file is not None:
            l.addHandler(fileHandler)
        if console == True:
          l.addHandler(streamHandler)
             
    except Exception as e:
        print("Error in Logging setup: %s - do you have permission to write the log file??" % e)
        sys.exit(1)
        
def battery_percent(bat_volt):
    '''
    Calculate battery percentage from battery voltage
    bat_volt is a float in V eg 2.900 V
    Max voltage is 3.5 V, nominal 3.0V,
    min is 2.4 V (ish) - which is dead
    '''
    if bat_volt is None or bat_volt == 0:
        #not valid readings
        return "-"
    
    Vmax = 3.000
    Vmin = 2.400
    
    if bat_volt < Vmin:
        return "0"
        
    if bat_volt > Vmax:
        return "100"
    
    Vrange = Vmax-Vmin
    bat_percent = int(((bat_volt - Vmin)/ Vrange)* 100)
    return str(bat_percent)
    
def getStructure(CLIENT_ID, CLIENT_SECRET, API_ROOT, house_id):
    log.info("Authenticating")
    try:
        client = make_client(CLIENT_ID, CLIENT_SECRET, API_ROOT,
            mapper={
                'vent-sensor-readings': VentSensorReading,
                'vent-states': VentState,
                'vents' : Vent,
                'sensor-readings' : PuckSensorReading,
                'puck-states' : PuckState,
                'pucks' : Puck,
                'rooms' : Room
            },
            admin=True
        )
        
        if client is None or client.expires_in is None:
            log.error("failed to Authenticate, check CLIENT_ID, CLIENT_SECRET")
            return None, 0
            
        log.info("Authenticated for %ds" % (client.expires_in))
        
        return client.get("structures", id=house_id), time.time() + client.expires_in   #structure for our house id, time authentication expires
    except ApiError as e:
        log.error(e.status_code)
        log.error(e.json)
        log.exception(e)
        
    return None, 0
        
def PublishVent_data(structure, mqttc=None, name=None):
    vent_data = {}
    try:
        vents = structure.get_rel("vents")
        if name is None:
            log.info("got data for %d vents" % len(vents))
        else:
            log.info("got data for %d vents, just %s: %s" % (len(vents), 'showing' if mqttc is None else 'publishing', name))
        
        for vent in vents:
            sensor_readings = vent.get_rel('sensor-readings')
            #states = vent.get_rel('vent-states')
            current_state = vent.get_rel('current-state')
            #room = vent.get_rel('room')
            
            if vent.inactive:
                vent_data[vent.name] = {'online':False}
            else:
                vent_data[vent.name] = {'date':sensor_readings[0].local_date_string_iso, 
                                        'Pressure':sensor_readings[0].duct_pressure, 
                                        'Temperature':sensor_readings[0].duct_temperature_c, 
                                        'percent_open':sensor_readings[0].percent_open, 
                                        'RSSI':sensor_readings[0].rssi, 
                                        'battery':sensor_readings[0].system_voltage, 
                                        'bat_percent':battery_percent(sensor_readings[0].system_voltage),
                                        'set_by':current_state.set_by,
                                        'online':True}
                                        
            if name is None or name == vent.name:
                log.info("Vent: %s, Latest Reading: %s" % (vent.name, json.dumps(vent_data[vent.name], indent=2, sort_keys=True)))
                if mqttc is not None:
                    mqttc.publish('%s/flair/vent/%s/LastUpdate' % (pub_topic,vent.name), "%s" % time.ctime())
                    for data, value in vent_data[vent.name].items():
                        if value is not None:
                            mqttc.publish('%s/flair/vent/%s/%s' % (pub_topic,vent.name,data), value)
                else:
                    log.info("Data NOT published")
            
    except ApiError as e:
        log.error(e.status_code)
        log.error(e.json)
        log.exception(e)
       
    return vent_data

def PublishPuck_data(structure, mqttc=None, name=None):
    puck_data = {}
    try:
        pucks = structure.get_rel("pucks")
        if name is None:
            log.info("got data for %d pucks" % len(pucks))
        else:
            log.info("got data for %d pucks, just %s: %s" % (len(pucks), 'showing' if mqttc is None else 'publishing', name))
        
        for puck in pucks:
            sensor_readings = puck.get_rel('sensor-readings')
            #puck_states = puck.get_rel('puck-states')
            current_state = puck.get_rel('current-state')
            room = puck.get_rel('room')

            if puck.rssi == None:
                puck_data[puck.name] = {'online':False}
            else:
                puck_data[puck.name] = {'date':sensor_readings[0].local_date_string_iso, 
                                        'Pressure':sensor_readings[0].room_pressure, 
                                        'Temperature':sensor_readings[0].room_temperature_c, 
                                        'Humidity':sensor_readings[0].humidity, 
                                        'light':sensor_readings[0].light, 
                                        'set_temp':current_state.desired_temperature/100.0,
                                        'set_point_c':room.set_point_c,
                                        'RSSI':sensor_readings[0].rssi, 
                                        'battery':sensor_readings[0].system_voltage, 
                                        'bat_percent':battery_percent(sensor_readings[0].system_voltage),
                                        'active':False if puck.inactive else True,
                                        'occupied':room.active,
                                        'room_name': room.name,
                                        'set_by':current_state.set_by,
                                        'set_point_manual':room.set_point_manual,
                                        'hold_reason':room.hold_reason,
                                        'hold_until':room.local_hold_until_string_iso,
                                        'online':True}
                                        
            if name is None or name == puck.name:
                log.info("Puck: %s, Latest Reading: %s" % (puck.name, json.dumps(puck_data[puck.name], indent=2, sort_keys=True)))
                if mqttc is not None:
                    mqttc.publish('%s/flair/puck/%s/LastUpdate' % (pub_topic,puck.name), "%s" % time.ctime())
                    for data, value in puck_data[puck.name].items():
                        if value is not None:
                            mqttc.publish('%s/flair/puck/%s/%s' % (pub_topic,puck.name,data), value)
                else:
                    log.info("Data NOT published")
        
    except ApiError as e:
        log.error(e.status_code)
        log.error(e.json)
        log.exception(e)
        
    return puck_data
    
def update_room_desired_temp(structure, name, value):
    updateRoom(structure, name, {'set-point-c':value})
    
def update_room_occupied(structure, name, value):
    updateRoom(structure, name, {'active':value})
    
def update_room_clear_hold(structure, name, value):
    updateRoom(structure, name, {'hold-until':value}, False)
    data = PublishPuck_data(structure, mqttc=None, name=name)
    if data[name]['set_point_c'] != data[name]['set_temp']:
        updateRoom(structure, name, {'set-point-c':data[name]['set_point_c']}, False)
        updateRoom(structure, name, {'hold-until':value})
    else:
        PublishPuck_data(structure, mqttc, name)

def updateRoom(structure, name, value, publish=True):
    try:
        pucks = structure.get_rel('pucks')
        for puck in pucks:
            if puck.rssi != None:
                if puck.name == name:
                    room = puck.get_rel('room')
                    log.info("Updating Room: %s to: %s" % (room.name, value))
                    #room.update(attributes={'active':value}, relationships=dict(structure=structure, room=room))
                    room.update(attributes=value)
                    log.info("updated")
                    if publish:
                        PublishPuck_data(structure, mqttc, name)
        
    except ApiError as e:
        log.error(e.status_code)
        log.error(e.json)
        log.exception(e)
        
def updatePuck(structure, name, value, publish=True):
    try:
        pucks = structure.get_rel('pucks')
        for puck in pucks:
            if puck.rssi != None:
                if puck.name == name:
                    #puck_state = puck.get_rel('current-state')
                    room = puck.get_rel('room')
                    log.info("Updating Room: %s to desired_temperature: %s" % (room.name, value))
                    #room.update(attributes={'set-point-c':value}, relationships=dict(structure=structure, puck=puck))
                    room.update(attributes={'set-point-c':value})
                    log.info("updated")
                    if publish:
                        PublishPuck_data(structure, mqttc, name)
        
    except ApiError as e:
        log.error(e.status_code)
        log.error(e.json)
        log.exception(e)

def updateVent(structure, name, value, publish=True):
    try:
        vents = structure.get_rel('vents')
        for vent in vents:
            if not vent.inactive:
                if vent.name == name:
                    log.info("Updating Vent: %s to percent_open: %d%%" % (vent.name, value))
                    #vent.update(attributes={'percent-open':value}, relationships=dict(structure=structure, vent=vent))
                    vent.update(attributes={'percent-open':value})
                    log.info("updated")
                    if publish:
                        PublishVent_data(structure, mqttc, name)
        
    except ApiError as e:
        log.error(e.status_code)
        log.error(e.json)
        log.exception(e)      
        
        
def read_config_file(file="./config.ini"):
        #read config file
        result = {}
        Config = ConfigParser.ConfigParser()
        dataset = Config.read(file)
        if len(dataset) == 0:
            return result  
        log.info("reading info from config file %s" % file)
        houses = Config.sections()
        if len(houses) > 1:
            log.warn("config file has entries for %d Houses, "
                          "only using the first!")
        house = houses[0]
        result['house_id']=house
        result['CLIENT_ID'] = Config.get(house, "CLIENT_ID")
        result['CLIENT_SECRET'] = Config.get(house, "CLIENT_SECRET")
        result['broker'] = Config.get(house, "broker")
        result['port'] = Config.getint(house, "port")
        result['pub_topic'] = Config.get(house, "pub_topic")
        result['user'] = Config.get(house, "user")
        result['password'] = Config.get(house, "password")

        return result
        
def write_config_file(file="./config.ini", house_id=None, values=None):
    Config = ConfigParser.ConfigParser()
    Config.add_section(house_id)
    for key, value in values.items():
        Config.set(house_id,key, value)
    # write config file
    with open(file, 'w') as cfgfile:
        Config.write(cfgfile)
    log.info("wrote config file: %s" % file)
    
def update_config_file(arg, file="./config.ini", house_id=None, values=None):
    updated = False
    if house_id != arg.house_id and arg.house_id is not None:
        house_id = arg.house_id
        updated = True
    if values['CLIENT_ID'] != arg.client_id and arg.client_id is not None:
        values['CLIENT_ID']=arg.client_id
        updated = True
    if values['CLIENT_SECRET'] != arg.client_secret and arg.client_secret is not None:
        values['CLIENT_SECRET']=arg.client_secret
        updated = True
    if values['user'] != arg.user and arg.user is not None:
        values['user']=arg.user
        updated = True
    if values['password'] != arg.password  and arg.password  is not None:
        values['password']=arg.password
        updated = True
    if values['broker'] != arg.broker  and arg.broker is not None:
        values['broker']=arg.broker
        updated = True
    if values['port'] != arg.port  and arg.port is not None:
        values['port']=arg.port
        updated = True
    if values['pub_topic'] != arg.topic  and arg.topic is not None:
        values['pub_topic']=arg.topic
        updated = True
    if updated:
        write_config_file(house_id=house_id, values=values)
    return house_id, values

    
#------- MQTT Callabcks -----------
                
def on_message(mosq, obj, msg):
    global mqttc
    #log.info("message topic: %s, value:%s received" % (msg.topic,msg.payload.decode("utf-8")))
    command = msg.topic.split('/')[-1]
    device = msg.topic.split('/')[-2]
    value = msg.payload.decode("utf-8")
    
    if value == 'ON':
        value = True
    elif value == 'OFF':
        value = False
    
    if 'puck' in msg.topic:
        log.info("Received setting: %s:%s for Puck: %s" % (command,value,device))
        if command == 'occupied':
            update_room_occupied(structure, device, value)
        elif command == 'set_temp':
            update_room_desired_temp(structure, device, value)
        elif command == 'set_point_manual':
            update_room_clear_hold(structure, device, None)
    elif 'vent' in msg.topic:
        log.info("Received setting: %s:%s for Vent: %s" % (command,value,device))
        if command == 'percent_open':
            updateVent(structure, device, int(value))

def on_connect(mosq, obj, rc):
    global mqttc
    #log.info("rc: %s" % str(rc))
    mqttc.subscribe(pub_topic +"/flair/command/#", 0) #eg openhab/sensors/flair/command/puck/

def on_publish(mosq, obj, mid):
    #log.info("published: %s %s" % (str(mid), str(obj)))
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    log.info("Subscribed: %s %s" % (str(mid), str(granted_qos)))

def on_disconnect():
    pass

def on_log(mosq, obj, level, string):
    log.info(string)

def main():
    import argparse
    global log
    global mqttc
    global pub_topic
    global structure
    global Local_tz
    
    parser = argparse.ArgumentParser(description='Read Flair Smart Vents/Pucks Values and Sensors, publish via MQTT')
    parser.add_argument('-id','--house_id', action="store", default=None, help='flair house id (default=None)')
    parser.add_argument('-cid','--client_id', action="store", default=None, help='flair API CLIENT ID (default=None)')
    parser.add_argument('-cs','--client_secret', action="store", default=None, help='flair API CLIENT SECRET (default=None)')
    parser.add_argument('-n',action='store', dest='count', default=0,type=int, help="Number of times to loop data, 0=forever")
    parser.add_argument('-t',action='store',type=int, default=60, help='time between polling default=60s')
    parser.add_argument('-b','--broker', action="store", default=None, help='mqtt broker to publish sensor data to. (default=127.0.0.1)')
    parser.add_argument('-p','--port', action="store", type=int, default=None, help='mqtt broker port (default=1883)')
    parser.add_argument('-u','--user', action="store", default=None, help='mqtt broker username. (default=none)')
    parser.add_argument('-pw','--password', action="store", default=None, help='mqtt broker password. (default=None)')
    parser.add_argument('-m','--topic', action="store",default=None, help='topic to publish sensor data to. (default=openhab/sensors)')
    parser.add_argument('-l','--log', action="store",default="~/Scripts/flair_vents.log", help='main log file. (default=~/Scripts/flair_vents.log)')
    parser.add_argument('-C','--config', action='store_true', help='use config File', default = False)
    parser.add_argument('-D','--debug', action='store_true', help='debug mode', default = False)
    parser.add_argument('-V','--version', action='version',version='%(prog)s {version}'.format(version=__VERSION__))

    arg = parser.parse_args()
    
    
    #----------- Logging ----------------
    if arg.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
        
    #log_level = logging.DEBUG   #FOR TESTING, REMOVE FOR PRODUCTION
    
    if arg.log == 'None':
        log_file = None
    else:
        log_file=os.path.expanduser(arg.log)
    
    setup_logger('Main', log_file, level=log_level, console=True)
    
    log = logging.getLogger('Main')             #set up logging
    
    log.info("****** Program Started ********")
    log.debug("Debug Mode")
    
    values = {'broker':'127.0.01', 'port':1883, 'pub_topic':'openhab/sensors'} #defaults
    config_file = False
    
    if arg.config:
        config_values = read_config_file()
        if len(config_values) > 0:
            config_file = True
            house_id = config_values.pop('house_id')
            house_id, config_values = update_config_file(arg, house_id=house_id, values=config_values)
            values.update(config_values)
    
    if not config_file:
        log.info("config is NONE")
        house_id = arg.house_id
        values['CLIENT_ID'] = arg.client_id
        values['CLIENT_SECRET'] = arg.client_secret
        if values['CLIENT_ID'] is None or values['CLIENT_SECRET'] is None or house_id is none:
            log.critical("You must enter your house_id, API CLIENT ID and CLIENT SECRET to access the flair API - get them from hello@flair.co")
            sys.exit(1)
        
        if arg.Topic is not None:
            values['pub_topic'] = arg.topic

        if arg.broker is not None:
            values['broker'] = arg.broker #mosquitto broker host

        if arg.port is not None:
            values['port'] = arg.port     #mosquitto broker port

        values['user'] = arg.user
        values['password'] = arg.password
        
        if arg.config:
            write_config_file(house_id=house_id, values=values)
            
    log.info("reading house: %s" % house_id)     
    pub_topic = values['pub_topic']
    broker = values['broker']
    port = values['port']
    user = values['user']
    password = values['password']
    CLIENT_ID = values['CLIENT_ID']
    CLIENT_SECRET = values['CLIENT_SECRET']
        

    mqttc = paho.Client()               #Setup MQTT
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    
    #figure out time zone offset
    is_dst = time.daylight and time.localtime().tm_isdst > 0
    utc_offset = - (time.altzone if is_dst else time.timezone)
    Local_tz = t_zone(utc_offset)
    
    counter = 0
    forever = False   
    if arg.count == 0:
        forever = True
        
    try:
        mqttc.will_set(pub_topic+"/flair/LastUpdate", "Offline at: %s" % time.ctime(), 0, False)
        if user is not None and password is not None:
            mqttc.username_pw_set(username=user,password=password)
        mqttc.connect(broker, port, arg.t+60)
        mqttc.loop_start()
        
        structure, expiry_time = getStructure(CLIENT_ID, CLIENT_SECRET, API_ROOT, house_id)
        
        while (counter < arg.count or forever):
            try:
                if time.time() >= expiry_time - arg.t:
                    structure, expiry_time = getStructure(CLIENT_ID, CLIENT_SECRET, API_ROOT, house_id)
                else:
                    log.info("Authentication expires in: %ds" % int(expiry_time - time.time()))
                    
                if structure is not None:
                    PublishVent_data(structure, mqttc)                  
                    PublishPuck_data(structure, mqttc)               
                    mqttc.publish(pub_topic+"/flair/LastUpdate", "%s" % time.ctime())
            
            except ApiError as e:
                log.error(e.status_code)
                log.error(e.json)
                log.exception(e)
                mqttc.publish(pub_topic+"/flair/LastUpdate", "API Error Updating at: %s" % time.ctime())
        
            except ConnectionError as e:    #requests.exceptions.ConnectionError
                log.exception(e)
                mqttc.publish(pub_topic+"/flair/LastUpdate", "Connection Error Updating at: %s" % time.ctime())
            
            if not forever: counter += 1
            time.sleep(arg.t)
        
    except (KeyboardInterrupt, SystemExit):
        log.info("System exit Received - Exiting program")
        mqttc.publish(pub_topic+"/flair/LastUpdate", "Program Exit at: %s" % time.ctime())
        
    finally:
        mqttc.loop_stop()
        mqttc.disconnect()
        
if __name__ == "__main__":
    main()