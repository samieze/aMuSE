import argparse
import csv
import math
import sys
from typing import List, Tuple, Dict, Set
import dag
from readinput import OperatorPlacementProblem
from pprint import pformat
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

"""
Notes on Types:
    Event types are strings
    Network Nodes are integers from 0 to N-1
    Queries are DAGs (adjacency lists) whose nodes are event types. Leaf nodes are primitive types.
    Placements are maps from inner query nodes (operators) to network nodes
"""
from readinput import PrimitiveEventType, EventType, OperatorType, Rate, NodeId as NetworkNode
Placement = Dict[OperatorType, NetworkNode]

def find_optimal_placement(problem: OperatorPlacementProblem) -> Tuple[float, Placement]:
    """
    Find optimal cost and optimal placement
    """
    query = problem.inputs
    rates = problem.rates
    sources = problem.sources
    num_nodes = problem.num_nodes() #type:int
    del problem

    ids = list(dag.traverse_all(query))
    primitive_events = [id for id in ids if dag.is_leaf(query, id)]
    operators = [id for id in ids if id not in primitive_events]
    num_ops = len(operators)

    sources_count = {event : len(sources[event]) for event in primitive_events}
    centralization_cost = {e : (sources_count[e] - 1) * rates[e] for e in primitive_events}

    class Candidate:
        def __init__(self,
                     event_types_available: Dict[NetworkNode, Set[EventType]],
                     partial_placement: Placement,
                     uncentralized_primitive_events: Set[PrimitiveEventType],
                     cost: Rate,
                     next_op_index: int):
            self.event_types_available = event_types_available
            self.partial_placement = partial_placement
            self.uncentralized_primitive_events = uncentralized_primitive_events
            self.cost = cost
            self.next_op_index = next_op_index

    def is_done(candidate : Candidate):
        return candidate.next_op_index == num_ops

    def extend(candidate :Candidate, node : NetworkNode) -> Candidate:
        operator = operators[candidate.next_op_index]
        partial_placement = candidate.partial_placement.copy()
        partial_placement[operator] = node
        cost = candidate.cost
        uncentralized_primitive_events = candidate.uncentralized_primitive_events
        event_types_available = candidate.event_types_available

        if operator not in event_types_available[node]:
            event_types_available = event_types_available.copy()
            event_types_available[node] = event_types_available[node] | {operator}
            available_here = event_types_available[node]

            for input in dag.children(query, operator):
                if input not in available_here:
                    available_here.add(input)
                    if dag.is_leaf(query, input): #primitive input
                        uncentralized_primitive_events = uncentralized_primitive_events.difference({input})
                        if node in sources[input]:
                            cost += (sources_count[input] - 1) * rates[input]
                        else:
                            cost += sources_count[input] * rates[input]
                    else: #complex input
                        cost += rates[input]

        return Candidate(event_types_available, partial_placement, uncentralized_primitive_events, cost, candidate.next_op_index+1)

    def h(candidate : Candidate):
        """Lower bound for how much more the cost will increase before the candidate is a solution"""
        return sum((centralization_cost[e] for e in candidate.uncentralized_primitive_events))

    def children(candidate : Candidate):
        for i in range(num_nodes):
            yield extend(candidate,i)

    candidates = [
        Candidate(event_types_available={i : set() for i in range(num_nodes)},
                  partial_placement=dict(),
                  uncentralized_primitive_events={e for e in primitive_events if sources_count[e] > 1},
                  cost=0,
                  next_op_index=0)
    ]#type:List[Candidate]

    best_cost = math.inf
    best_p = None
    while candidates:
        c = candidates.pop()
        if is_done(c) and c.cost < best_cost:
            best_cost = c.cost
            best_p = c.partial_placement
            log.debug(f"New cost: {best_cost}")
            log.debug(f"New placement: {best_p}")
        elif c.cost + h(c) >= best_cost:
            log.debug(f"Rejected candidate of length {c.next_op_index} with cost {c.cost} and minimal final cost {c.cost + h(c)}")
        else:
            candidates.extend(children(c))

    return best_cost, best_p

def main():
    args = parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    elif args.quiet:
        log.setLevel(logging.WARN)

    with open(args.filename, "rb") as f:
        problem = OperatorPlacementProblem.from_pickle_file(f)

    musecosts =  args.filename[9:]

    cost, placement = find_optimal_placement(problem)

    log.info(f"Cost: {cost}")
    log.info(f"Placement: { pformat(placement) }")

    if args.prefix is not None:
        output_file = open(f"{args.prefix}.csv", "a")
    else:
        output_file = sys.stdout

    writer = csv.writer(output_file)
    writer.writerow([musecosts,
                     cost,
                     problem.central_costs,
                     repr(placement)])
    output_file.close()

def parse_args():
    parser = argparse.ArgumentParser(description='Calculate optimal operator placement. Outputs a line of CSV with these fields: [experiment_id : float, optimal_placement_cost : float, central_cost : float, optimal_placement : str]')
    parser.add_argument("filename", help="Pickle file with problem instance")
    parser.add_argument("-q", "--quiet", help="Suppress logging (logging output goes to stderr)", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", help="More logging (logging output goes to stderr) (overrides -q)", action="store_true",
                        default=False)
    parser.add_argument("-o", "--output", dest="prefix", help="If given, write output to a file {prefix}{experiment_id}.csv instead of stdout")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()

