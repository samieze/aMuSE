import pickle
from typing import List, Set, Dict, Union

import dag
from dag import normalize_adjacency_list
from ooclass import OperatorPlacementProblem as PickledOperatorPlacementProblem
from ooclass import PrimitiveEventType, EventType, Rate, OperatorType, NodeId

class OperatorPlacementProblem:
    def __init__(self, raw_opp : PickledOperatorPlacementProblem):
        #convert from {0: ["A", "B", ...], 1: ["B"], ...} to {"B" : {0, 1, ...}, "A": {0, ...}, ...}
        sources = dict()
        for (node_id, generated_events) in raw_opp.network.items():
            for eventtype in generated_events:
                try:
                    sources[eventtype].add(node_id)
                except KeyError:
                    sources[eventtype] = {node_id}

        #convert lists in raw_opp to sets
        sources = {key: list_to_set(value) for (key, value) in sources.items()}
        rates = {key: value for (key, value) in raw_opp.event_rates.items()}
        inputs = {key: list_to_set(value) for (key, value) in raw_opp.operator_inputs.items()}

        #Normalize adjacency list
        inputs = normalize_adjacency_list(inputs)

        self.sources = sources             #type:Dict[PrimitiveEventType, Set[NodeId]]
        self.rates = rates                 #type:Dict[EventType, Rate]
        self.inputs = inputs               #type:Dict[OperatorType, Set[EventType]]
        self.experiment_id = raw_opp.experiment_id if hasattr(raw_opp, "experiment_id") else None #type:Union[str, int]
        self.central_costs = raw_opp.central_costs if hasattr(raw_opp, "central_costs") else None #type:float

        self._validate()

    @classmethod
    def from_pickle_file(cls, file):
        return cls(pickle.load(file))

    def get_local_rate(self, primitive_event_type, node_id) -> Rate:
        if node_id not in self.sources[primitive_event_type]:
            return 0
        else:
            return self.rates[primitive_event_type]

    def get_global_rate(self, primitive_event_type) -> Rate:
        num_sources = len(self.sources[primitive_event_type])
        return num_sources * self.rates[primitive_event_type]

    def _validate(self):
        #Every primitive event type in the query occurs in the network
        primitive_events_in_query_with_no_source = self._primitive_event_types_in_query() - self._primitive_event_types_with_source()
        if len(primitive_events_in_query_with_no_source) > 0:
            raise ValueError(f"No source in network for the following primitive event types from the query: {primitive_events_in_query_with_no_source}" )

        #Every primitive event in the query has a rate
        idsWithoutRate = self._primitive_event_types_in_query() - self.rates.keys()
        if len(idsWithoutRate) > 0:
            raise ValueError(f"No rate for these consumed primitive event types: {idsWithoutRate}")

        #Every non-root operator has a rate
        idsWithoutRate = (self._operator_ids() - self._root_operator_ids()) - self.rates.keys()
        if len(idsWithoutRate) > 0:
            raise ValueError(f"No rate for these operators: {idsWithoutRate}")

        #node_ids = {0, ..., numNodes-1}
        num_nodes= len(self._node_ids())
        if not self._node_ids() == set(range(num_nodes)):
            raise ValueError(f"node ids: {self._node_ids()} is not 0 ... {num_nodes-1}")

    def _primitive_event_types_with_source(self):
        return self.sources.keys()

    def num_nodes(self) -> int:
        return len(self._node_ids())

    def _query_node_ids(self):
        return self.inputs.keys()

    def _primitive_event_types_in_query(self):
        return {id for id in self._query_node_ids() if len(self.inputs[id]) == 0}

    def _operator_ids(self):
        return {id for id in self._query_node_ids() if len(self.inputs[id]) > 0}

    def _root_operator_ids(self):
        return set(dag.roots(self.inputs))

    def _node_ids(self):
        return {nodeId for nodeList in self.sources.values() for nodeId in nodeList}

def list_to_set(list: List):
    """
    Convert list to set, throw error on duplicates
    """
    result = set(list)
    if len(result) == len(list):
        return result
    else:
        raise ValueError(f"Duplicate in list {list}")