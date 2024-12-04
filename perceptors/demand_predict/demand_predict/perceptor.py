import time
from composabl_core import PerceptorImpl
from demand_predict.sensors import sensors

# The DemoPerceptor class processes sensor data to predict demand for various products.
# It uses a heuristic-based approach to estimate future demand for cookies, cupcakes, and cakes.
class DemoPerceptor(PerceptorImpl):
    def __init__(self, *args, **kwargs):
        """
        Initializes the DemoPerceptor with tracking variables.
        Attributes:
            previous_value: Placeholder for storing previous observations (not currently used).
            previous_time: Placeholder for tracking the timestamp of previous computations (not currently used).
        """
        self.previous_value = None
        self.previous_time = None

    async def compute(self, obs_spec, obs):
        """
        Processes sensor data and computes predictions for product demand using heuristics.

        Args:
            obs_spec: Specification of the observation space (not used in this implementation).
            obs: Sensor data provided as either a list or dictionary.

        Returns:
            dict: Predicted demand values for cookies, cupcakes, and cakes.
        """
        # Extract sensor names from the sensor definitions.
        sensor_names = [s.name for s in sensors]

        # Convert observations to a dictionary if they are not already in that format.
        obs_dict = dict(map(lambda i, j: (i, j), sensor_names, obs))  # Maps sensor names to their respective values.
        if type(obs) != dict:
            obs = dict(zip(sensor_names, obs))  # Converts a list of observations into a dictionary.

        # Apply heuristic-based calculations to predict demand.
        # The heuristic scales current demand values to estimate future demand.
        co = int(1.3 * float(obs["cookies_demand"]))  # Predict cookies demand.
        cp = int(1.1 * float(obs["cupcake_demand"]))  # Predict cupcake demand.
        ck = int(1.05 * float(obs["cake_demand"]))    # Predict cake demand.

        # Return the predictions as new sensor variables.
        return {
            "cookies_demand_predict": co,
            "cupcake_demand_predict": cp,
            "cake_demand_predict": ck
        }

    def filtered_sensor_space(self, obs):
        """
        Specifies the sensors that are relevant for the perceptor's computations.

        Args:
            obs: Sensor data provided by the environment (not used in this implementation).

        Returns:
            list: Names of all sensors relevant to this perceptor.
        """
        return [s.name for s in sensors]