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

        score = float(request.form["score"])

        df = pd.DataFrame({
            "Category": ["Your Score"],
            "Value": [score]
        })

        sns.set_theme(style="whitegrid")

        plt.figure(figsize=(6,4))

        ax = sns.barplot(
            data=df,
            x="Category",
            y="Value"
        )

        ax.set_ylim(0,100)
        ax.set_title("Personalized Score")

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