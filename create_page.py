from flet import *
from database import to_float, calc_values


def show_create(app, e):
    app.page.clean()
    tf_width = None if app.is_mobile else 200

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
            s_val = to_float(sold.value)
            m_val = to_float(made.value)
            if s_val > m_val:
                sold.error_text = "Ошибка: продано не может быть больше изготовлено"
            else:
                sold.error_text = None
            c, w, r, p, mu = calc_values(price.value, sold.value, made.value, mat_cost.value, time.value)
            cost.value = str(round(c, 2))
            work.value = str(round(w, 2))
            remainder.value = str(round(r, 2))
            profit.value = str(round(p, 2))
            markup.value = str(round(mu, 2))
            app.page.update()

        for f in [price, sold, made, mat_cost, time]:
            f.on_change = calc
        calc()
        return (name, size, material, price, sold, made, mat_cost, time, series, date, cost, work, remainder, profit, markup)

    fields = build_form()

    def save(_):
        app.cursor.execute(
            "INSERT INTO products VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            [fields[0].value, fields[1].value, fields[2].value, fields[3].value,
             fields[4].value, fields[5].value, 0, fields[6].value, 0,
             fields[7].value, fields[8].value, fields[9].value, 0, 0, 0]
        )
        app.conn.commit()
        from main_page import show_main
        show_main(app)

    form_fields = Column([
        Row([fields[0], fields[1]], wrap=True, spacing=10),
        Row([fields[2], fields[3]], wrap=True, spacing=10),
        Row([fields[4], fields[5]], wrap=True, spacing=10),
        Row([fields[6], fields[7]], wrap=True, spacing=10),
        Row([fields[8], fields[9]], wrap=True, spacing=10),
    ], spacing=10)

    calc_fields = Column([
        Row([fields[10], fields[11]], wrap=True, spacing=10),
        Row([fields[12], fields[13]], wrap=True, spacing=10),
        Row([fields[14]], wrap=True, spacing=10),
    ], spacing=10)

    form_ui = Container(
        padding=20,
        bgcolor="#2a2f77",
        border_radius=20,
        content=Column([
            Text("Добавить", size=25, color="white"),
            form_fields,
            Divider(color="white24"),
            Text("Расчёты", color="white"),
            calc_fields,
            Row([
                Button("Сохранить", on_click=save),
                Button("Назад", on_click=lambda _: app.show_main())
            ], alignment=MainAxisAlignment.CENTER, spacing=10)
        ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=15)
    )

    app.page.add(
        Container(
            alignment=Alignment(0, 0),
            expand=True,
            content=ListView(
                [
                    Container(
                        width=500 if not app.is_mobile else None,
                        padding=20,
                        bgcolor="#041955",
                        border_radius=20,
                        content=form_ui
                    )
                ]
            )
        )
    )
