

class Node:
    def __init__(self):
        self.neighbours = []

    def dvr_update_neighbours(self,change):
        self.sendnameplaceholder = []

def apply_topology_to_nodes(data):
    nodes = {}
    for node_id, neighbor_ids in enumerate(data):
        node = Node()
        nodes[node_id] = node
        for neighbor_id, cost in enumerate(neighbor_ids):
            if cost != 0:
                node.neighbours.append((neighbor_id, cost))
    return nodes

def distancevector(topology, message, changes):
    topology_data = get_data(topology)
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