import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._Partenza = None
        self._Arrivo = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_analizza(self, e):
        minimo = self._view.txt_compagnie.value
        if minimo=='' or minimo is None or not minimo.isdigit():
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Devi inserire un numero valido", color="red", size=18))
            self._view.update_page()
            return
        self.caricamento()
        numnodi, numarchi = self._model.creategraph(int(minimo))
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text("Grafo correttamente creato", color="green", size=18))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo contiene {numnodi} nodi e {numarchi} archi"))
        self.fillDDAeroporti()
        self._view.dpd_partenza.disabled=False
        self._view.dpd_destinazione.disabled=False
        self._view.btn_connessi.disabled=False
        self._view.txt_tratte.disabled=False
        self._view.btn_itinerario.disabled=False
        self._view.update_page()

    def handle_connessi(self, e):
        selezionato = self._Partenza
        if selezionato == '' or selezionato is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Devi selezionare un aeroporto", color="red", size=18))
            self._view.update_page()
            return
        self.caricamento()
        vicini = self._model.getconnessi(selezionato)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text("Aeroporti connessi: ", color="blue", size=18))
        for a in vicini.keys():
            self._view.txtOut.controls.append(ft.Text(f"{a} - numero voli {vicini[a]["weight"]}"))
        self._view.update_page()

    def handle_itinerario(self, e):
        maxtrat=self._view.txt_tratte.value
        if (maxtrat == '' or maxtrat is None or not maxtrat.isdigit() or self._Arrivo is None or self._Arrivo=="" or
            self._Partenza is None or self._Partenza==""):
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Devi selezionare due aeroporti e una tratta massima", color="red", size=18))
            self._view.update_page()
            return
        self.caricamento()
        itinerario, numvoli = self._model.getbestit(int(maxtrat),self._Partenza, self._Arrivo)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Itinerario migliore ({numvoli} voli disponibili): ", color="blue", size=18))
        for a in itinerario:
            self._view.txtOut.controls.append(ft.Text(a))
        self._view.update_page()
        pass

    def caricamento(self):
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text("Caricamento..."))
        self._view.update_page()

    def fillDDAeroporti(self):
        for aeroporto in self._model._aeroportinodes:
            self._view.dpd_partenza.options.append(ft.dropdown.Option(text=aeroporto.AIRPORT,
                                                         data=aeroporto,
                                                         on_click=self.read_DD_Partenza))
            self._view.dpd_destinazione.options.append(ft.dropdown.Option(text=aeroporto.AIRPORT,
                                                                    data=aeroporto,
                                                                    on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        self._Partenza = e.control.data

    def read_DD_Arrivo(self,e):
        self._Arrivo = e.control.data

