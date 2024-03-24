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
        updated = True 

        while updated:
            updated = False

            for node_id, node in self.nodes.items():
                #do for each neighbour of node
                for neighbour_id, cost in node.neighbours.items():
                    neighbour = self.nodes[neighbour_id]
                    #add route for each of neighbours' neighbours
                    for destination, (next_hop, path_cost) in neighbour.forwarding_table.items():
                        #check for lower cost path
                        if destination not in node.forwarding_table or cost + path_cost < node.forwarding_table[destination][1]:
                            node.update_forwarding_table(destination,neighbour_id,cost+path_cost)
                            updated = True
    
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
            node_next.remove_neighbour(node_id)

def generate_forwarding_table(node,file):
    
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
            from_node_id = int(piece[0])
            to_node_id = int(piece[1])
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

def output_data(file, messages, network):
    
            # generate fowarding tables
        for node_id, node in sorted(network.nodes.items()):
            file.write(f"node {node_id} forwarding table\n")
            generate_forwarding_table(node,file)
        for from_id, to_id, message in messages:
            #find message distance
            node = network.nodes.get(from_id,Node())
            next_hop, path_to_destination = node.forwarding_table[to_id]
            #get hops
            hops = []
            hops.append(from_id)
            '''
            traversed = True
            while traversed:
                node = network.nodes.get(next_hop,Node())
                hops.append(next_hop)
                next_hop, path_cost = node.forwarding_table[to_id]
                if path_cost == 0:
                    traversed = False
             '''       
            send_message(from_id,to_id,path_to_destination,hops,message,file)
        
def apply_change(network,change):

        node1_id = change[0]
        node2_id = change[1]
        node1 = network.nodes.get(node1_id, Node())
        node2 = network.nodes.get(node2_id, Node())
        new_cost = change[2]
        if new_cost != -999:
            node1.update_forwarding_table(node2_id,node2_id,new_cost)
            node2.update_forwarding_table(node1_id,node1_id,new_cost)
        else:
            node1.remove_neighbour(node2_id)
            node2.remove_neighbour(node1_id)

def distancevector(topology, message, changes, network, output='outputFile.txt'):

    #read topology and apply it to the network
    topology_data = get_data(topology)
    apply_topology_to_nodes(topology_data, network)
    #read messages to send
    messages = read_message(message)
    changes_data = get_data(changes)
    with open(output,'w') as file:
        #output_data(file,messages,network)
        for change in changes_data:
            apply_change(network,change)
            network.converge()
            output_data(file, messages, network)


    ###########
    # ADD change file implementation, reconverge, reoutput
    ###########
    #output forwarding tables and sent messages
    





import sys
if __name__ == '__main__':
    network = Network()
    top = sys.argv[1]
    msg = sys.argv[2]
    chg = sys.argv[3]
    if len(sys.argv) > 4:
        out = sys.argv[4]
        distancevector(top,msg,chg,network,out)
    else: 
        distancevector(top,msg,chg,network)
    #print(f"{top},{msg},{chg},{out}")
    
    #distancevector('topologyFile.txt','messageFile.txt','changesFile.txt',network)