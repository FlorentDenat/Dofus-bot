from collections import deque

# https://www.pythonpool.com/a-star-algorithm-python/
class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis
 
    def get_neighbors(self, v):
        return self.adjac_lis[v]
 
    # This is heuristic function which is having equal values for all nodes
    # We use Manhattan distance between test point and stop point. 
    # VERIFIER L'HEURISTIQUE EN PRINTANT QUAND J'AURAIS DES DATAAAAAAAAAS
    def h(self,n,stop):
        return (abs(stop[0]-n[0]) + abs(stop[1]-n[1]))
 
    def a_star_algorithm(self, start, stop):
        # In this open_lst is a list of nodes which have been visited, but who's 
        # neighbours haven't all been always inspected, it starts off with the start node
        # Closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = set([start])
        closed_lst = set([])
 
        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0
 
        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start
 
        while len(open_lst) > 0:
            n = None
 
            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + self.h(v,stop) < poo[n] + self.h(n,stop):
                    n = v;
 
            if n == None:
                print('Path does not exist!')
                return None
 
            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []
 
                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]
 
                reconst_path.append(start)
 
                reconst_path.reverse()
 
                print('Path found: {}'.format(reconst_path))
                return reconst_path
 
            # for all the neighbors of the current node do
            # Here the weight is set at 1 between all points.
            for m in self.get_neighbors(n):
                # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + 1
 
                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + 1:
                        poo[m] = poo[n] + 1
                        par[m] = n
 
                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)
 
            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)
 
        print('Path does not exist!')
        return None

    #Creer le graph auto : Sur une map, check les accessibles autour et où cliquer.
    # Noter dans le graph, et mettre les maps notées dans les maps a voir. (save dans un fichier pour recommencer)
    # Aller dans la map connu la plus proche et recommencer.

    # Pour faire ça commencer par tester sur un petit echantillon créé a la main. 
    # Quand les fonctions de déplacement fonctionnent, on rempli.

    # def check_adj_map(direction)
    # def find_adj_maps():
    # def write_adj_maps():


# adjac_lis_dof = {
#     (0,0): {(0,1) : (1000,500), (1,0) :(500,0), (-1,0) : (500,1000)},
#     (0,1): {(1,1) : (500,0)},
#     (1,0): {(1,1) : (1000,500)},
#     (-1,0): {}
# }

# graph1 = Graph(adjac_lis_dof)
# graph1.a_star_algorithm((0,0), (1,1))