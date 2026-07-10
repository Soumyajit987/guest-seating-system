from flask import Flask, render_template, request
from parser import parse_file
from seating import generate_seating

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    seating = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            guests = parse_file(file)
            tables = int(request.form["tables"])
            capacity = int(request.form["capacity"])

            seating = generate_seating(
                guests,
                tables,
                capacity
            )

    return render_template("index.html", seating=seating)

if __name__ == "__main__":
    app.run(debug=True)