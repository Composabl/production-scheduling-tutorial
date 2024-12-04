import os
import sys

# Add the parent directory to the Python path for module resolution
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import SkillController
from optimization_benchmark.sensors import sensors


# Controller for managing cookie production
class MakeCookieController(SkillController):
    def __init__(self, *args, **kwargs):
        # Initialize variables to track total time and observation history
        self.total_time = 0
        self.obs_history = []

    async def transform_sensors(self, obs):
        # Pass the raw observations as-is; this method can be extended for preprocessing
        return obs

    async def filtered_sensor_space(self):
        # Return the relevant sensor names for cookie production
        return [s.name for s in sensors]

    async def compute_action(self, obs, action):
        # Convert observations to a dictionary format using sensor names
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i, j: (i, j), sensors_name, obs))
        self.total_time += 1  # Increment the total time counter
        self.obs_history.append(obs)  # Append the observation to history

        action = 0  # Default action: no operation

        ## COOKIES
        # MIX step
        if obs['baker_1_time_remaining'] == 0:  # Example: chip cookies
            action = 1
        elif obs['baker_2_time_remaining'] == 0:  # Example: cocoa cookies
            action = 4
        elif obs['baker_3_time_remaining'] == 0:  # Example: eclair cookies
            action = 7

        # BAKE step
        if obs['baker_1_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 1:
                action = 10
            elif obs['mixer_2_recipe'] == 1:
                action = 11
        elif obs['baker_2_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 1:
                action = 12
            elif obs['mixer_2_recipe'] == 1:
                action = 13
        elif obs['baker_3_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 1:
                action = 14
            elif obs['mixer_2_recipe'] == 1:
                action = 15

        # DECORATE step
        if obs['baker_1_time_remaining'] == 0:
            if obs['oven_1_recipe'] == 1:
                action = 16
            elif obs['oven_2_recipe'] == 1:
                action = 17
            elif obs['oven_3_recipe'] == 1:
                action = 18
        elif obs['baker_3_time_remaining'] == 0:
            if obs['oven_1_recipe'] == 1:
                action = 19
            elif obs['oven_2_recipe'] == 1:
                action = 20
            elif obs['oven_3_recipe'] == 1:
                action = 21
        elif obs['baker_4_time_remaining'] == 0:  # Example: Reese cookies
            if obs['oven_1_recipe'] == 1:
                action = 22
            elif obs['oven_2_recipe'] == 1:
                action = 23
            elif obs['oven_3_recipe'] == 1:
                action = 24

        return action

    async def compute_success_criteria(self, transformed_obs, action):
        # Define criteria for success (e.g., completing all batches)
        return False

    async def compute_termination(self, transformed_obs, action):
        # Define termination conditions for the process
        return False


# Controller for managing cupcake production
class MakeCupcakeController(SkillController):
    def __init__(self, *args, **kwargs):
        self.total_time = 0
        self.obs_history = []

    async def transform_sensors(self, obs):
        return obs

    async def filtered_sensor_space(self):
        return [s.name for s in sensors]

    async def compute_action(self, obs):
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i, j: (i, j), sensors_name, obs))
        self.total_time += 1
        self.obs_history.append(obs)

        action = 0

        ## CUPCAKES
        # MIX step
        if obs['baker_1_time_remaining'] == 0:
            action = 2
        elif obs['baker_2_time_remaining'] == 0:
            action = 5
        elif obs['baker_3_time_remaining'] == 0:
            action = 8

        # BAKE step
        if obs['baker_1_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 2:
                action = 10
            elif obs['mixer_2_recipe'] == 2:
                action = 11
        elif obs['baker_2_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 2:
                action = 12
            elif obs['mixer_2_recipe'] == 2:
                action = 13
        elif obs['baker_3_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 2:
                action = 14
            elif obs['mixer_2_recipe'] == 2:
                action = 15

        # DECORATE step
        if obs['baker_1_time_remaining'] == 0:
            if obs['oven_1_recipe'] == 2:
                action = 16
            elif obs['oven_2_recipe'] == 2:
                action = 17
            elif obs['oven_3_recipe'] == 2:
                action = 18
        elif obs['baker_3_time_remaining'] == 0:
            if obs['oven_1_recipe'] == 2:
                action = 19
            elif obs['oven_2_recipe'] == 2:
                action = 20
            elif obs['oven_3_recipe'] == 2:
                action = 21
        elif obs['baker_4_time_remaining'] == 0:
            if obs['oven_1_recipe'] == 2:
                action = 22
            elif obs['oven_2_recipe'] == 2:
                action = 23
            elif obs['oven_3_recipe'] == 2:
                action = 24

        return action

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False


# Controller for managing cake production
class MakeCakeController(SkillController):
    def __init__(self, *args, **kwargs):
        self.total_time = 0
        self.obs_history = []

    async def transform_sensors(self, obs):
        return obs

    async def filtered_sensor_space(self):
        return [s.name for s in sensors]

    async def compute_action(self, obs):
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i, j: (i, j), sensors_name, obs))
        self.total_time += 1
        self.obs_history.append(obs)

        action = 0

        ## CAKES
        # MIX step
        if obs['baker_1_time_remaining'] == 0:
            action = 3
        elif obs['baker_2_time_remaining'] == 0:
            action = 6
        elif obs['baker_3_time_remaining'] == 0:
            action = 9

        # BAKE step
        if obs['baker_1_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 3:
                action = 10
            elif obs['mixer_2_recipe'] == 3:
                action = 11
        elif obs['baker_2_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 3:
                action = 12
            elif obs['mixer_2_recipe'] == 3:
                action = 13
        elif obs['baker_3_time_remaining'] == 0:
            if obs['mixer_1_recipe'] == 3:
                action = 14
            elif obs['mixer_2_recipe'] == 3:
                action = 15

        # DECORATE step
        if obs['baker_1_time_remaining'] == 0:
            if obs['oven_1_recipe'] == 3:
                action = 16
            elif obs['oven_2_recipe'] == 3:
                action = 17
            elif obs['oven_3_recipe'] == 3:
                action = 18
        elif obs['baker_3_time_remaining'] == 0:
            if obs['oven_1_recipe'] == 3:
                action = 19
            elif obs['oven_2_recipe'] == 3:
                action = 20
            elif obs['oven_3_recipe'] == 3:
                action = 21
        elif obs['baker_4_time_remaining'] == 0:
            if obs['oven_1_recipe'] == 3:
                action = 22
            elif obs['oven_2_recipe'] == 3:
                action = 23
            elif obs['oven_3_recipe'] == 3:
                action = 24

        return action

    async def compute_success_criteria(self, transformed_obs, action):
        # Define criteria for success (e.g., completing all cake batches)
        return False

    async def compute_termination(self, transformed_obs, action):
        # Define termination conditions for the process
        return False


# Controller for managing waiting periods
class WaitController(SkillController):
    def __init__(self, *args, **kwargs):
        # Initialize variables to track total time and observation history
        self.total_time = 0
        self.obs_history = []

    async def transform_sensors(self, obs):
        # Pass the raw observations as-is; this method can be extended for preprocessing
        return obs

    async def filtered_sensor_space(self):
        # Return the relevant sensor names during wait periods
        return [s.name for s in sensors]

    async def compute_action(self, obs):
        # Convert observations to a dictionary format using sensor names
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i, j: (i, j), sensors_name, obs))
        self.total_time += 1  # Increment the total time counter
        self.obs_history.append(obs)  # Append the observation to history

        action = 0  # Default action: no operation during waiting

        return action

    async def compute_success_criteria(self, transformed_obs, action):
        # Define criteria for success during waiting (if applicable)
        return False

    async def compute_termination(self, transformed_obs, action):
        # Define termination conditions during waiting periods
        return False