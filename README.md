# 40-VirtualRacing: The Parking Lot Nerds Development Repository

![](https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/1774_115.png)

### 1 background

It all started at a parking lot...

A few guys meet there, discussed after a long meetup evening, came up with a crazy idea and made it happening. We met at Maker Faire Bay Area 2019 with more guys from [Oakland](http://diyrobocars.com), [Ann Arbor](https://www.meetup.com/a3vgroup/), [Detroit](https://www.meetup.com/Detroit-Autonomous-Vehicle-Meetup/), [Ottawa](https://www.meetup.com/Ottawa-Autonomous-Vehicle-Group/), [Shenzehn](https://www.roboticsmasters.co/), [Stuttgart](https://www.meetup.com/Connected-Autonomous-Driving) and many more countries. 
Now we're calling us the ***Parking Lot Nerds*** and are heading towards our new venture: Virtual Autonomous Racing. 

Thanks a lot to Ed & Tawn (Oakland), Nic & Paul (Ottawa), Dave (Ann Arbor), Linda & Wallarug (Shenzhen), Benjamin (Stuttgart) and especially Alex (Detroit) for literally driving the extra miles down to Stuttgart and making our journey to Silicon Valley / Maker Faire Bay Area 2019 a once in a life time experience.

<p float="left">
  
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/8F637155-8FAC-45C5-9554-D6F8E864B21D.jpeg" alt="drawing" width="300"/>
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/p11_data.png" alt="drawing" width="300"/>
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/p11_track.png" alt="drawing" width="300"/>
</p>





### 2 preparation

- [Tawn's gist](https://gist.github.com/tawnkramer/6d244090cb8f2af1bc9f6d1ebc0377b1)
- [Ottawa, Paul: Virtual-Hack-And-Race-Workshop](https://github.com/Ottawa-Autonomous-Vehicle-Group/Virtual-Hack-And-Race-Workshop)
- [Ottawa repo with an early model](https://github.com/Ottawa-Autonomous-Vehicle-Group/Simulator_racer)


### 3 [data](https://github.com/connected-autonomous-mobility/40-VirtualRacing/tree/master/data)


### 4 [training](https://github.com/connected-autonomous-mobility/40-VirtualRacing/tree/master/training)


### 5 [models](https://github.com/connected-autonomous-mobility/40-VirtualRacing/tree/master/models)

models trained by others
- [naisy](https://drive.google.com/file/d/1CwBHI4Ms1wphSNg2xyUn7fdYAkepYQSU/view)

### 6 [Leaderboard](https://aleaderboard.com/w2/b24ffdaf-895c-422f-9aed-c51c4edc4579)

### 7 twitch.tv channels

- [DAVG](https://www.twitch.tv/doavg)
- [Oakland](https://www.twitch.tv/mossmann3333)
- [Stuttgart](https://www.twitch.tv/DIYrobocars_stuttgart)

### 8 Quick Start

#### 8.1 Run your model
```
(donkey) rainer@neuron:~/mysim2$ python manage.py drive --model=models/lane_keeper.h5
```

#### 8.2 In your browser goto
```
http://localhost:8887/drive
```
And set mode to ```local pilot```

### 9 Races
#### [First Ever Virtual Race](https://youtu.be/BOzX-Bm0bk0) League @DIYrobocars, April 25th, 2020




<p float="left">
  
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/6E5AFF4A-5451-48A4-9A94-76E3E866379C.png" alt="drawing" width="300"/>
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/362A3608-0214-4FBE-B048-71AEA1683AE5.png" alt="drawing" width="300"/>
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/E572C649-CA33-40EE-8456-F95C59A8E4B4.png" alt="drawing" width="300"/>
</p>


<p float="left">
  
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/A6C51FE6-457B-4244-82C0-470353C6990E.png" alt="drawing" width="300"/>
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/182B7FFF-362B-4906-8CF0-88613AE0C27D.png" alt="drawing" width="300"/>
  <img src="https://github.com/connected-autonomous-mobility/40-VirtualRacing/blob/master/images/1F064E3D-F780-4989-A6AA-57F255DC00F5.png" alt="drawing" width="300"/>
</p>

- [Japan](https://www.youtube.com/watch?v=ilvRFw7jCwY)

### 10 [Reinforcement Learning (very experimental!)](https://github.com/connected-autonomous-mobility/40-VirtualRacing/tree/master/ddqn)

### Credits
- https://diyrobocars.com
- https://github.com/tawnkramer/gym-donkeycar
- https://github.com/Maximellerbach/Virtual_Racing
- https://github.com/robocarstore/donkey-car-training-on-google-colab/blob/master/Donkey_Car_Training_using_Google_Colab.ipynb
- https://github.com/Ottawa-Autonomous-Vehicle-Group/donkeycar
- https://github.com/Ottawa-Autonomous-Vehicle-Group/Simulator_racer
- https://github.com/Sashulik/DIYRobocars-Virtual-Racing-League (main repo)
- https://github.com/hogenimushi/donkey_data


