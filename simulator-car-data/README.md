# Car Data of the simulator

1. Link to simulator repository: https://github.com/tawnkramer/sdsandbox

2. Car Data as of August, 2nd, 2020

| data                   | unit | simulator     | remark             |
|------------------------|------|---------------|--------------------|     
| mass                   | kg   | 500           |                    |
| length                 | m    | 1.7           |                    |
| wheel radius           | m    | 0.32          | needs confirmation |
| car track width, front | m    | 1.398         |                    |
| car track width, rear  | m    | 1.380         |                    |
| braking torque         | Nm   | 400           |                    |
| motor torque           | Nm   | 450           |                    |
| maximum speed          | m/s  | 50            |                    |
| maximum steering angle | deg  | 25            | tricky: in the code 16, after spawning maxSteer=45, but checking with joystick = 25 |
| drag                   | ---  | 0.1           |                    |
| angular drag           | ---  | 0.05          |                    |
| local center of mass   | m    | (0, -0.122, 0.085) | XYZ Unity left-handed coordinate system |
|                        |      |               |                    |
| m_ForwardFriction      |      |               |                    |
| m_ExtremumSlip         | ---  | 0.4           |                    |
| m_ExtremumValue        | ---  | 1             |                    |
| m_AsymptoteSlip        | ---  | 0.8           |                    |
| m_AsymptoteValue       | ---  | 0.5           |                    |
| m_Stiffness            | ---  | 1             |                    |
  m_SidewaysFriction:
    m_ExtremumSlip: 0.2
    m_ExtremumValue: 1
    m_AsymptoteSlip: 0.5
    m_AsymptoteValue: 0.75
    m_Stiffness: 1
