import math
import numpy as np
from composabl import Teacher, SkillTeacher
from learned_selector.sensors import sensors

# The BaseTeacher class is a custom teacher implementation for a learned selector.
# It tracks observations, rewards, and actions, and provides functionality to process sensor data and compute rewards.
class BaseTeacher(Teacher):
    def __init__(self, *args, **kwargs):
        """
        Initializes the BaseTeacher class with tracking variables.
        Attributes:
            obs_history: A list to store the history of observed sensor data.
            reward_history: A list to store the history of calculated rewards.
            last_reward: Stores the most recent reward value.
            error_history: A list to track any errors encountered during execution.
            action_history: A list to store the actions taken by the agent.
            colors: A list (currently unused) that can be extended for color-based decision-making or tracking.
            count: A counter to track the number of reward computations or steps.
        """
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.action_history = []
        self.colors = []
        self.count = 0

    # Processes sensor data if needed. By default, it returns the data unchanged.
    # Useful for normalizing, filtering, or preprocessing raw sensor values.
    async def transform_sensors(self, obs, action):
        """
        Args:
            obs: Observations or sensor data from the environment.
            action: The action being taken by the agent (not modified in this method).

        Returns:
            The unmodified sensor data (obs).
        """
        return obs

    # Modifies actions if needed before applying them in the environment.
    # By default, this function passes actions through unchanged.
    async def transform_action(self, transformed_obs, action):
        """
        Args:
            transformed_obs: Processed observation data from the environment.
            action: The action to be taken by the agent.

        Returns:
            The unmodified action.
        """
        return action

    # Specifies the sensors that are relevant for this teacher.
    # Filters the sensor space to include only those defined in the `sensors` module.
    async def filtered_sensor_space(self):
        """
        Returns:
            A list of sensor names relevant to this teacher.
        """
        return [s.name for s in sensors]

    # Computes the reward signal based on the simulation reward.
    # Rewards are scaled down for more manageable values.
    async def compute_reward(self, transformed_obs, action, sim_reward):
        """
        Args:
            transformed_obs: Processed observation data from the environment.
            action: The action taken by the agent.
            sim_reward: The reward provided by the simulation.

        Returns:
            reward: The scaled reward value.
        """
        # Initialize observation history if this is the first step.
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0  # No reward for the initial step.
        else:
            # Append the current observation to the history.
            self.obs_history.append(transformed_obs)

        # Scale the simulation reward for more manageable values.
        reward = sim_reward / 100000

        # Track the reward and action history.
        self.reward_history.append(reward)
        self.action_history.append(action)

        # Increment the step counter.
        self.count += 1

        return reward

    # Optionally restricts the agent's action space.
    # By default, this function imposes no restrictions (returns None).
    async def compute_action_mask(self, transformed_obs, action):
        """
        Args:
            transformed_obs: Processed observation data from the environment.
            action: The current action (not used in this implementation).

        Returns:
            None, indicating no action restrictions.
        """
        return None

    # Defines the success criteria for the skill.
    # This implementation does not define any success criteria and always returns False.
    async def compute_success_criteria(self, transformed_obs, action):
        """
        Args:
            transformed_obs: Processed observation data from the environment.
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
            transformed_obs: Processed observation data from the environment.
            action: The current action taken by the agent.

        Returns:
            terminate: Boolean indicating whether the episode should terminate.
        """
        return False