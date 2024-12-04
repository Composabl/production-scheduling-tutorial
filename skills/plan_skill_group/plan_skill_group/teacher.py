import math

import numpy as np
from composabl import Teacher, SkillTeacher
from plan_skill_group.sensors import sensors

# The BaseTeacher class defines the logic for teaching an agent in a planning scenario.
class BaseTeacher(SkillTeacher):
    def __init__(self, *args, **kwargs):
        """
        Initializes the BaseTeacher with tracking variables for observations, rewards, errors, and actions.
        """
        self.obs_history = None  # Tracks the history of sensor observations.
        self.reward_history = []  # Stores calculated rewards for the agent.
        self.last_reward = 0  # Stores the most recent reward value.
        self.error_history = []  # Tracks errors (if applicable in reward calculations).
        self.action_history = []  # Keeps a record of actions taken by the agent.
        self.colors = []  # Placeholder for additional metadata (e.g., visualization markers).
        self.count = 0  # Counter for the number of reward calculations.

    async def transform_sensors(self, obs, action):
        """
        Prepares or modifies sensor observations before use.
        Currently, this method passes observations unchanged.
        """
        return obs

    async def transform_action(self, transformed_obs, action):
        """
        Adjusts or processes the action before it is executed.
        Currently, this method passes the action unchanged.
        """
        return action

    async def filtered_sensor_space(self):
        """
        Specifies which sensors are relevant for this teacher.
        Returns the list of sensor names defined in the 'sensors' module.
        """
        return [s.name for s in sensors]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        """
        Calculates the reward signal for the agent based on the current state and action.
        
        Args:
            transformed_obs: The processed sensor data.
            action: The action taken by the agent.
            sim_reward: A simulation-provided reward value (scaled in this implementation).

        Returns:
            reward: The calculated reward value for the agent.
        """
        # Initialize observation history if this is the first step
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0  # No reward at the first step
        else:
            # Append the current observation to the history
            self.obs_history.append(transformed_obs)

        # Scale the simulation reward
        reward = sim_reward / 100000

        # Log the reward and action in their respective histories
        self.reward_history.append(reward)
        self.action_history.append(action)

        # Increment the reward calculation count
        self.count += 1

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        """
        Optionally restricts the set of actions the agent can take.
        Returns None, indicating no restrictions.
        """
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        """
        Determines whether the agent has successfully completed its task.
        Currently, always returns False.
        """
        return False

    async def compute_termination(self, transformed_obs, action):
        """
        Determines whether to terminate the current training episode.
        Currently, always returns False, meaning the episode continues indefinitely.
        """
        return False