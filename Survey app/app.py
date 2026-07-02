from flask import Flask, render_template, request
import matplotlib

matplotlib.use("Agg") # supress matplotlib from trying to open a GUI

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    graph_exists = False

    if request.method == "POST":

        math = float(request.form["math"])
        science = float(request.form["science"])
        english = float(request.form["english"])
        history = float(request.form["history"])
        art = float(request.form["art"])

        df = pd.DataFrame({
            "Category": [
                "Math",
                "Science",
                "English",
                "History",
                "Art"
            ],
            "Value": [
                math,
                science,
                english,
                history,
                art
            ]
        })

        sns.set_theme(style="whitegrid")

        plt.figure(figsize=(8,5))

        ax = sns.barplot(
            data=df,
            x="Category",
            y="Value"
        )

        ax.set_ylim(0,100)
        ax.set_ylabel("Score")
        ax.set_title("Personalized Scores")

        plt.tight_layout()
        plt.savefig("static/graph.png")
        plt.close()

        graph_exists = True

    return render_template(
        "index.html",
        graph_exists=graph_exists
    )


if __name__ == "__main__":
    app.run(debug=True)