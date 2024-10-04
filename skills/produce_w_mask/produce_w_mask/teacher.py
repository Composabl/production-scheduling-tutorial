import math

import numpy as np
from composabl import Teacher, SkillTeacher
from produce_w_mask.sensors import sensors

class BaseTeacher(SkillTeacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.action_history = []
        self.colors = []
        self.last_reward = 0
        self.count = 0

    async def transform_sensors(self, obs, action):
        return obs

    async def transform_action(self, transformed_obs, action):
        return action

    async def filtered_sensor_space(self):
        return [s.name for s in sensors]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        reward = sim_reward/100000

        self.reward_history.append(reward)
        self.action_history.append(action)

        self.count += 1

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        action_mask = [int(x) for x in list(transformed_obs.values())[:25]]
        return np.array(action_mask)

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False
