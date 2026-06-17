import os
import shutil
import flet as ft

from database import get_db_path, connect_db
from data_service import refresh_all


def export_db(app, e):
    async def do_save():
        try:
            directory = await app.file_picker.get_directory_path()
            if not directory:
                return

            export_path = os.path.join(directory, "data_backup.db")
            if app.conn:
                app.conn.commit()
            shutil.copy2(get_db_path(), export_path)

            app.page.snack_bar = ft.SnackBar(
                ft.Text(f"Сохранено:\n{export_path}"),
                open=True
            )
        except Exception as ex:
            app.page.snack_bar = ft.SnackBar(
                ft.Text(f"Ошибка: {ex}"),
                open=True
            )
        app.page.update()

    app.page.run_task(do_save)


def import_db(app, e):
    async def do_pick():
        try:
            result = await app.file_picker.pick_files(allowed_extensions=["db"])
            if not result:
                return

            src = result[0].path
            db_path = get_db_path()

            if app.conn:
                app.conn.close()

            shutil.copy2(src, db_path)
            app.conn, app.cursor = connect_db(db_path)

            refresh_all(app)
            app.show_snack("📥 Импорт выполнен")
        except Exception as ex:
            app.show_snack(f"Ошибка: {ex}")

    app.page.run_task(do_pick)
