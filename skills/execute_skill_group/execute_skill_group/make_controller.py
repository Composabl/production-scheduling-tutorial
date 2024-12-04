import os
import sys

# Add parent directory to the Python path for module imports.
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import SkillController
from execute_skill_group.sensors import sensors

# The MakeCookieController class handles production logic for cookies.
class MakeCookieController(SkillController):
    def __init__(self, *args, **kwargs):
        """
        Initializes the MakeCookieController with tracking variables.
        Attributes:
            total_time: Cumulative time spent in production steps.
            obs_history: Records the history of sensor observations.
        """
        self.total_time = 0
        self.obs_history = []

    async def transform_sensors(self, obs):
        """
        Args:
            obs: Sensor data to process.

        Returns:
            The unmodified sensor data.
        """
        return obs

    async def filtered_sensor_space(self):
        """
        Returns:
            A list of sensor names relevant for cookie production.
        """
        return [s.name for s in sensors]

    async def compute_action(self, obs):
        """
        Determines the next action for cookie production based on the state of the environment.

        Args:
            obs: Current sensor data.

        Returns:
            action: The action to execute.
                - Mix, bake, or decorate actions are decided based on the state of mixers, ovens, and bakers.
        """
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i, j: (i, j), sensors_name, obs))
        self.total_time += 1

        # Append the current observation to history.
        self.obs_history.append(obs)

        action = 0  # Default to no action.

        ## Cookie Production Steps
        # MIX
        if obs['baker_1_time_remaining'] == 0:  # Chip
            action = 1
        elif obs['baker_2_time_remaining'] == 0:  # Coco
            action = 4
        elif obs['baker_3_time_remaining'] == 0:  # Eclair
            action = 7

        # BAKE
        if obs['baker_1_time_remaining'] == 0:  # Chip
            if obs['mixer_1_recipe'] == 1:
                action = 10
            elif obs['mixer_2_recipe'] == 1:
                action = 11
        elif obs['baker_2_time_remaining'] == 0:  # Coco
            if obs['mixer_1_recipe'] == 1:
                action = 12
            elif obs['mixer_2_recipe'] == 1:
                action = 13
        elif obs['baker_3_time_remaining'] == 0:  # Eclair
            if obs['mixer_1_recipe'] == 1:
                action = 14
            elif obs['mixer_2_recipe'] == 1:
                action = 15

        # DECORATE
        if obs['baker_1_time_remaining'] == 0:  # Chip
            if obs['oven_1_recipe'] == 1:
                action = 16
            elif obs['oven_2_recipe'] == 1:
                action = 17
            elif obs['oven_3_recipe'] == 1:
                action = 18
        elif obs['baker_3_time_remaining'] == 0:  # Eclair
            if obs['oven_1_recipe'] == 1:
                action = 19
            elif obs['oven_2_recipe'] == 1:
                action = 20
            elif obs['oven_3_recipe'] == 1:
                action = 21
        elif obs['baker_4_time_remaining'] == 0:  # Reesee
            if obs['oven_1_recipe'] == 1:
                action = 22
            elif obs['oven_2_recipe'] == 1:
                action = 23
            elif obs['oven_3_recipe'] == 1:
                action = 24

        return action

    async def compute_success_criteria(self, transformed_obs, action):
        """
        Defines the success criteria for cookie production.
        Currently always returns False (no success criteria defined).

        Args:
            transformed_obs: Processed observation data.
            action: Current action being executed.

        Returns:
            Boolean indicating whether success criteria have been met.
        """
        return False

    async def compute_termination(self, transformed_obs, action):
        """
        Defines the termination criteria for cookie production.
        Currently always returns False (no termination criteria defined).

        Args:
            transformed_obs: Processed observation data.
            action: Current action being executed.

        Returns:
            Boolean indicating whether the production episode should terminate.
        """
        return False

# The MakeCupcakeController class handles production logic for cupcakes.
# (The structure and comments are similar to MakeCookieController but adapted for cupcakes.)
# ...

# The MakeCakeController class handles production logic for cakes.
# (The structure and comments are similar to MakeCookieController but adapted for cakes.)
# ...

# The WaitController class provides a no-action state for idle periods.
class WaitController(SkillController):
    def __init__(self, *args, **kwargs):
        """
        Initializes the WaitController with tracking variables.
        Attributes:
            total_time: Cumulative time spent in idle state.
            obs_history: Records the history of sensor observations.
        """
        self.total_time = 0
        self.obs_history = []

    async def transform_sensors(self, obs):
        """
        Args:
            obs: Sensor data to process.

        Returns:
            The unmodified sensor data.
        """
        return obs

    async def filtered_sensor_space(self):
        """
        Returns:
            A list of sensor names relevant for waiting periods.
        """
        return [s.name for s in sensors]

    async def compute_action(self, obs):
        """
        Executes no action during idle periods.

        Args:
            obs: Current sensor data.

        Returns:
            action: Always returns 0 (no action).
        """
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i, j: (i, j), sensors_name, obs))
        self.total_time += 1

        # Append the current observation to history.
        self.obs_history.append(obs)

        action = 0  # No action during wait.
        return action

    async def compute_success_criteria(self, transformed_obs, action):
        """
        Defines the success criteria for idle periods.
        Currently always returns False (no success criteria defined).
        """
        return False

    async def compute_termination(self, transformed_obs, action):
        """
        Defines the termination criteria for idle periods.
        Currently always returns False (no termination criteria defined).
        """
        return False