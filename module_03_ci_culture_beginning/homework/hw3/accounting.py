from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    storage[date] = number
    return f"Добавлено: {date} – {number} руб."


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    total = 0
    for date_str, amount in storage.items():
        if date_str.startswith(str(year)):
            total += amount
    return str(total)


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    total = 0
    month_str = f"{month:02d}"
    for date_str, amount in storage.items():
        if date_str.startswith(f"{year}{month_str}"):
            total += amount
    return str(total)


if __name__ == "__main__":
    app.run(debug=True)