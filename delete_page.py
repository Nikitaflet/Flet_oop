from flet import *


def show_delete(app, e):
    app.page.clean()
    tf_width = None if app.is_mobile else 200
    inp = TextField(
        label="№ строки",
        width=tf_width,
        color="white",
        label_style=TextStyle(color="white")
    )

    def delete_row(_):
        try:
            real_id = app.row_ids[int(inp.value) - 1]
            app.cursor.execute("DELETE FROM products WHERE id=?", (real_id,))
            app.conn.commit()
            from main_page import show_main
            show_main(app)
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
                        Text("Удалить", size=25, color="white"),
                        inp,
                        Row([
                            Button(
                                "Удалить",
                                on_click=delete_row,
                                bgcolor="#e53935",
                                color="white"
                            ),
                            Button("Назад", on_click=lambda _: app.show_main())
                        ], alignment=MainAxisAlignment.CENTER, spacing=10)
                    ],
                        spacing=15,
                        horizontal_alignment=CrossAxisAlignment.CENTER)
                )
            ])
        )
    )
