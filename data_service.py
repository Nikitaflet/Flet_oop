from datetime import datetime
from flet import (
    Text, DropdownOption, DataRow, DataCell,
    Container, Column, Divider, FontWeight
)

from database import to_float, get_year_from_date, calc_values


def load_years(cursor, year_dropdown):
    cursor.execute("SELECT DISTINCT date FROM products WHERE date IS NOT NULL")
    years = set()
    for (date,) in cursor.fetchall():
        y = get_year_from_date(date)
        if y:
            years.add(y)
    years = sorted(years, reverse=True)
    if not years:
        years = [datetime.now().year]
    year_dropdown.options = [DropdownOption(str(y)) for y in years]
    if year_dropdown.value is None or year_dropdown.value == "":
        year_dropdown.value = str(years[0])


def load_data(app):
    app.table.rows.clear()
    app.row_ids.clear()

    def t(v):
        return Text(str(v), color="white")

    search = app.search_input.value.lower() if app.search_input.value else ""
    date_f = app.date_filter.value if app.date_filter.value else ""
    selected_year = app.year_dropdown.value if app.year_dropdown.value else None

    query = "SELECT * FROM products"
    conditions = []
    params = []

    if search:
        conditions.append("(LOWER(name) LIKE ? OR LOWER(series) LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])
    if date_f:
        conditions.append("date LIKE ?")
        params.append(f"%{date_f}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    app.cursor.execute(query, params)
    rows = app.cursor.fetchall()

    for i, row in enumerate(rows, start=1):
        if selected_year:
            y = get_year_from_date(row[12])
            if y != int(selected_year):
                continue

        app.row_ids.append(row[0])

        cost, work, remainder, profit, markup = calc_values(
            row[4], row[5], row[6], row[8], row[10]
        )

        app.table.rows.append(
            DataRow(cells=[
                DataCell(t(i)),
                DataCell(t(row[1])),
                DataCell(t(row[2])),
                DataCell(t(row[3])),
                DataCell(t(row[4])),
                DataCell(t(row[5])),
                DataCell(t(row[6])),
                DataCell(t(row[8])),
                DataCell(t(round(work, 2))),
                DataCell(t(round(cost, 2))),
                DataCell(t(row[10])),
                DataCell(t(row[11])),
                DataCell(t(row[12])),
                DataCell(t(round(remainder, 2))),
                DataCell(t(round(profit, 2))),
                DataCell(t(round(markup, 2))),
            ])
        )

    calc_total(app)


def calc_total(app):
    total = 0
    for row in app.table.rows:
        cells = row.cells
        if app.cb_sold.value:
            total += to_float(cells[5].content.value)
        if app.cb_made.value:
            total += to_float(cells[6].content.value)
        if app.cb_cost.value:
            total += to_float(cells[9].content.value)
        if app.cb_remainder.value:
            total += to_float(cells[13].content.value)
        if app.cb_profit.value:
            total += to_float(cells[14].content.value)
    app.total_text.value = f"Итого: {round(total, 2)}"
    app.page.update()


def update_balance(app):
    selected_year = app.year_dropdown.value if app.year_dropdown.value else None
    app.cursor.execute("SELECT price, sold, materials_cost, time, date FROM products")
    income = 0
    outcome = 0
    for p, s, m, t, d in app.cursor.fetchall():
        if selected_year:
            y = get_year_from_date(d)
            if y != int(selected_year):
                continue
        p = to_float(p)
        s = to_float(s)
        m = to_float(m)
        t = to_float(t)
        work = t * 500
        cost = m + work
        income += p * s
        outcome += cost * s
    app.balance_text.value = f"{round(income - outcome, 2)} ₽"
    app.income_text.value = f"Доход: {round(income, 2)} ₽"
    app.outcome_text.value = f"Расход: {round(outcome, 2)} ₽"


def update_categories(app):
    selected_year = app.year_dropdown.value if app.year_dropdown.value else None
    app.cursor.execute("SELECT series, name, price, materials_cost, sold, time, date FROM products")
    income_map = {}
    for series, name, price, mat, sold, time, d in app.cursor.fetchall():
        if selected_year:
            y = get_year_from_date(d)
            if y != int(selected_year):
                continue
        price_f = to_float(price)
        sold_f = to_float(sold)
        mat_f = to_float(mat)
        time_f = to_float(time)
        work = time_f * 500
        cost = mat_f + work
        income = price_f * sold_f
        outcome = cost * sold_f
        markup = (price_f / cost * 100) if cost != 0 else 0
        if series not in income_map:
            income_map[series] = []
        income_map[series].append((name, income, outcome, markup))

    app.categories_column.controls.clear()
    for series, items in income_map.items():
        total_income = sum(i[1] for i in items)
        total_cost = sum(i[2] for i in items)
        avg_markup = sum(i[3] for i in items) / len(items) if items else 0
        app.categories_column.controls.append(
            Container(
                padding=15,
                bgcolor="#2a2f77",
                border_radius=20,
                content=Column([
                    Text(series, color="white", weight=FontWeight.BOLD),
                    Column([Text(name, color="white70", size=12) for name, _, _, _ in items]),
                    Divider(color="white24"),
                    Text(f"Доход: {round(total_income, 2)} ₽", color="green"),
                    Text(f"Себестоимость: {round(total_cost, 2)} ₽", color="red"),
                    Text(f"Наценка: {round(avg_markup, 2)}%", color="yellow")
                ])
            )
        )


def refresh_all(app):
    load_years(app.cursor, app.year_dropdown)
    load_data(app)
    update_balance(app)
    update_categories(app)
    app.page.update()
