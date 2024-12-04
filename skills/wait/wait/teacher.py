import math
import numpy as np
from composabl import Teacher, SkillTeacher
from wait.sensors import sensors

# The BaseTeacher class defines a SkillTeacher for handling a "wait" state.
# It provides reward computation, sensor transformation, and task-specific logic.
class BaseTeacher(SkillTeacher):
    def __init__(self, *args, **kwargs):
        """
        Initializes the teacher with attributes for tracking observations, rewards,
        and actions, as well as metadata for the teaching process.
        """
        self.obs_history = None  # Keeps track of all observed sensor data.
        self.reward_history = []  # Stores the rewards computed during each step.
        self.last_reward = 0  # Holds the most recent reward value.
        self.error_history = []  # Placeholder for error metrics (unused).
        self.action_history = []  # Logs all actions performed.
        self.colors = []  # Placeholder for metadata or state classification.
        self.count = 0  # Counter for reward computation calls.

    async def transform_sensors(self, obs, action):
        """
        Transforms or preprocesses the sensor data before usage.
        Currently, this method returns the data unchanged.

        Args:
            obs: The original sensor data.
            action: The action corresponding to the observation.

        Returns:
            The unmodified observation data.
        """
        return obs

    async def transform_action(self, transformed_obs, action):
        """
        Overrides the action transformation to always return 0, representing a "wait" action.

        Args:
            transformed_obs: The processed observation data.
            action: The action to be transformed.

        Returns:
            int: A constant value of 0.
        """
        return 0

    async def filtered_sensor_space(self):
        """
        Specifies the subset of sensors relevant for this teacher.
        
        Returns:
            list: A list of sensor names from the 'wait.sensors' module.
        """
        return [s.name for s in sensors]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        """
        Computes the reward for the agent based on simulation feedback.

        Args:
            transformed_obs: The processed observation data.
            action: The action taken by the agent.
            sim_reward: The raw reward signal from the simulation.

        Returns:
            float: A scaled reward value.
        """
        # Initialize observation history if this is the first step.
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0  # No reward for the initial step.

        # Append the current observation to the history.
        self.obs_history.append(transformed_obs)

        # Scale the simulation reward to a smaller range for ease of use.
        reward = sim_reward / 100000

        # Log the reward and action for tracking purposes.
        self.reward_history.append(reward)
        self.action_history.append(action)

        # Increment the counter for computation steps.
        self.count += 1

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        """
        Specifies an action mask to restrict available actions for the agent.
        Currently, this returns None, indicating no restrictions.

        Args:
            transformed_obs: The processed observation data.
            action: The action being evaluated.

        Returns:
            None: No action masking is applied.
        """
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        """
        Determines whether the task has been successfully completed.
        
        Returns:
            bool: Always False, as success criteria are not defined here.
        """
        return False

    async def compute_termination(self, transformed_obs, action):
        """
        Determines whether the current episode or task should terminate.
        
        Returns:
            bool: Always False, allowing episodes to run indefinitely.
        """
        return False