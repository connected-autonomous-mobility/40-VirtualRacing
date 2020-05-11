# Racing Model Performance

| Server | Client |Racing Script  | Model                         | no laps | fastest time | ping(ms) |
|--------|--------|---------------|-------------------------------|---------|--------------|----------|
| Neuron   | Neuron | 5             | parkinglotnerds8c_AI_tub48.h5  | 10+       | 17.88        | 0.06      |
| Paul   | donkey1| 5              | parkinglotnerds8.h5           | 13+      | 17.92        | 75       |
| Paul   | Neuron | 5             | parkinglotnerds8c_AI_tub48.h5  | 8       | 17.95        | 75      |
| Paul   | TawnTraining | 5             | parkinglotnerds8c_AI_tub48.h5  | 11+       | 17.98        | 85      |
| Neuron   | Neuron | 5l             | parkinglotnerds8c_AI_tub48.h5  | 10       | 18.20        | 0.06      |
| Tawn   | Paul   | manage.py      | ver02-slided200           | 3       | 18.26        | 80       |
| Tawn   | donkey1| 5              | parkinglotnerds8.h5           | 21      | 18.34        | 80       |
| Paul   | TawnTraining| 5              | parkinglotnerds8.h5           | 15+      | 18.43        | 75       |
| Tawn   | colab  | 5              | parkinglotnerds8.h5           | 10      | 18.54        | 160       |
| Tawn   | donkey1| 4              | parkinglotnerds8.h5           | 3       | 18.60        | 80       |
| Tawn   | donkey1| 5              | paul-tub20-ver01.h5           | 4       | 18.78        | 80      |
| Paul   | donkey1| 0              | parkinglotnerds8.h5           | 10+      | 19.06        | 75       |
| Tawn   | Colab  | 0              | paul-tub20-ver01.h5           | 6       | 19.32        | 160      |
| Tawn   | donkey1| 0              | parkinglotnerds8.h5           | 13      | 19.46        | 80       |
| Tawn   | Colab  | 5              | parkinglotnerds8.h5           | 10      | 19.50        | 160       |
| Tawn   | Colab  | 0              | parkinglotnerds8.h5           | 7+      | 19.66        | 160      |
| Paul   | TawnTraing  | 0              | parkinglotnerds8.h5           | 15+      | 19.73        | 85      |
| Tawn   | Neuron | 0              | paul-tub20-ver01.h5           | 2       | 19.80        | 220      |
| Tawn   | Colab  | 2              | parkinglotnerds8.h5           | 3       | 19.86        | 160      |
| Tawn   | Colab  | 0              | parkinglotnerds14.h5          | 2       | 19.78        | 160      |
| Tawn   | Colab  | 5             | parkinglotnerds8c_AI_tub48.h5  | 3       | 19.98        | 160      |
| Tawn   | Colab  | 0              | parkinglotnerds12.h5          | 6       | 20.10        | 160      |
| Tawn   | Colab  | 0              | parkinglotnerds13.h5          | 2       | 20.36        | 160      |
| Tawn   | Colab  | 0              | parkinglotnerds10.h5          | 2       | 20.74        | 220      |
| Tawn   | Colab  | 4              | parkinglotnerds8.h5           | 3       | 20.80        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds5.h5           | 3       | 20.90        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds3.h5           | 2       | 21.88        | 220      |
| Tawn   | Colab  | 2              | paul-tub20-ver01-slide200.h5  | 1       | 21.76        | 220      |
| Tawn   | Colab  | 2              | parkinglotnerds1.h5           | 3       | 22.04        | 220      |
| Tawn   | Colab  | 0              | paul-tub21-ver01.h5           | 1       | 22.94        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds7.h5           | 1       | 24.10        | 220      |
| Tawn   | Neuron | 0              | parkinglotnerds8.h5           | 2       | 24.30        | 0.05     |
| Tawn   | Colab  | 2              | paul-tub20-ver01.h5           | 1       | 24.94        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerdsAI_tub48.h5    | 1       | 24.72        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds16.h5          | 2       | 23.00        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds4.h5           | 1       | 24.82        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds2.h5           | 1       | 25.20        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds15.h5          | 2+      | 35.72        | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds8c_AI_tub48.h5 | 0       | DQ           | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds11.h5          | DQ      |              | 220      |
| Tawn   | Colab  | 0              | parkinglotnerds6.h5           | DQ      |              | 220      |
| Tawn   | Colab  | 2              | paul-tub21-ver01.h5           | DQ      |              | 220      |
| Tawn   | Colab  | 4              | paul-tub20-ver01.h5           | DQ      |              | 220      |
| Tawn   | Colab  | 0              | paul-tub21-ver01.h5           | DQ      |              | 220      |

(donkey_ottawa) rainer@neuron:~/dev/40-VirtualRacing/scripts$ python racer_pln5l.py --model=../models/parkinglotnerds8c_AI_tu8.h5 --host=127.0.0.1 --name pln8
