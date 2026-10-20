import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _errore(self, msg):
        self._view._txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDAnni(self):
        for a in self._model.getAnni():
            self._view._ddAnno1.options.append(ft.dropdown.Option(str(a)))
            self._view._ddAnno2.options.append(ft.dropdown.Option(str(a)))

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        # 1. leggo i due anni (il dropdown restituisce una stringa, oppure None)
        if self._view._ddAnno1.value is None or self._view._ddAnno2.value is None:
            self._errore("Selezionare entrambi gli anni!")
            return
        anno1 = int(self._view._ddAnno1.value)
        anno2 = int(self._view._ddAnno2.value)

        # 2. controllo l'ordine
        if anno1 > anno2:
            self._errore("L'anno di inizio non può essere successivo all'anno di fine!")
            return

        # 3. creo il grafo
        self._model.buildGraph(anno1, anno2)
        if self._model.getNumNodi() == 0:
            self._errore("Nessun pilota ha vinto una gara nel periodo selezionato!")
            return

        # 4. stampo nodi e archi
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # 5. riempio il dropdown dei piloti (per il punto 2)
        self._view._ddPilota.options.clear()
        self._view._ddPilota.value = None
        for d in self._model.getNodiOrdinati():
            self._view._ddPilota.options.append(
                ft.dropdown.Option(key=str(d.driverId), text=str(d)))

        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()

        # il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # a. pilota con più vittorie
        pilota, vittorie = self._model.getPiuVittorie()
        self._view._txt_result.controls.append(
            ft.Text(f"Pilota con più vittorie: {pilota} ({vittorie} vittorie)"))

        # b. i 3 archi di peso maggiore
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(ft.Text("Top 3 archi di peso maggiore:"))
        for i, (n1, n2, peso) in enumerate(self._model.getTop3(), start=1):
            self._view._txt_result.controls.append(
                ft.Text(f"{i}. {n1} -- {n2} (circuiti in comune: {peso})"))

        # c. numero di componenti connesse
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di componenti connesse: {self._model.getNumComponenti()}"))

        self._view.update_page()

    def handleSquadra(self, e):
        self._view._txt_result.controls.clear()

        # 1. il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # 2. pilota di partenza
        if self._view._ddPilota.value is None:
            self._errore("Selezionare un pilota di partenza!")
            return
        partenza = self._model.getPilota(int(self._view._ddPilota.value))
        if partenza is None:
            self._errore("Pilota non presente nel grafo, ricreare il grafo!")
            return

        # 3. N
        try:
            n = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._errore("N deve essere un numero intero!")
            return
        if n < 2 or n > 6:
            self._errore("N deve essere compreso tra 2 e 6!")
            return

        # 4. ricorsione
        squadra, totale = self._model.getSquadra(partenza, n)

        # 5. stampa
        if len(squadra) == 0:
            self._errore(f"Nessun gruppo di {n} piloti connesso e con nazionalità diverse "
                         f"partendo da {partenza}")
            return

        self._view._txt_result.controls.append(
            ft.Text(f"Squadra dei campioni di {n} piloti (partenza: {partenza}):"))
        for p in sorted(squadra, key=lambda x: str(x)):
            self._view._txt_result.controls.append(
                ft.Text(f"- {p} ({p.nationality}) - vittorie: {p.vittorie}"))
        self._view._txt_result.controls.append(ft.Text(f"Somma totale delle vittorie: {totale}"))

        self._view.update_page()

