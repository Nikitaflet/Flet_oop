from flet import *
from data_service import refresh_all
from import_export import export_db, import_db


def show_main(app):
    app.current_page = "main"
    app.page.controls.clear()
    app.page.overlay.clear()
    app.page.update()

    def close_drawer():
        app.drawer_panel.left = -260
        app.drawer_overlay.opacity = 0
        app.drawer_overlay.visible = False
        app.page.update()

    def open_drawer():
        app.drawer_panel.left = 0
        app.drawer_overlay.opacity = 0.5
        app.drawer_overlay.visible = True
        app.page.update()

    def overlay_click(e):
        close_drawer()

    app.drawer_overlay = Container(
        bgcolor="#88000000",
        expand=True,
        on_click=overlay_click,
        visible=False,
        opacity=0,
        left=0, top=0, right=0, bottom=0
    )

    app.drawer_panel = Container(
        width=260,
        bgcolor="#1a1a5e",
        padding=10,
        left=-260,
        top=0, bottom=0,
        content=Column([
            Container(height=20),
            Row([
                Icon(Icons.STORAGE, color="white"),
                Container(width=10),
                Text("Меню", color="white", size=18, weight=FontWeight.BOLD),
            ]),
            Divider(color="white24"),
            ListTile(
                leading=Icon(Icons.HOME, color="white"),
                title=Text("Главная", color="white"),
                on_click=lambda _: close_drawer(),
            ),
            Divider(color="white24"),
            Text("  Android", color="white54", size=12),
            ListTile(
                leading=Icon(Icons.UPLOAD, color="white"),
                title=Text("Экспорт БД", color="white"),
                on_click=lambda e: export_db(app, e),
            ),
            ListTile(
                leading=Icon(Icons.DOWNLOAD, color="white"),
                title=Text("Импорт БД", color="white"),
                on_click=lambda e: import_db(app, e),
            ),
        ])
    )

    app.page.overlay.extend([app.drawer_overlay, app.drawer_panel])

    app.search_input.on_change = lambda e: refresh_all(app)
    app.date_filter.on_change = lambda e: refresh_all(app)
    app.year_dropdown.on_change = lambda e: refresh_all(app)
    from data_service import load_years
    load_years(app.cursor, app.year_dropdown)

    if app.is_mobile:
        app.search_input.label = "Поиск"
        app.date_filter.label = "Дата"
        app.year_dropdown.width = 100
        app.search_input.width = None
        app.date_filter.width = None
    else:
        app.search_input.width = 200
        app.date_filter.width = 150
        app.year_dropdown.width = 120

    def zoom_in(_):
        app.app_scale = min(app.app_scale + 0.1, 2.0)
        app.page.clean()
        show_main(app)

    def zoom_out(_):
        app.app_scale = max(app.app_scale - 0.1, 0.5)
        app.page.clean()
        show_main(app)

    def toggle_mobile(_):
        app.mobile_toggled = True
        app.is_mobile = not app.is_mobile
        app.page.clean()
        show_main(app)

    title_size = 24 if app.is_mobile else 20

    header = Row(
        alignment=MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            Row([
                IconButton(Icons.MENU, icon_color="white", on_click=lambda _: open_drawer()),
                Text("Учет производства", color="white", size=title_size, weight=FontWeight.BOLD),
            ]),
            Row([
                IconButton(Icons.PHONE_ANDROID, icon_color="white", on_click=toggle_mobile, tooltip="Переключить мобильный/ПК", visible=app.dev_tools_visible),
                IconButton(Icons.REMOVE, icon_color="white", on_click=zoom_out, tooltip="Уменьшить", visible=app.dev_tools_visible),
                IconButton(Icons.ADD, icon_color="white", on_click=zoom_in, tooltip="Увеличить", visible=app.dev_tools_visible),
            ])
        ],
        expand=True
    )

    if app.is_mobile:
        filter_column = Column([
            Row([app.search_input], alignment=MainAxisAlignment.CENTER),
            Row([app.date_filter], alignment=MainAxisAlignment.CENTER),
            Row([app.year_dropdown], alignment=MainAxisAlignment.CENTER),
            Row([Button("Обновить", on_click=lambda _: refresh_all(app))], alignment=MainAxisAlignment.CENTER)
        ], spacing=10)
    else:
        filter_column = Row([
            app.search_input, app.date_filter, app.year_dropdown,
            Button("Обновить", on_click=lambda _: refresh_all(app))
        ], spacing=10, alignment=MainAxisAlignment.CENTER)

    if app.is_mobile:
        cards_section = Container(
            content=Column([
                Container(
                    padding=20,
                    bgcolor="#5f4bdb",
                    border_radius=15,
                    content=Column([
                        Text("Баланс", color="white", weight=FontWeight.BOLD, size=18),
                        app.balance_text,
                        app.income_text,
                        app.outcome_text
                    ], horizontal_alignment=CrossAxisAlignment.CENTER, alignment=MainAxisAlignment.CENTER),
                    alignment=Alignment(0, 0),
                    expand=True
                ),
                Container(
                    padding=10,
                    bgcolor=app.fg,
                    border_radius=15,
                    content=Column([
                        Text("Категории", color="white", weight=FontWeight.BOLD, size=18),
                        app.categories_column
                    ], horizontal_alignment=CrossAxisAlignment.CENTER, scroll=ScrollMode.AUTO),
                    alignment=Alignment(0, 0),
                    expand=True,
                    height=300
                )
            ], spacing=10, expand=True),
            alignment=Alignment(0, 0),
            expand=True
        )
    else:
        cards_section = Container(
            content=Row([
                Container(
                    padding=20,
                    bgcolor="#5f4bdb",
                    border_radius=15,
                    content=Column([
                        Text("Баланс", color="white", weight=FontWeight.BOLD, size=18),
                        app.balance_text,
                        app.income_text,
                        app.outcome_text
                    ], horizontal_alignment=CrossAxisAlignment.CENTER, alignment=MainAxisAlignment.CENTER),
                    alignment=Alignment(0, 0),
                    expand=True,
                    height=300
                ),
                Container(
                    padding=10,
                    bgcolor=app.fg,
                    border_radius=15,
                    content=Column([
                        Text("Категории", color="white", weight=FontWeight.BOLD, size=18),
                        app.categories_column
                    ], horizontal_alignment=CrossAxisAlignment.CENTER, scroll=ScrollMode.AUTO),
                    alignment=Alignment(0, 0),
                    expand=True,
                    height=300
                ),
            ], spacing=15, expand=True),
            alignment=Alignment(0, 0),
            padding=15,
            bgcolor=app.bg,
            expand=True
        )

    table_container = Container(
        padding=10,
        bgcolor=app.fg,
        border_radius=15,
        content=Row([
            Container(content=app.table, width=None)
        ], scroll=ScrollMode.AUTO),
        alignment=Alignment(0, 0)
    )

    totals_container = Container(
        padding=15,
        bgcolor="#2a2f77",
        border_radius=15,
        content=Column([
            Text("Итоги (выберите столбцы):", color="white", weight=FontWeight.BOLD, size=16),
            Row([app.cb_sold, app.cb_made, app.cb_cost, app.cb_remainder, app.cb_profit], wrap=True),
            app.total_text
        ]),
        alignment=Alignment(0, 0)
    )

    buttons_row = Container(
        content=Row([
            Button("Добавить", on_click=lambda e: app.show_create(e)),
            Button("Редактировать", on_click=lambda e: app.show_edit(e)),
            Button("Удалить", on_click=lambda e: app.show_delete(e))
        ], wrap=True, spacing=10),
        alignment=Alignment(0, 0)
    )

    main_content = Column([
        Container(header, alignment=Alignment(0, 0)),
        Container(filter_column, alignment=Alignment(0, 0)),
        Container(cards_section, alignment=Alignment(0, 0)),
        Container(table_container, alignment=Alignment(0, 0)),
        Container(totals_container, alignment=Alignment(0, 0)),
        Container(buttons_row, alignment=Alignment(0, 0))
    ], spacing=15, alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER)

    app.page.add(
        Container(
            content=ListView([Container(content=main_content, alignment=Alignment(0, 0))]),
            alignment=Alignment(0, 0),
            expand=True
        )
    )

    def on_keyboard(e: KeyboardEvent):
        if e.shift and e.key == "D":
            app.dev_tools_visible = not app.dev_tools_visible
            app.page.clean()
            show_main(app)

    app.page.on_keyboard_event = on_keyboard
    refresh_all(app)
