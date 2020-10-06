from typing import List, Dict, Set, Union

Rate = float
NodeId = int
PrimitiveEventType = str
OperatorType = str
EventType = Union[PrimitiveEventType, OperatorType]

class OperatorPlacementProblem:
    def __init__(self,
                 network: Dict[NodeId, List[PrimitiveEventType]],
                 event_rates: Dict[EventType, Rate],
                 operator_inputs: Dict[OperatorType, Set[EventType]],
                 experiment_id: Union[int, str],
                 central_costs: float):
        self.network = network
        self.event_rates = event_rates
        self.operator_inputs = operator_inputs
        self.experiment_id = experiment_id
        self.central_costs = central_costs
