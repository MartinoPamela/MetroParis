from database.DAO import DAO
import networkx as nx
import geopy.distance


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMap = {}  # creo un dizionario che ha come chiavi gli id e come valori gli oggetti
        # lo faccio nell'init perché tanto lo faccio solo una volta
        for f in self._fermate:
            self._idMap[f.id_fermata] = f
        self._linee = DAO.getAllLinee()  # posso caricarle all'inizio perché non dipendono dall'utente
        self._lineaMap = {}
        for l in self._linee:
            self._lineaMap[l.id_linea] = l

    def getBestPath(self, v0, v1):
        costoTot, path = nx.single_source_dijkstra(self._grafo, v0, v1)
        return costoTot, path  # costoTot è il traversal time totale per fare il percorso


    def getBFSNodes(self, source):
        # source lo devo prendere come argomento della funzione, quindi questo metodo avrà bisogno di un ingresso
        edges = nx.bfs_edges(self._grafo, source)
        visited = []
        for u,v in edges:
            visited.append(v)
        return visited

    def getDFSNodes(self, source):
        edges = nx.dfs_edges(self._grafo, source)
        visited = []
        for u,v in edges:
            visited.append(v)
        return visited

    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)

        # Mode 1: doppio loop su nodi e query per ogni arco.
        """
        for u in self._fermate:
            for v in self._fermate:
                res = DAO.getEdge(u, v)
                # res mi aspetto che sia o vuoto e quindi non devo mettere l'arco,
                # oppure non vuoto e quindi devo mettere l'arco
                if len(res) > 0:  # vuol dire che c'è un arco
                    self._grafo.add_edge(u, v)
                    print(f"Added edge between {u} and {v}")
        """

        # Mode 2: loop singolo sui nodi e query per identificare i vicini
        """
        for u in self._fermate:
            vicini = DAO.getEdgesVicini(u)  # vicini sarà una lista che in generale avrà più di un elemento
            for v in vicini:
                v_nodo = self._idMap[v.id_stazA]
                self._grafo.add_edge(u, v_nodo)
                print(f"Added edge between {u} and {v_nodo}")
        """

        # Mode 3: unica query che legge tutte le connessioni
        allConnessioni = DAO.getAllConnessioni()
        print(len(allConnessioni))
        for c in allConnessioni:
            u_nodo = self._idMap[c.id_stazP]
            v_nodo = self._idMap[c.id_stazA]
            self._grafo.add_edge(u_nodo, v_nodo)  # aggiungo l'arco
            # print(f"Added edge between {u_nodo} and {v_nodo}")

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgePesati()

    def addEdgePesati(self):
        self._grafo.clear_edges()
        allConnessioni = DAO.getAllConnessioni()
        for c in allConnessioni:
            v0 = self._idMap[c.id_stazP]
            v1 = self._idMap[c.id_stazA]
            linea = self._lineaMap[c.id_linea]
            peso = self.getTraversalTime(v0, v1, linea)  # questo peso lo metto nel grafo solo se è il più piccolo
            # possibile fra questa coppia di stazioni

            if self._grafo.has_edge(v0, v1):  # vuol dire che ho già aggiunto un peso
                if self._grafo[v0][v1]["weight"] > peso:  # se il peso che ho già aggiunto, che è un tempo di
                    self._grafo[v0][v1]["weight"] = peso  # percorrenza, è > peso allora sostituisco questo peso
            else:
                self._grafo.add_edge(v0, v1, weight=peso)

        # for c in allConnessioni:
        #    if self._grafo.has_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA]):
                # se l'arco c'è incremento il peso di 1
        #        self._grafo[self._idMap[c.id_stazP]][self._idMap[c.id_stazA]]["weight"] += 1
                # quest'istruzione accede al weight, agli attributi di quell'arco lì
        #    else:  # vuol dire che non l'ho ancora aggiunto
        #        self._grafo.add_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA], weight=1)

    def getArchiPesoMaggiore(self):
        # questo metodo cicla su tuti gli archi e mi restituisce una lista degli archi che hanno un peso maggiore di 1
        if len(self._grafo.edges) == 0:
            print("Il grafo è vuoto")
            return

        edges = self._grafo.edges  # prendo tutti gli archi del mio grafo
        result = []  # metto il risultato in una lista
        for u,v in edges:
            # print(self._grafo[u][v]["weight"])   così stampo i pesi
            peso = self._grafo[u][v]["weight"]  # [u][v] è un accesso al dizionario
            if peso > 1:  # in questo caso salvo l'arco
                result.append((u,v,peso))  # in questo result metto delle tuple che hanno nodo source,nodo target e peso

        return result

    def getEdgeWeight(self, v1, v2):  # metodo per leggere i pesi
        return self._grafo[v1][v2]["weight"]  # questo metodo mi dice il peso dell'arco dati due nodi



    @property
    def fermate(self):
        return self._fermate

    def getNumNodes(self):
        return len(self._grafo.nodes)  # mi restituisce la dimensionalità dei nodi

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getTraversalTime(self, v0, v1, linea):
        p0 = (v0.coordX, v0.coordY)
        p1 = (v1.coordX, v1.coordY)
        distanza = geopy.distance.distance(p0, p1).km
        velocita = linea.velocita
        tempo = distanza/velocita * 60  # converto in minuti dato che ce l'ho in ore
        return tempo
