from typing import TypeVar, Iterable, Set, Dict, List

IDType = TypeVar("IDType")
AdjacencyList = Dict[IDType, Set[IDType]]

def normalize_adjacency_list(adjacency_list: Dict[IDType, Set[IDType]]) -> Dict[IDType, Set[IDType]]:
    '''
    Return a copy of an adjacency list wherein every id occurs as a key.
    '''
    ids = set(adjacency_list.keys()).union(*adjacency_list.values())

    normalized = dict()
    for id in ids:
        try:
            normalized[id] = adjacency_list[id]
        except KeyError:
            normalized[id] = set()  # empty set of successors for leaves

    assert set(normalized.keys()) == ids
    return normalized

def invert_adjacency_list(adjacency_list: Dict[IDType, Set[IDType]]):
    """
    Invert all edges in the graph
    """
    adjacency_list=normalize_adjacency_list(adjacency_list)
    ids = adjacency_list.keys()

    inverted = {id: set() for id in ids}
    for id in ids:
        for child_id in adjacency_list[id]:
            inverted[child_id].add(id)
    return inverted

def is_leaf(adjacency_list : Dict[IDType, Set[IDType]], id : IDType):
    return adjacency_list[id] == set()

def is_not_leaf(adjacency_list : Dict[IDType, Set[IDType]], id : IDType):
    return not is_leaf(adjacency_list, id)

def children(adjacency_list : Dict[IDType, Set[IDType]], id : IDType):
    return adjacency_list[id]

def inners(adjacency_list : Dict[IDType, Set[IDType]]) -> List[IDType]:
    return [id for id in adjacency_list.keys() if is_not_leaf(adjacency_list, id)]

def leaves(normalized_adjacency_list : Dict[IDType, Set[IDType]]) -> List[IDType]:
    return [id for id in normalized_adjacency_list.keys() if is_leaf(normalized_adjacency_list, id)]

def roots(adjacency_list: Dict[IDType, Set[IDType]]) -> List[IDType]:
    inverted = invert_adjacency_list(adjacency_list)
    return [id for id in inverted.keys() if len(inverted[id]) == 0]

def traverse_all(adjacency_list : Dict[IDType, Set[IDType]]) -> Iterable[IDType]:
    """
    Traverse graph in reverse topological order (children before parents)
    :param adjacency_list:
    :return:
    """
    visited = set()
    for id in roots(adjacency_list):
        yield from traverse(adjacency_list, id, visited)

def traverse(adj_list : Dict[IDType, Set[IDType]],
             root : IDType,
             visited : Set[IDType] = None) -> Iterable[IDType]:
    if visited is None:
        visited = set()
    if root in visited:
        return
    for child in children(adj_list, root):
        yield from traverse(adj_list, child, visited)
    visited.add(root)
    yield root