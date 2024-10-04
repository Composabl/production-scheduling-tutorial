# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import time

from composabl_core import PerceptorImpl
from demand_predict.sensors import sensors

class DemoPerceptor(PerceptorImpl):
    def __init__(self, *args, **kwargs):
        self.previous_value = None
        self.previous_time = None

    async def compute(self, obs_spec, obs):
        sensor_names = [s.name for s in sensors]
        obs_dict = dict(map(lambda i,j : (i,j), sensor_names, obs))
        # change obs to dictionary using sensors
        if type(obs) != dict:
            obs = dict(zip(sensor_names, obs))

        #Heuristic
        co = int(1.3 * float(obs["cookies_demand"]))
        cp = int(1.1 * float(obs["cupcake_demand"]))
        ck = int(1.05 * float(obs["cake_demand"]))

        return {"cookies_demand_predict": co, "cupcake_demand_predict": cp, "cake_demand_predict": ck}

    def filtered_sensor_space(self, obs):
        return [s.name for s in sensors]
