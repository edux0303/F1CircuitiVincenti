import networkx as nx
from itertools import combinations
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        # punto 2
        self._solBest = []
        self._pesoBest = -1
        self._visti = set()
        self._N = 0

    # ==================== PUNTO 1 ====================

    def getAnni(self):
        return DAO.getAllYears()

    def buildGraph(self, anno1, anno2):
        self._grafo.clear()
        self._idMap = {}

        # nodi: piloti che hanno vinto almeno una gara nel periodo
        nodi = DAO.getNodi(anno1, anno2)
        self._idMap = {d.driverId: d for d in nodi}
        self._grafo.add_nodes_from(nodi)

        # riempio il set dei circuiti su cui ha vinto ogni pilota
        for idP, idC in DAO.getVittorieCircuiti(anno1, anno2):
            if idP in self._idMap:
                self._idMap[idP].circuiti.add(idC)

        # archi: due piloti che hanno vinto su almeno uno stesso circuito
        for d1, d2 in combinations(nodi, 2):
            comuni = d1.circuiti & d2.circuiti
            if len(comuni) > 0:
                self._grafo.add_edge(d1, d2, weight=len(comuni))

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda d: str(d))

    def getPilota(self, idP):
        return self._idMap.get(idP)

    def getPiuVittorie(self):
        best = max(self._grafo.nodes, key=lambda d: d.vittorie)
        return best, best.vittorie

    def getTop3(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:3]

    def getNumComponenti(self):
        return nx.number_connected_components(self._grafo)

    # ==================== PUNTO 2 ====================

    def getSquadra(self, partenza, N):
        self._solBest = []
        self._pesoBest = -1
        self._visti = set()
        self._N = N
        self._ricorsione([partenza], partenza.vittorie)
        return self._solBest, self._pesoBest

    def _ricorsione(self, parziale, pesoParziale):
        # 0. gruppo già visto in un altro ordine -> mi fermo
        chiave = frozenset(parziale)
        if chiave in self._visti:
            return
        self._visti.add(chiave)

        # 1. caso terminale: il gruppo ha N piloti
        if len(parziale) == self._N:
            if pesoParziale > self._pesoBest:
                self._pesoBest = pesoParziale
                self._solBest = list(parziale)
            return

        # 2. candidati: vicini dei piloti già nel gruppo
        candidati = set()
        for p in parziale:
            for v in self._grafo.neighbors(p):
                if self._ammissibile(v, parziale):
                    candidati.add(v)

        # 3. provo ad aggiungere ogni candidato (prima i più vincenti)
        for c in sorted(candidati, key=lambda x: -x.vittorie):
            parziale.append(c)
            self._ricorsione(parziale, pesoParziale + c.vittorie)
            parziale.pop()

    def _ammissibile(self, c, parziale):
        # non deve essere già nel gruppo
        if c in parziale:
            return False
        # nazionalità diversa da tutti quelli del gruppo
        for p in parziale:
            if p.nationality == c.nationality:
                return False
        return True