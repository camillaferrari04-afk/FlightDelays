import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._aeroportinodes = []
        self._graph = nx.Graph()
        self._idMap = {}

        self._bestit = []
        self._maxcost = 0

    def getbestit(self, maxtrat, source, target):
        #devo trovare percorso che massimizzi peso archi totale, non visitando più di maxtrat+1 nodi
        #come dico di andare da a1 a a2?
        parziale = [source]
        costoparziale = 0

        #source è il nodo da cui parto a quel giro, target è il nodo finale
        def ricorsione(livmax: int, target, costo):
            if parziale[len(parziale)-1]==target:
                if costo > self._maxcost:
                    self._maxcost=costo
                    self._bestit = copy.deepcopy(parziale)
                return
            if len(parziale)==livmax+1:
                return
            for n in self._graph.neighbors(parziale[-1]):
                if n not in parziale:
                    parziale.append(n)
                    pesoarco = self._graph.get_edge_data(parziale[-2], n)['weight']
                    ricorsione(livmax, target, costo+pesoarco)
                    parziale.pop()
        ricorsione(maxtrat, target, costoparziale)
        return self._bestit, self._maxcost



    def creategraph(self, minimo:int):
        self._graph.clear()
        self.getnodes(minimo)
        self.getedges(minimo)
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getedges(self, minimo:int):
        for e in DAO.getedges(minimo):
            self._graph.add_edge(self._idMap[e["air1"]], self._idMap[e["air2"]], weight=e["weight"])

    def getnodes(self, minimo:int):
        for a in DAO.getairportsmin(minimo):
            self._aeroportinodes.append(a)
            self._idMap[a.ID] = a
        self._graph.add_nodes_from(self._aeroportinodes)

    def getallariports(self) -> list:
        aeroporti = []
        for a in DAO.getAllAirports():
            aeroporti.append(a)
        return aeroporti

    def getconnessi(self, nodo):
        #dizionario {nodo: {weight : pesoarco}}
        dizvicini = self._graph[nodo]
        dizvicini = dict(sorted(dizvicini.items(), key=lambda item: item[1]['weight'], reverse=True))
        return dizvicini