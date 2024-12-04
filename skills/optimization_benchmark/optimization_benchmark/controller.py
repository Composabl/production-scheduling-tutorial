from typing import Dict, List
from composabl_core import SkillController
import numpy as np
from optimization_benchmark.sensors import sensors
from gekko import GEKKO
from optimization_benchmark.make_controller import (
    MakeCakeController,
    MakeCookieController,
    MakeCupcakeController,
)

# The Controller class serves as the benchmark implementation for production scheduling.
# It uses GEKKO for optimization to maximize production efficiency and revenue.
class Controller(SkillController):
    def __init__(self, *args, **kwargs):
        """
        Initializes the controller with a GEKKO optimization model and production logic.
        Attributes:
            count: Tracks the number of time steps in the production schedule.
            action_count: Tracks the current action index in the GEKKO optimization results.
            m: The GEKKO model instance for optimizing production decisions.
            u1, u2, u3: Manipulated variables representing the production decision for each product.
            wt: A state variable representing the planned wait time for production.
            make_cake, make_cupcake, make_cookie: Flags to coordinate production order among products.
        """
        self.count = 0
        self.action_count = 1

        # Initialize the GEKKO optimization model
        self.m = GEKKO(remote=False)
        nt = 10  # Number of time steps
        self.m.time = [i for i in range(0, nt)]

        # Define manipulated variables for production decisions
        self.u1 = self.m.MV(value=0, lb=0, ub=1, integer=True)  # Produce cookies
        self.u2 = self.m.MV(value=0, lb=0, ub=1, integer=True)  # Produce cupcakes
        self.u3 = self.m.MV(value=0, lb=0, ub=1, integer=True)  # Produce cakes

        # Define state variables for quantities, wait time, and revenue
        q = self.m.SV(value=0, lb=0, integer=True)  # Quantity produced
        self.wt = self.m.SV(value=0, lb=0, ub=480, integer=True)  # Wait time
        r = self.m.SV(value=0, lb=0, ub=5000, integer=True)  # Revenue

        # Allow the optimizer to adjust the manipulated variables
        self.u1.STATUS = 1
        self.u2.STATUS = 1
        self.u3.STATUS = 1

        # Define production quantities and prices
        quantities = {1: 12, 2: 6, 3: 1}
        prices = {1: 5, 2: 7, 3: 10}

        # Add equations to model production dynamics, constraints, and objectives
        self.m.Equations([
            q.dt() == 12 * self.u1 + 6 * self.u2 + 1 * self.u3,
            self.wt.dt() == self.m.max2(self.m.max2(28 * self.u1, 57 * self.u2), 80 * self.u3),
            self.wt <= 480,  # Ensure wait time does not exceed available time
            r.dt() == 12 * 5 * self.u1 + 6 * 7 * self.u2 + 1 * 10 * self.u3,  # Revenue calculation
            self.u1 + self.u2 + self.u3 <= 2  # Limit to producing two products simultaneously
        ])

        # Define the objective to maximize revenue
        self.m.Maximize(r)

        # Set the optimization mode
        self.m.options.IMODE = 6  # Optimal control mode

        # Solve the optimization problem
        self.display_mpc_vals = False
        self.m.solve(disp=self.display_mpc_vals)

        # Initialize production flags
        self.make_cake = True
        self.make_cupcake = True
        self.make_cookie = True

    async def reset(self):
        """
        Resets the controller to its initial state, reinitializing the GEKKO model.
        """
        self.__init__()  # Reinitialize the controller

    async def compute_action(self, obs, action):
        """
        Determines the next action based on the optimized GEKKO plan.
        Args:
            obs: Current observations from the environment.
            action: The previous action taken (not used here).

        Returns:
            The next production action to execute.
        """
        action = 0  # Default action is to wait
        self.count += 1

        # Extract production plans from the GEKKO optimization results
        x1 = [int(x) for x in self.u1.value]
        x2 = [int(x) for x in self.u2.value]
        x3 = [int(x) for x in self.u3.value]
        self.x1 = x1

        wt = [int(x) for x in self.wt.value]

        # If no more actions are planned, return the wait action
        if self.action_count >= len(wt):
            return action

        wt_plan = wt[self.action_count]

        if self.count < wt_plan:
            # Execute the production actions based on the GEKKO plan
            if self.make_cake and x3[self.action_count] == 1:
                action = MakeCakeController().compute_action(obs)
                self.make_cake = False
                self.make_cupcake = True
                self.make_cookie = True
                return action

            if self.make_cupcake and x2[self.action_count] == 1:
                action = MakeCupcakeController().compute_action(obs)
                self.make_cake = True
                self.make_cupcake = False
                self.make_cookie = True
                return action

            if self.make_cookie and x1[self.action_count] == 1:
                action = MakeCookieController().compute_action(obs)
                self.make_cake = True
                self.make_cupcake = True
                self.make_cookie = False
                return action

        else:
            # Advance to the next action in the plan
            self.action_count += 1

        return action

    async def compute_termination(self, transformed_obs, action):
        """
        Determines whether to terminate the current episode.
        Returns True if all actions in the plan have been executed.
        """
        if self.action_count > len(self.x1):
            return True
        else:
            return False

    async def filtered_sensor_space(self):
        """
        Filters the list of sensors to include only those relevant for this skill.
        """
        return [s.name for s in sensors]

    async def compute_success_criteria(self, transformed_obs, action):
        """
        Evaluates whether the agent has successfully completed its task.
        Currently, this always returns False.
        """
        return False