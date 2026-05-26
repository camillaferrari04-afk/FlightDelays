import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_compagnie = None
        self.btn_analizza = None
        self.dpd_partenza = None
        self.dpd_destinazione = None
        self.btn_connessi = None
        self.txt_tratte = None
        self.btn_itinerario = None
        self.txtOut = None

    def load_interface(self):
        # title
        self._title = ft.Text("Extflightdelays", color="blue", size=24)
        self._page.controls.append(self._title)

        self.txt_compagnie = ft.TextField(label="Compagnie minime", hint_text="Inserisci un numero")
        self.btn_analizza = ft.ElevatedButton(text="Analizza aeroporti", on_click=self._controller.handle_analizza)

        self.dpd_partenza = ft.Dropdown(label="Aeroporto di partenza", disabled=True)
        self.dpd_destinazione = ft.Dropdown(label="Aeroporto di destinazione",  disabled=True)
        self.btn_connessi = ft.ElevatedButton(text="Aeroporti connessi", on_click=self._controller.handle_connessi,  disabled=True)

        self.txt_tratte = ft.TextField(label="Numero tratte massimo", hint_text="Inserisci un numero", disabled=True)
        self.btn_itinerario = ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handle_itinerario, disabled=True)

        self.txtOut = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        row1 = ft.Row([
            ft.Container(ft.Text("Compagnie minime"), width=250),
            ft.Container(self.txt_compagnie , width=250),
            ft.Container(self.btn_analizza, width=250)],alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        row2 = ft.Row([
            ft.Container(ft.Text("Aeroporto di partenza"), width=250),
            ft.Container(self.dpd_partenza , width=250),
            ft.Container(self.btn_connessi, width=250)],alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        row3 = ft.Row([
            ft.Container(ft.Text("Aeroporto di destinazione"), width=250),
            ft.Container(self.dpd_destinazione , width=250),
            ft.Container(width=250)],alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        row4 = ft.Row([
            ft.Container(ft.Text("Numero tratte massimo"), width=250),
            ft.Container(self.txt_tratte, width=250),
            ft.Container(self.btn_itinerario, width=250)], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        self._page.add(row1, row2, row3, row4, self.txtOut)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
