

class Node:
    def __init__(self):
        self.neighbours = []

    def dvr_update_neighbours(self,change):
        self.sendnameplaceholder = []


def distancevector(topology, message, changes):
    #function definition
    print(f"Hello {topology}, {message}, {changes}")







def get_topology(filename):
    nodes = {}
    with open(filename,'r') as file:
        topologydata = file.read()
        print(topologydata)




if __name__ == '__main__':
    distancevector('topologyFile.txt','messageFile','changesFile')