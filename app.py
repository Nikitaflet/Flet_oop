import flet as ft
from flet import *

from database import get_db_path, ensure_db_exists, connect_db
from main_page import show_main as _show_main
from create_page import show_create as _show_create
from edit_page import show_edit as _show_edit
from delete_page import show_delete as _show_delete


class App:
    def __init__(self, page: Page):
        self.page = page
        self.file_picker = FilePicker()
        self.page.overlay.append(self.file_picker)

        self.app_scale = 1.0
        self.is_mobile = False
        self.mobile_toggled = False
        self.dev_tools_visible = False
        self.current_page = "main"

        self.drawer_open = False
        self.drawer_panel = None
        self.drawer_overlay = None

        self.bg = "#041955"
        self.fg = "#3450a1"
        self.page.bgcolor = self.bg
        self.page.padding = 0

        self.is_mobile = self.page.width < 600 or str(self.page.platform) in ["android", "ios"]

        db_path = get_db_path()
        ensure_db_exists(db_path)
        self.conn, self.cursor = connect_db(db_path)

        self.row_ids = []

        self.balance_text = Text(color="white", size=28, weight=FontWeight.BOLD)
        self.income_text = Text(color="white")
        self.outcome_text = Text(color="white")

        self.search_input = TextField(
            label="Поиск",
            width=200,
            color="white",
            label_style=TextStyle(color="white")
        )

        self.date_filter = TextField(
            label="Дата",
            width=150,
            color="white",
            label_style=TextStyle(color="white")
        )

        self.year_dropdown = Dropdown(
            label="Год",
            width=120,
            color="white",
            label_style=TextStyle(color="white")
        )

        self.table = DataTable(
            columns=[
                DataColumn(Text(c, color="white")) for c in [
                    "№", "Название", "Размер", "Материал", "Цена",
                    "Продано", "Изготовлено", "Ст-сть мат-ов",
                    "Изготовление", "Себестоимость", "Время",
                    "Серия", "Дата", "Остаток", "Прибыль", "Наценка %"
                ]
            ],
            rows=[]
        )

        self.categories_column = Column(scroll=ScrollMode.AUTO)

        self.cb_sold = self._make_cb("Продано")
        self.cb_made = self._make_cb("Изготовлено")
        self.cb_cost = self._make_cb("Себестоимость")
        self.cb_remainder = self._make_cb("Остаток")
        self.cb_profit = self._make_cb("Прибыль")

        self.total_text = Text(color="white", size=16, weight=FontWeight.BOLD)

        self.show_main()

    def _make_cb(self, label):
        return Checkbox(
            label=label,
            on_change=lambda e: self._calc_total(),
            label_style=TextStyle(color="white"),
            check_color="#ffffff",
            active_color="#5f4bdb",
            fill_color="#5f4bdb"
        )

    def _calc_total(self):
        from data_service import calc_total
        calc_total(self)

    def show_snack(self, text, color="green"):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="white"),
                ft.Text(text, color="white")
            ]),
            bgcolor=color,
            duration=2000,
            open=True
        )
        self.page.update()

    def show_main(self):
        _show_main(self)

    def show_create(self, e):
        _show_create(self, e)

    def show_edit(self, e):
        _show_edit(self, e)

    def show_delete(self, e):
        _show_delete(self, e)
