from typing import Dict, List

from composabl_core import SkillController
import numpy as np
from rule_based_controller.sensors import sensors
from rule_based_controller.make_controller import (
    MakeCakeController,
    MakeCookieController,
    MakeCupcakeController,
)

# The Controller class is a rule-based skill controller.
# It prioritizes production tasks for cakes, cupcakes, and cookies based on demand and completion status.
class Controller(SkillController):
    def __init__(self, *args, **kwargs):
        """
        Initializes the Controller with tracking variables.
        Attributes:
            count: Tracks the number of iterations or steps.
            action_count: Placeholder for the number of actions taken (not actively used).
            make_cake: Boolean indicating whether the system should prioritize cake production.
            make_cupcake: Boolean indicating whether the system should prioritize cupcake production.
            make_cookie: Boolean indicating whether the system should prioritize cookie production.
        """
        self.count = 0
        self.action_count = 1

        # Flags for production priorities
        self.make_cake = True
        self.make_cupcake = True
        self.make_cookie = True

    # Determines the next action based on demand and completion status.
    async def compute_action(self, obs, action):
        """
        Args:
            obs: Current sensor data (observations).
            action: Placeholder for the computed action.

        Returns:
            action: The computed action for the current step.
                - 0: Wait (no action needed).
                - Invokes specific MakeXController actions for cakes, cupcakes, or cookies.
        """
        old_obs = obs.copy()  # Preserve the original observations.
        sensors_name = [s.name for s in sensors]

        # Convert observations into a dictionary if they are not already.
        obs = dict(map(lambda i, j: (i, j), sensors_name, obs))

        # Default action is to wait (action = 0).
        action = 0
        self.count += 1

        # Flags for unmet demands.
        x1 = 0  # Cookies.
        x2 = 0  # Cupcakes.
        x3 = 0  # Cakes.

        # Retrieve demand and completion status for each product.
        dem_cake = obs['cake_demand']
        dem_cupcake = obs['cupcake_demand']
        dem_cookie = obs['cookies_demand']

        # If all demands are met, no further action is required.
        if (
            obs['completed_cake'] >= dem_cake and
            obs['completed_cupcakes'] >= dem_cupcake and
            obs['completed_cookies'] >= dem_cookie
        ):
            return action  # Return default wait action.

        # Determine unmet demands.
        if obs['completed_cake'] < dem_cake:
            x3 = 1  # Cake demand unmet.
        if obs['completed_cupcakes'] < dem_cupcake:
            x2 = 1  # Cupcake demand unmet.
        if obs['completed_cookies'] < dem_cookie and (x3 + x2 < 2):
            self.make_cookie = True
            x1 = 1  # Cookie demand unmet.

        # Handle cake production if prioritized and demand is unmet.
        if self.make_cake and x3 == 1:
            print('Produce Cake')
            action = MakeCakeController().compute_action(old_obs)
            self.make_cake = False
            self.make_cupcake = True
            self.make_cookie = True
            return action

        # Handle cupcake production if prioritized and demand is unmet.
        if self.make_cupcake and x2 == 1:
            print('Produce Cupcake')
            action = MakeCupcakeController().compute_action(old_obs)
            self.make_cake = True
            self.make_cupcake = False
            self.make_cookie = True
            return action

        # Handle cookie production if prioritized and demand is unmet.
        if self.make_cookie and x1 == 1:
            print('Produce Cookie')
            action = MakeCookieController().compute_action(old_obs)
            self.make_cake = True
            self.make_cupcake = True
            self.make_cookie = False
            return action

        return action  # Default action (wait).

    # Specifies the sensors relevant for this controller.
    async def filtered_sensor_space(self):
        """
        Returns:
            A list of sensor names relevant to the controller.
        """
        return [s.name for s in sensors]

    # Placeholder for success criteria.
    # Always returns False as success criteria are not defined in this implementation.
    async def compute_success_criteria(self, transformed_obs, action):
        """
        Args:
            transformed_obs: Processed sensor data.
            action: Current action taken by the agent.

        Returns:
            Boolean indicating whether success criteria have been met.
        """
        return False

    # Placeholder for termination criteria.
    # Always returns False as termination criteria are not defined in this implementation.
    async def compute_termination(self, transformed_obs, action):
        """
        Args:
            transformed_obs: Processed sensor data.
            action: Current action taken by the agent.

        Returns:
            Boolean indicating whether the production episode should terminate.
        """
        return False