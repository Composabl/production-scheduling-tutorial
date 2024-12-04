import math
import numpy as np
from composabl import Teacher, SkillTeacher
from produce_w_mask.sensors import sensors

# The BaseTeacher class defines a skill teacher for a production scenario,
# integrating functionality for reward computation, action masking, and task-specific logic.
class BaseTeacher(SkillTeacher):
    def __init__(self, *args, **kwargs):
        """
        Initializes the teacher with attributes to track observations, rewards,
        actions, and metadata for the teaching process.
        """
        self.obs_history = None  # Tracks all observed sensor data across steps.
        self.reward_history = []  # Records the rewards calculated at each step.
        self.last_reward = 0  # Stores the most recent reward value.
        self.error_history = []  # Placeholder for error metrics, if needed.
        self.action_history = []  # Logs all actions taken during the process.
        self.colors = []  # Placeholder for future extensions (e.g., state metadata).
        self.count = 0  # Counter for tracking the number of rewards computed.

    async def transform_sensors(self, obs, action):
        """
        Transforms or preprocesses the sensor data before usage.
        Currently, it returns the data unchanged.
        """
        return obs

    async def transform_action(self, transformed_obs, action):
        """
        Transforms or adjusts the action before execution.
        Currently, it returns the action unchanged.
        """
        return action

    async def filtered_sensor_space(self):
        """
        Specifies the subset of sensors relevant for this teacher.
        Returns:
            list: Names of the relevant sensors as defined in 'produce_w_mask.sensors'.
        """
        return [s.name for s in sensors]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        """
        Computes the reward signal for the agent based on simulation feedback.

        Args:
            transformed_obs: The processed observation data.
            action: The action executed by the agent.
            sim_reward: The raw reward provided by the simulation.

        Returns:
            float: The scaled reward value.
        """
        # Initialize observation history on the first step.
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0  # No reward for the initial step.

        # Append the current observation to the history.
        self.obs_history.append(transformed_obs)

        # Scale the simulation reward for more manageable values.
        reward = sim_reward / 100000

        # Log the computed reward and action for tracking.
        self.reward_history.append(reward)
        self.action_history.append(action)

        # Increment the computation counter.
        self.count += 1

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        """
        Generates an action mask to restrict the agent's available actions.
        In this case, it maps the first 25 transformed observations to integers.

        Args:
            transformed_obs: The processed observation data.
            action: The action being evaluated.

        Returns:
            np.array: A binary mask array indicating allowed actions.
        """
        action_mask = [int(x) for x in list(transformed_obs.values())[:25]]
        return np.array(action_mask)

    async def compute_success_criteria(self, transformed_obs, action):
        """
        Determines whether the task has been successfully completed.
        Returns:
            bool: Always False, as success criteria are not defined here.
        """
        return False

    async def compute_termination(self, transformed_obs, action):
        """
        Determines whether the current task or training episode should terminate.
        Returns:
            bool: Always False, allowing indefinite episodes.
        """
        return False