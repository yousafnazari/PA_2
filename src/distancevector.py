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
        #create the same for neighbouring nodes
        node_next = network.nodes.get(neighbour_id, Node())
        network.nodes[neighbour_id] = node_next
        if cost != -999:
            node.update_neighbour(neighbour_id, cost) #apply node -> neighbour
            node.update_forwarding_table(neighbour_id,neighbour_id,cost) #dst, next hop, cost
            node.update_forwarding_table(node_id,node_id,0) # add node to itself
            # second column of nodes need to be added with the same path costs
            node_next.update_neighbour(node_id, cost)
            node_next.update_forwarding_table(node_id,node_id,cost)
            node_next.update_forwarding_table(neighbour_id,neighbour_id,0)
        else:
            node.remove_neighbour(neighbour_id)
            neighbour_id.remove_neighbour(node_id)

def generate_forwarding_table(node,outputFile,file):
    
    #with open(outputFile,'a') as file:
        for destination, (next_hop, path_cost) in sorted(node.forwarding_table.items()):
            file.write(f"{destination} {next_hop} {path_cost}\n")
    

def send_message(source, destination, path_cost, path, message, file):
    
        if path_cost == float('inf'):
            #print(f"from {source} to {destination} cost infinite hops unreachable message {message}")
            file.write(f"from: {source} to: {destination} cost: infinite hops: unreachable message: {message}\n")
        else:
            hops = ' '.join(map(str, path))
            #print(f"from {source} to {destination} cost {path_cost} hops {hops} message {message}")
            file.write(f"from: {source} to: {destination} cost: {path_cost} hops: {hops} message: {message}\n")

def read_message(messageFile):
    messages = []
    with open(messageFile,'r') as file:
        for line in file:
            piece = line.split(maxsplit=2)
            from_node_id = str(piece[0])
            to_node_id = str(piece[1])
            message = piece[2].strip()
            messages.append((from_node_id,to_node_id,message))
    return messages
    
def get_data(filename):
    
    data = []
    with open(filename,'r') as file:
        for line in file:
            data.append([int(num) for num in line.split()])
        #print(data)
    return data

def output_data(output, messages, network):
    with open(output,'w') as file:
            # generate fowarding tables
        for node_id, node in sorted(network.nodes.items()):
            file.write(f"node {node_id} forwarding table\n")
            generate_forwarding_table(node,output,file)
        for from_id, to_id, message in messages:
            send_message(from_id,to_id,7,[2, 1],message,file)
        


def distancevector(topology, message, changes, network, output='outputFile.txt'):

    #read topology and apply it to the network
    topology_data = get_data(topology)
    apply_topology_to_nodes(topology_data, network)
    #read messages to send
    messages = read_message(message)
    '''
    ADD FORWARDING TABLE CONGERENCE ALGO HERE
    '''
    #output forwarding tables and sent messages
    output_data(output, messages, network)


    changes_data = get_data(changes)




if __name__ == '__main__':
    network = Network()
    distancevector('topologyFile.txt','messageFile.txt','changesFile.txt',network)