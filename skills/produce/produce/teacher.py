import math
import numpy as np
from composabl import Teacher, SkillTeacher
from produce.sensors import sensors

# The BaseTeacher class defines a foundational skill teacher for a production-oriented scenario.
# It handles sensor transformations, reward computation, action masking, and task-specific logic.
class BaseTeacher(SkillTeacher):
    def __init__(self, *args, **kwargs):
        """
        Initializes the teacher with variables to manage observation history,
        rewards, actions, and metadata tracking.
        """
        self.obs_history = None  # Keeps track of all observed sensor data.
        self.reward_history = []  # Stores calculated rewards for analysis.
        self.last_reward = 0  # Tracks the most recent reward value.
        self.error_history = []  # (Optional) Tracks error metrics for debugging or analysis.
        self.action_history = []  # Records the sequence of actions taken by the agent.
        self.colors = []  # Placeholder for potential visual or state metadata.
        self.count = 0  # Counter for the number of rewards computed.

    async def transform_sensors(self, obs, action):
        """
        Prepares or transforms sensor data for further processing.
        Currently, this is a pass-through method.
        """
        return obs

    async def transform_action(self, transformed_obs, action):
        """
        Adjusts the action before execution, if necessary.
        Currently, this is a pass-through method.
        """
        return action

    async def filtered_sensor_space(self):
        """
        Defines the subset of sensors relevant for this teacher.
        Returns:
            A list of sensor names as defined in the 'produce.sensors' module.
        """
        return [s.name for s in sensors]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        """
        Computes the reward for the agent's action based on simulation data.

        Args:
            transformed_obs: The processed observation data.
            action: The action taken by the agent.
            sim_reward: The simulation-provided reward.

        Returns:
            float: The scaled reward value.
        """
        # Initialize the observation history if this is the first step.
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0  # No reward for the initial step.

        # Add the current observation to the observation history.
        self.obs_history.append(transformed_obs)

        # Scale the simulation reward for this use case.
        reward = sim_reward / 100000

        # Log the reward and action for history tracking.
        self.reward_history.append(reward)
        self.action_history.append(action)

        # Increment the reward computation counter.
        self.count += 1

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        """
        Defines an action mask to restrict available actions for the agent.
        Returns:
            None: Indicates no restrictions are applied in this implementation.
        """
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        """
        Determines whether the task has been successfully completed.
        Returns:
            bool: Always False, indicating no success criteria are defined yet.
        """
        return False

    async def compute_termination(self, transformed_obs, action):
        """
        Determines whether the current training or task episode should terminate.
        Returns:
            bool: Always False, indicating episodes continue indefinitely.
        """
        return False