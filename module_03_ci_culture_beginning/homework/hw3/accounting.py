from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<number>")
def add(date: str, number: str):
    if len(date) != 8 or not date.isdigit():
        return "Invalid date format. Use YYYYMMDD", 400
    try:
        num = int(number)
    except ValueError:
        return "Invalid number", 400
    storage[date] = num
    return f"Добавлено: {date} – {num} руб."


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    total = 0
    for date_str, amount in storage.items():
        if date_str.startswith(str(year)):
            total += amount
    return str(total)


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if month < 1 or month > 12:
        return "Invalid month", 400
    month_str = f"{month:02d}"
    total = 0
    for date_str, amount in storage.items():
        if date_str.startswith(f"{year}{month_str}"):
            total += amount
    return str(total)


if __name__ == "__main__":
    app.run(debug=True)