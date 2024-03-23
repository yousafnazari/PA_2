"""@package algo
Insert Documentation here.



"""

class Network:
    """Documentations for this class.
    details.
    """
    def __init__(self):
        self.nodes = {}

    def converge(self):
        #do converge algorithm
        pass

    
class Node:
    def __init__(self):
        self.neighbours = {}
        self.forwarding_table = {}
        self.inbox = {}

    def update_neighbour(self, neighbour_id, cost):
        self.neighbours[neighbour_id] = cost

    def remove_neighbour(self, neighbour_id):
        if neighbour_id in self.neighbours:
            del self.neighbours[neighbour_id]

    def update_forwarding_table(self, destination, next_hop, path_cost):
        self.forwarding_table[destination] = (next_hop, path_cost)

    def dvr_update_neighbours(self,change):
        pass

    def receive_message(self,message,sender):
        self.inbox.update({sender:message})

def apply_topology_to_nodes(data, network):
    network.nodes = {}
    for topology_line in data:
        node_id, neighbour_id, cost = topology_line
        # get existing node or create a new one
        node = network.nodes.get(node_id, Node())
        network.nodes[node_id] = node
        if cost != -999:
            node.update_neighbour(neighbour_id, cost)
        else:
            node.remove_neighbour(neighbour_id)

def generate_forwarding_table(node):
    for destination, (next_hop, path_cost) in node.forwarding_table.items():
        print(f"{destination} {next_hop} {path_cost}")

def send_message(source, destination, path_cost, path, message, outputFile):
    with open(outputFile,'w') as file:
        if path_cost == float('inf'):
            #print(f"from {source} to {destination} cost infinite hops unreachable message {message}")
            file.write(f"from: {source} to: {destination} cost: infinite hops: unreachable message: {message}")
        else:
            hops = ' '.join(map(str, path))
            #print(f"from {source} to {destination} cost {path_cost} hops {hops} message {message}")
            file.write(f"from: {source} to: {destination} cost: {path_cost} hops: {hops} message: {message}")

def read_message(messageFile):
    with open(messageFile,'r') as file:
        for line in file:
            piece = line.split(maxsplit=2)
            from_node_id = str(piece[0])
            to_node_id = str(piece[1])
            message = piece[2].strip()
    return from_node_id, to_node_id, message
    
def get_data(filename):
    
    data = []
    with open(filename,'r') as file:
        for line in file:
            data.append([int(num) for num in line.split()])
        #print(data)
    return data


def distancevector(topology, message, changes, network):
    topology_data = get_data(topology)
    apply_topology_to_nodes(topology_data, network)


    # generate fowarding tables
    for node_id, node in network.nodes.items():
        # distance vector algo here!!!!!!!!!!!!!!!!!
        pass
        generate_forwarding_table(node)

    #just for fun testing
    changes_data = get_data(changes)
    from_id, to_id, msg = read_message(message)
    send_message(from_id,to_id,7,[2, 1],msg,'outputFile.txt')



if __name__ == '__main__':
    network = Network()
    distancevector('topologyFile.txt','messageFile.txt','changesFile.txt',network)