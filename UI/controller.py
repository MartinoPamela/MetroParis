import flet as ft


class Controller:  # attraverso il controller parliamo con l'interfaccia
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._fermataPartenza = None
        self._fermataArrivo = None

    def handlePercorso(self, e):
        # questo è un metodo chiamato da un pulsante, quindi gli viene passato un oggetto di tipo evento
        if self._fermataPartenza is None or self._fermataArrivo is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text(f"Attenzione, selezionare le due fermate."))
            return
        totTime, path = self._model.getBestPath(self._fermataPartenza, self._fermataArrivo)

        if path == []:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text(f"Percorso non trovato."))
            return

        # se arrivo qui significa che il percorso l'ho trovato
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Percorso trovato!"))
        self._view.lst_result.controls.append(ft.Text(f"Il cammino più breve fra "
                                                      f"{self._fermataPartenza} e "
                                                      f"{self._fermataArrivo} impiega "
                                                      f"{totTime} minuti"))

        # poi stampo il percorso
        for p in path:
            self._view.lst_result.controls.append(ft.Text(f"{p}"))

        self._view.update_page()


    def handleCreaGrafo(self, e):
        self._model.buildGraph()  # creo il grafo

        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()

        self._view.lst_result.controls.clear()

        self._view.lst_result.controls.append(ft.Text("Grafo correttamente creato"))  # stampo nel view
        # le informazioni del grafo

        self._view.lst_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi."))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo ha {nEdges} archi."))

        self._view._btnCalcola.disabled = False

        self._view.update_page()

    def handleCreaGrafoPesato(self, e):
        self._model.buildGraphPesato()
        nNodes = self._model.getNumNodes()  # questo posso sempre usarlo perché lavoro sullo stesso grafo
        nEdges = self._model.getNumEdges()

        archiPesoMaggiore = self._model.getArchiPesoMaggiore()

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Grafo pesato correttamente creato. "))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi."))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo ha {nEdges} archi. "))

        # for a in archiPesoMaggiore:
        #    self._view.lst_result.controls.append(ft.Text(a))

        self._view._btnCalcola.disabled = False
        self._view._btnCalcolaPercorso.disabled = False
        self._view.update_page()

    def handleCercaRaggiungibili(self, e):
        # visited = self._model.getBFSNodes(self._fermataPartenza)
        visited = self._model.getDFSNodes(self._fermataPartenza)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Dalla stazione {self._fermataPartenza} posso raggiungere"
                                                      f" {len(visited)} stazioni."))
        for v in visited:
            self._view.lst_result.controls.append(ft.Text(v))
        self._view.update_page()

    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self, e):
        # il dropdown se faccio .value mi restituisce una stringa, non un oggetto, per recuperare l'oggetto devo
        # prenderlo dall'evento, quindi associo alla selezione della voce del dropdown un metodo, questo read
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data

    # c
