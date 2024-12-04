from typing import Dict, List
from composabl_core import SkillController
from programmed_selector.sensors import sensors

# The Controller class is a custom implementation for managing production scheduling.
# It selects actions based on demand predictions and completed quantities for various products.
class Controller(SkillController):
    def __init__(self, *args, **kwargs):
        """
        Initializes the Controller class with tracking variables.
        Attributes:
            counter: Tracks the number of steps or decisions made by the controller.
        """
        self.counter = 0

    # Computes the action based on demand predictions and completed quantities.
    # Determines which product to prioritize for production.
    async def compute_action(self, transformed_sensors: Dict, action) -> List[float]:
        """
        Args:
            transformed_sensors: Dictionary containing sensor data, including demand predictions
                                 and completed quantities for cakes, cupcakes, and cookies.
            action: The placeholder for the action to be computed.

        Returns:
            action: A list containing the selected action.
                - [2]: Prioritize cakes.
                - [1]: Prioritize cupcakes.
                - [0]: Prioritize cookies.
                - [3]: Default action if all demands are met.
        """
        if transformed_sensors["cake_demand_predict"] < transformed_sensors['completed_cake']:
            action = [2]  # Prioritize cakes if their demand is not yet fulfilled.
        elif transformed_sensors["cupcake_demand_predict"] < transformed_sensors['completed_cupcakes']:
            action = [1]  # Prioritize cupcakes if their demand is not yet fulfilled.
        elif transformed_sensors["cookies_demand_predict"] < transformed_sensors['completed_cookies']:
            action = [0]  # Prioritize cookies if their demand is not yet fulfilled.
        else:
            action = [3]  # Default action when all demands are met.

        return action

    # Defines the success criteria for the controller.
    # This implementation does not define any success criteria and always returns False.
    async def compute_success_criteria(self, transformed_sensors: Dict, action) -> bool:
        """
        Args:
            transformed_sensors: Processed sensor data from the environment.
            action: The current action taken by the agent.

        Returns:
            success: Boolean indicating whether the success criteria have been met.
        """
        return False

    # Determines whether to terminate the current training episode.
    # This implementation does not terminate episodes and always returns False.
    async def compute_termination(self, transformed_sensors: Dict, action) -> bool:
        """
        Args:
            transformed_sensors: Processed sensor data from the environment.
            action: The current action taken by the agent.

        Returns:
            terminate: Boolean indicating whether the episode should terminate.
        """
        return False

    # Processes the observed sensor data if needed.
    # By default, this function returns the data unchanged.
    async def transform_sensors(self, sensors, action) -> str:
        """
        Args:
            sensors: Observations or sensor data from the environment.
            action: The current action being taken by the agent (not used in this method).

        Returns:
            The unmodified sensor data.
        """
        return sensors

    # Modifies actions if needed before applying them in the environment.
    # By default, this function passes actions through unchanged.
    async def transform_action(self, transformed_sensors: Dict, action) -> float:
        """
        Args:
            transformed_sensors: Processed observation data from the environment.
            action: The action to be taken by the agent.

        Returns:
            The unmodified action.
        """
        return action

    # Specifies the sensors that are relevant for this controller.
    # Filters the sensor space to include only the names of defined sensors.
    async def filtered_sensor_space(self) -> List[str]:
        """
        Returns:
            A list of sensor names relevant to this controller.
        """
        return [s.name for s in sensors]