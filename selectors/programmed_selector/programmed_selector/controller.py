# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Dict, List

from composabl_core import SkillController

from programmed_selector.sensors import sensors


class Controller(SkillController):
    def __init__(self, *args, **kwargs):
        self.counter = 0

    async def compute_action(self, transformed_sensors: Dict, action) -> List[float]:
        if transformed_sensors["cake_demand_predict"] < transformed_sensors['completed_cake']:
            action = [2]
        elif transformed_sensors["cupcake_demand_predict"] < transformed_sensors['completed_cupcakes']:
            action = [1]
        elif transformed_sensors["cookies_demand_predict"] < transformed_sensors['completed_cookies']:
            action = [0]
        else:
            action = [3]

        return action

    async def compute_success_criteria(self, transformed_sensors: Dict, action) -> bool:
        return False

    async def compute_termination(self, transformed_sensors: Dict, action) -> bool:
        return False

    async def transform_sensors(self, sensors, action) -> str:
        return sensors

    async def transform_action(self, transformed_sensors: Dict, action) -> float:
        return action

    async def filtered_sensor_space(self) -> List[str]:
        return [s.name for s in sensors]
