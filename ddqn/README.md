# ToDo


- [x] code
```
        img_arr = img_arr.reshape((1,) + img_arr.shape)
        outputs = self.model.predict(img_arr)
        steering = outputs[0]
        throttle = outputs[1]
```
- [x] get_action(self, s_t): return linear_unbin(q_value[0])
- [ ] next_obs vs. obs for starting
- [ ] reward: speed > 0
- [reward function](https://github.com/tawnkramer/gym-donkeycar/blob/6f04b529f9712f4176c5b78096bc8768b7562dea/gym_donkeycar/envs/donkey_sim.py)
![](https://github.com/Heavy02011/50-donkey/blob/master/VirtualRacingLeague/21917BAC-404B-4342-A573-880DB8889101.jpeg)
