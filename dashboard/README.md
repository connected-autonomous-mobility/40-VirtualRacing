# Parking Lot Nerds - Racing Monitor
Version 0.1, May 3rd, 2020

![](https://github.com/Heavy02011/50-donkey/blob/master/dashboard/racing_monitor.png)

This code is in a very early stage and not really tested yet. Handle with care!

## 0 Prerequisites
our modified code versions
- [Ottawa-Autonomous-Vehicle-Group/donkeycar](https://github.com/Ottawa-Autonomous-Vehicle-Group/donkeycar)
- [sdsandbox-pln](https://github.com/Ottawa-Autonomous-Vehicle-Group/sdsandbox-pln)
- [TcpCarHandlers.cs](https://github.com/Ottawa-Autonomous-Vehicle-Group/sdsandbox-pln/blob/sim-racer/sdsim/Assets/Scripts/tcp/TcpCarHandler.cs): 

change from "time" 
```
   void SendTelemetry()
   {
      …
      json.AddField("time", Time.timeSinceLevelLoad);
      …
   }
```  
   to "time_simulator" in
```
   void SendTelemetry()
   {
      …
      json.AddField("time_simulator", Time.timeSinceLevelLoad);
      …
   }
```

## 1 Installation

### 1.1 [InfluxDB](https://www.thomas-krenn.com/de/wiki/InfluxDB_Installation_und_Konfiguration_unter_Ubuntu_Server_18.04)

### 1.2 [Grafana](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-grafana-on-ubuntu-18-04)
- install plotly plugin
```
grafana-cli plugins install natel-plotly-panel
```
- hint: use nanoseconds until epoch
```
time.tims_ns()
```

### 1.3 Configuration

- Add your login credentials into racing script ```racer_dashboard.py```:

```
dbclient = InfluxDBClient("127.00.0.1", 8086, "<user>", "<password>", databasename)
```
- Import the dashboard ```DIYrobocars-RacingDashboard-1588493699316.json```.
- Have fun!

## 2 Documentaion

- [grafana times series](https://grafana.com/docs/grafana/latest/guides/timeseries/)
- [samples influxdb](https://github.com/influxdata/influxdb-python/blob/master/examples/tutorial_sine_wave.py)


## 3 Testing with real data

### 3.1 influxdb python client
```
(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing/scripts$ python
Python 3.7.4 (default, Aug 13 2019, 20:35:49) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from influxdb import InfluxDBClient
>>> client = InfluxDBClient('localhost', 8086, '<user>', '<password>', 'example')
>>> client.create_database('example')
>>> json_body = [
...     {
...         "measurement": "DonkeySimulator",
...         "tags": {
...             "car": "PLN_8",
...             "race": "training"
...         },
...         "time": "2009-11-15T23:00:00Z",
...         "fields": {"msg_type": "telemetry", "steering_angle": -0.3062592, "throttle": 0.2804184, "speed": 5.567223, "image": "23", "hit": "none", "pos_x": 72.58524, "pos_y": 0.555452, "pos_z": 35.55362, "acc_x": 2.388114, "acc_y": 0.0007695926, "acc_z": 2.672911, "ang_acc_x": -4.858405, "ang_acc_y": 9.652755, "ang_acc_z": 0.747488, "wheelEncoderLR": -0.06308544, "wheelEncoderLF": -0.1019721, "wheelEncoderRF": -0.01272042, "wheelEncoderRR": -0.02423366, "time": 880.9467, "cte": -0.4879221}
...     }
... ]
>>> client.write_points(json_body)
True
>>> 
```

### 3.2 inspecting influxdb cli
```
influxdb
> show databases
name: databases
name
----
_internal
example
> use example
Using database example
> select * from DonkeySimulator
name: DonkeySimulator
time                acc_x     acc_y        acc_z     ang_acc_x ang_acc_y ang_acc_z  car   cte        hit  image msg_type  pos_x    pos_y     pos_z    race     speed    steering_angle throttle  wheelEncoderLF wheelEncoderLR wheelEncoderRF wheelEncoderRR
----                -----     -----        -----     --------- --------- ---------  ---   ---        ---  ----- --------  -----    -----     -----    ----     -----    -------------- --------  -------------- -------------- -------------- --------------
1258326000000000000 2.388114  0.0007695926 2.672911  -4.858405 9.652755  0.747488   PLN_8 -0.4879221 none 23    telemetry 72.58524 0.555452  35.55362 training 5.567223 -0.3062592     0.2804184 -0.1019721     -0.06308544    -0.01272042    -0.02423366
1258326182000000000 0.7830441 0.009175628  -2.676582 3.287839  -5.654635 -0.9827491 PLN_8 -0.5356815 none 23    telemetry 72.77829 0.5551577 36.4179  training 5.555685 -0.3169455     0.2590321 -0.02113376    0.1104023      -0.08089291    0.06320643
1258326302000000000 2.388114  0.0007695926 2.672911  -4.858405 9.652755  0.747488   PLN_8 -0.4879221 none 23    telemetry 72.58524 0.555452  35.55362 training 5.567223 -0.3062592     0.2804184 -0.1019721     -0.06308544    -0.01272042    -0.02423366
> 
```

### 3.3 Start race script

```
(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing/dashboard$ 
python racer_dashboard.py --model=../models/lane_keeper.h5 --host=127.0.0.1 --name pln

```
