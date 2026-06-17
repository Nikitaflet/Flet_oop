from flet import *
from database import calc_values


def show_edit(app, e):
    app.page.clean()
    tf_width = None if app.is_mobile else 200

    inp = TextField(
        label="№ строки",
        width=tf_width,
        color="white",
        label_style=TextStyle(color="white")
    )

    def build_form(values=None):
        tf_style = dict(
            color="white",
            label_style=TextStyle(color="white"),
            border_color="black",
            focused_border_color="black",
            cursor_color="white",
            filled=False,
        )

        name = TextField(label="Название", value=values[0] if values else "", width=tf_width, **tf_style)
        size = TextField(label="Размер", value=values[1] if values else "", width=tf_width, **tf_style)
        material = TextField(label="Материал", value=values[2] if values else "", width=tf_width, **tf_style)
        price = TextField(label="Цена", value=values[3] if values else "", width=tf_width, **tf_style)
        sold = TextField(label="Продано", value=values[4] if values else "", width=tf_width, **tf_style)
        made = TextField(label="Изготовлено", value=values[5] if values else "", width=tf_width, **tf_style)
        mat_cost = TextField(label="Ст-сть мат-ов", value=values[6] if values else "", width=tf_width, **tf_style)
        time = TextField(label="Время", value=values[7] if values else "", width=tf_width, **tf_style)
        series = TextField(label="Серия", value=values[8] if values else "", width=tf_width, **tf_style)
        date = TextField(label="Дата", value=values[9] if values else "", width=tf_width, **tf_style)

        cost = TextField(label="Себестоимость", read_only=True, **tf_style)
        work = TextField(label="Изготовление", read_only=True, **tf_style)
        remainder = TextField(label="Остаток", read_only=True, **tf_style)
        profit = TextField(label="Прибыль", read_only=True, **tf_style)
        markup = TextField(label="Наценка %", read_only=True, **tf_style)

        def calc(e=None):
            c, w, r, p, mu = calc_values(
                price.value, sold.value, made.value, mat_cost.value, time.value
            )
            cost.value = str(round(c, 2))
            work.value = str(round(w, 2))
            remainder.value = str(round(r, 2))
            profit.value = str(round(p, 2))
            markup.value = str(round(mu, 2))
            app.page.update()

        for f in [price, sold, made, mat_cost, time]:
            f.on_change = calc

        calc()

        return (
            name, size, material, price, sold, made,
            mat_cost, time, series, date,
            cost, work, remainder, profit, markup
        )

    def load(_):
        try:
            real_id = app.row_ids[int(inp.value) - 1]
            app.cursor.execute("SELECT * FROM products WHERE id=?", (real_id,))
            row = app.cursor.fetchone()

            values = [
                row[1], row[2], row[3], row[4], row[5],
                row[6], row[8], row[10], row[11], row[12]
            ]

            fields = build_form(values)

            def save(_):
                app.cursor.execute("""
                               UPDATE products
                               SET name=?,
                                   size=?,
                                   material=?,
                                   price=?,
                                   sold=?,
                                   made=?,
                                   materials_cost=?,
                                   time=?,
                                   series=?,
                                   date=?
                               WHERE id = ?
                               """, (
                                   fields[0].value, fields[1].value, fields[2].value,
                                   fields[3].value, fields[4].value, fields[5].value,
                                   fields[6].value, fields[7].value,
                                   fields[8].value, fields[9].value,
                                   real_id
                               ))
                app.conn.commit()
                from main_page import show_main
                show_main(app)

            form_ui = Container(
                padding=20,
                bgcolor="#2a2f77",
                border_radius=20,
                content=Column([
                    Text("Редактировать", size=25, color="white"),
                    inp,
                    Button("Загрузить", on_click=load),
                    Divider(color="white24"),
                    Column(fields[:10], spacing=10),
                    Divider(color="white24"),
                    Column(fields[10:], spacing=10),
                    Row([
                        Button("Сохранить", on_click=save),
                        Button("Назад", on_click=lambda _: app.show_main())
                    ], alignment=MainAxisAlignment.CENTER, spacing=10)
                ],
                    spacing=15,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )

            app.page.clean()
            app.page.add(
                Container(
                    alignment=Alignment(0, 0),
                    expand=True,
                    bgcolor="#041955",
                    content=ListView([
                        Container(
                            width=500 if not app.is_mobile else None,
                            content=form_ui
                        )
                    ])
                )
            )

        except:
            app.page.snack_bar = SnackBar(Text("Ошибка"), open=True)
            app.page.update()

    app.page.add(
        Container(
            alignment=Alignment(0, 0),
            expand=True,
            content=ListView([
                Container(
                    width=500 if not app.is_mobile else None,
                    padding=20,
                    bgcolor="#2a2f77",
                    border_radius=20,
                    content=Column([
                        Text("Редактировать", size=25, color="white"),
                        inp,
                        Button("Загрузить", on_click=load),
                        Row([
                            Button("Назад", on_click=lambda _: app.show_main())
                        ], alignment=MainAxisAlignment.CENTER)
                    ],
                        spacing=15,
                        horizontal_alignment=CrossAxisAlignment.CENTER)
                )
            ])
        )
    )
