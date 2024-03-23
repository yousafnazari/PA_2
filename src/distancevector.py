

class Node:
    def __init__(self):
        self.neighbours = {}
        self.forwarding_table = {}

    def update_neighbour(self, neighbour_id, cost):
        self.neighbours[neighbour_id] = cost

    def remove_neighbour(self, neighbour_id):
        if neighbour_id in self.neighbours:
            del self.neighbours[neighbour_id]

    def update_forwarding_table(self, destination, next_hop, path_cost):
        self.forwarding_table[destination] = (next_hop, path_cost)

    def dvr_update_neighbours(self,change):
        self.sendnameplaceholder = []

def apply_topology_to_nodes(data):
    nodes = {}
    for topology_line in data:
        node_id, neighbour_id, cost = topology_line
        # get existing node or create a new one
        node = nodes.get(node_id, Node())
        nodes[node_id] = node
        if cost != -999:
            node.update_neighbour(neighbour_id, cost)
        else:
            node.remove_neighbour(neighbour_id)
    return nodes

def generate_forwarding_table(node):
    for destination, (next_hop, path_cost) in node.forwarding_table.items():
        print(f"{destination} {next_hop} {path_cost}")

def send_message(source, destination, path_cost, path, message):
    if path_cost == float('inf'):
        print(f"from {source} to {destination} cost infinite hops unreachable message {message}")
    else:
        hops = ' '.joing(map(str, path))
        print(f"from {source} to {destination} cost {path_cost} hops {hops} message {message}")

def distancevector(topology, message, changes):
    topology_data = get_data(topology)
    nodes = apply_topology_to_nodes(topology_data)

    # generate fowarding tables
    for node_id, node in nodes.items():
        # distance vector algo here!!!!!!!!!!!!!!!!!
        pass
        generate_forwarding_table(node)

    # read messages to send
    #message_data = get_data(message)
    changes_data = get_data(changes)





def get_data(filename):
    nodes = {}
    data = []
    with open(filename,'r') as file:
        for line in file:
            data.append([int(num) for num in line.split()])
        print(data)
    return data



if __name__ == '__main__':
    distancevector('topologyFile.txt','messageFile.txt','changesFile.txt')