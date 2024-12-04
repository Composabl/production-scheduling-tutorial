from typing import Dict, List

from composabl_core import SkillController

import numpy as np
from execute_skill_group.sensors import sensors
from execute_skill_group.make_controller import (
    MakeCakeController,
    MakeCookieController,
    MakeCupcakeController,
)

# The Controller class manages the execution of production skills for cakes, cupcakes, and cookies.
# It ensures that demand for each product is met while cycling between production tasks.
class Controller(SkillController):
    def __init__(self, *args, **kwargs):
        """
        Initializes the Controller with tracking variables.
        Attributes:
            count: Tracks the number of steps or iterations.
            action_count: Tracks the number of actions taken (not currently used).
            make_cake: Boolean indicating whether the system should prioritize producing cakes.
            make_cupcake: Boolean indicating whether the system should prioritize producing cupcakes.
            make_cookie: Boolean indicating whether the system should prioritize producing cookies.
        """
        self.count = 0
        self.action_count = 1

        # Production priorities
        self.make_cake = True
        self.make_cupcake = True
        self.make_cookie = True

    # Computes the action to be taken based on product demands and completed quantities.
    # The controller alternates between producing cakes, cupcakes, and cookies based on demand.
    async def compute_action(self, obs, action):
        """
        Args:
            obs: Observations or sensor data from the environment.
            action: Placeholder for the computed action.

        Returns:
            action: The computed action for the current step.
        """
        old_obs = obs.copy()  # Keep a copy of the original observations.
        sensors_name = [s.name for s in sensors]

        # Convert observations to a dictionary if they are not already.
        if type(obs) != dict:
            obs = dict(zip(sensors_name, obs))

        # Default action: wait (action = 0).
        action = 0
        self.count += 1

        # Flags to indicate unmet demands for each product.
        x1 = 0  # Cookies.
        x2 = 0  # Cupcakes.
        x3 = 0  # Cakes.

        # Add noise to demand values to simulate variability in production requirements.
        obs['cookies_demand'] = float(obs['cookies_demand']) * (1 + action * 0.01)
        obs['cupcake_demand'] = float(obs['cupcake_demand']) * (1 + action * 0.01)
        obs['cake_demand'] = float(obs['cake_demand']) * (1 + action * 0.01)

        # Retrieve demand and completed quantities for each product.
        dem_cake = obs['cake_demand']
        dem_cupcake = obs['cupcake_demand']
        dem_cookie = obs['cookies_demand']

        # Check if all demands are met.
        if (
            obs['completed_cake'] >= dem_cake and
            obs['completed_cupcakes'] >= dem_cupcake and
            obs['completed_cookies'] >= dem_cookie
        ):
            return action  # No action required if all demands are satisfied.

        # Determine unmet demands.
        if obs['completed_cake'] < dem_cake:
            x3 = 1  # Cake demand unmet.
        if obs['completed_cupcakes'] < dem_cupcake:
            x2 = 1  # Cupcake demand unmet.
        if obs['completed_cookies'] < dem_cookie and x3 + x2 < 2:
            self.make_cookie = True
            x1 = 1  # Cookie demand unmet.

        # Produce cakes if their demand is unmet and prioritized.
        if self.make_cake and x3 == 1:
            print('Produce Cake')
            action = MakeCakeController().compute_action(old_obs)
            self.make_cake = False
            self.make_cupcake = True
            self.make_cookie = True
            return action

        # Produce cupcakes if their demand is unmet and prioritized.
        if self.make_cupcake and x2 == 1:
            print('Produce Cupcake')
            action = MakeCupcakeController().compute_action(old_obs)
            self.make_cake = True
            self.make_cupcake = False
            self.make_cookie = True
            return action

        # Produce cookies if their demand is unmet and prioritized.
        if self.make_cookie and x1 == 1:
            print('Produce Cookie')
            action = MakeCookieController().compute_action(old_obs)
            self.make_cake = True
            self.make_cupcake = True
            self.make_cookie = False
            return action

        return action  # Default action (wait).

    # Specifies the sensors that are relevant for this controller.
    # Filters the sensor space to include only the names of defined sensors.
    async def filtered_sensor_space(self):
        """
        Returns:
            A list of sensor names relevant to this controller.
        """
        return [s.name for s in sensors]

    # Defines the success criteria for the skill.
    # This implementation does not define any success criteria and always returns False.
    async def compute_success_criteria(self, transformed_obs, action):
        """
        Args:
            transformed_obs: Processed sensor data.
            action: The current action taken by the agent.

        Returns:
            success: Boolean indicating whether the success criteria have been met.
        """
        return False

    # Determines whether to terminate the current training episode.
    # This implementation does not terminate episodes and always returns False.
    async def compute_termination(self, transformed_obs, action):
        """
        Args:
            transformed_obs: Processed sensor data.
            action: The current action taken by the agent.

        Returns:
            terminate: Boolean indicating whether the episode should terminate.
        """
        return False