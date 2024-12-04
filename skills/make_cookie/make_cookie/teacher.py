import math
import numpy as np
from composabl import Teacher, SkillTeacher
from make_cookie.sensors import sensors

# The BaseTeacher class manages training and evaluation for the cookie production skill.
# It includes logic for processing observations, computing rewards, and constraining actions.
class BaseTeacher(SkillTeacher):
    def __init__(self, *args, **kwargs):
        """
        Initializes the BaseTeacher with history tracking and counters.
        Attributes:
            obs_history: Tracks all observed sensor data during training.
            reward_history: Stores rewards calculated during training episodes.
            last_reward: Tracks the most recent reward for reference.
            error_history: Records any error metrics during training (not used in this implementation).
            action_history: Stores all actions taken during training episodes.
            colors: Placeholder for any additional data related to training (not currently used).
            count: Counter for the number of reward calculations.
        """
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.action_history = []
        self.colors = []
        self.last_reward = 0
        self.count = 0

    async def transform_sensors(self, obs, action):
        """
        Transforms the observed sensor data for use in training.
        Currently, this function is a pass-through.
        Args:
            obs: The raw sensor data from the environment.
            action: The action taken by the agent (not used here).

        Returns:
            The unmodified sensor data.
        """
        return obs

    async def transform_action(self, transformed_obs, action):
        """
        Transforms the agent's action before applying it to the environment.
        Currently, this function is a pass-through.
        Args:
            transformed_obs: The processed sensor data.
            action: The raw action to be transformed.

        Returns:
            The unmodified action.
        """
        return action

    async def filtered_sensor_space(self):
        """
        Filters the list of sensors to include only those relevant for training.
        This reduces unnecessary data and focuses on key variables.

        Returns:
            A list of sensor names relevant to the skill.
        """
        return [s.name for s in sensors]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        """
        Computes the reward signal based on the current state of the environment.
        For this teacher, the reward is directly tied to the number of cookies completed.

        Args:
            transformed_obs: The processed sensor data.
            action: The agent's action.
            sim_reward: An optional reward from the simulation (not used here).

        Returns:
            reward: The calculated reward value.
        """
        # Initialize observation history if it's the first step.
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            # Append the current observation to the history.
            self.obs_history.append(transformed_obs)

        # Reward is the count of completed cookies.
        reward = float(transformed_obs['completed_cookies'])

        # Track the reward and action history.
        self.reward_history.append(reward)
        self.action_history.append(action)

        # Increment the reward calculation counter.
        self.count += 1

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        """
        Creates an action mask to constrain the agent's choices.
        The mask is derived from the first 25 sensor values in the transformed observation.

        Args:
            transformed_obs: The processed sensor data.
            action: The agent's action (not used here).

        Returns:
            action_mask: A NumPy array indicating valid actions (1 for allowed, 0 for disallowed).
        """
        action_mask = [int(x) for x in list(transformed_obs.values())[:25]]
        return np.array(action_mask)

    async def compute_success_criteria(self, transformed_obs, action):
        """
        Evaluates whether the agent has successfully completed the task.
        Currently, no success criteria are defined.

        Args:
            transformed_obs: The processed sensor data.
            action: The agent's action.

        Returns:
            success: A boolean indicating task success (always False in this implementation).
        """
        return False

    async def compute_termination(self, transformed_obs, action):
        """
        Determines whether to terminate the current training episode.
        Currently, no termination criteria are defined.

        Args:
            transformed_obs: The processed sensor data.
            action: The agent's action.

        Returns:
            terminate: A boolean indicating whether the episode should terminate (always False in this implementation).
        """
        return False