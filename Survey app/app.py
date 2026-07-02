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

        fine = float(request.form["fine"])
        human = float(request.form["human"])
        phys = float(request.form["phys"])
        life = float(request.form["life"])
        math = float(request.form["math"])

        df = pd.DataFrame({
            "Category": [
                "Fine Arts",
                "Humanities",
                "Physical Sciences",
                "Life Sciences",
                "Mathematics"
            ],
            "Value": [
                fine,
                human,
                phys,
                life,
                math
            ]
        })

        q2xa = float(request.form["Axa"])
        q2xb = float(request.form["Axb"])
        q2ya = float(request.form["Aya"])
        q2yb = float(request.form["Ayb"])
        q3xa = float(request.form["Bxa"])
        q3xb = float(request.form["Bxb"])
        q3ya = float(request.form["Bya"])
        q3yb = float(request.form["Byb"])

        df2 = pd.DataFrame({
            "Category": [
                "Q2xa",
                "Q2xb",
                "Q2ya",
                "Q2yb",
                "Q3xa",
                "Q3xb",
                "Q3ya",
                "Q3yb"
            ],
            "Value": [
                q2xa,
                q2xb,
                q2ya,
                q2yb,
                q3xa,
                q3xb,
                q3ya,
                q3yb
            ]
        })

        Q2x = ((q2xa - q2xb)*2.5)
        Q2y = ((q2ya - q2yb)*2.5)
        Q3x = ((q3xa - q3xb)*2.5)
        Q3y = ((q3ya - q3yb)*2.5)

        sns.set_theme(style="whitegrid")

        ############# barchart

        plt.figure(figsize=(8,5))
        ax = sns.barplot(data=df, x="Category", y="Value")
        ax.set_ylim(0,5); ax.set_ylabel("Score"); ax.set_title("Personalized Scores")
        plt.tight_layout(); plt.savefig("static/graph.png"); plt.close()
        
        
        ############# graph 2

        plt.figure(figsize=(6, 6))

        plt.scatter(Q2x, Q2y, s=150)

        plt.xlim(-10, 10); plt.ylim(-10, 10)
        plt.axhline(0, color="black", linewidth=1)
        plt.axvline(0, color="black", linewidth=1)
        plt.xlabel("Small Builds <-> Big Builds")
        plt.ylabel("Structured ^ \nFreeform v")
        plt.title("Execution Style")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("static/graph1.png")
        plt.close()

        ############# graph 3


        plt.figure(figsize=(6, 6))

        plt.scatter(Q3x, Q3y, s=150, color="orange")

        plt.xlim(-10, 10); plt.ylim(-10, 10)
        plt.axhline(0, color="black", linewidth=1)
        plt.axvline(0, color="black", linewidth=1)
        plt.xlabel("Systems <-> Details")
        plt.ylabel("Human Feedback ^\nPressure Testing v")
        plt.title("Thinking Style")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("static/graph2.png")
        plt.close()


        graph_exists = True

    return render_template(
        "index.html",
        graph_exists=graph_exists
    )


if __name__ == "__main__":
    app.run(debug=True)