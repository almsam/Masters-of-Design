from flask import Flask, render_template, request
import matplotlib

matplotlib.use("Agg") # supress matplotlib from trying to open a GUI

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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

        sns.set_theme(style="dark")

        ############# barchart

        colors = ["magenta", "yellow", "coral", "yellowgreen", "turquoise"]
        plt.figure(figsize=(4.5,4.5))
        plt.xlabel(""); plt.ylabel("")
        ax = sns.barplot(data=df, x="Category", y="Value", palette=colors)
        ax.set_ylim(0,5)#; ax.set_ylabel("Score")
        ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
        
        bold_labels = {"Fine Arts", "Humanities", "Physical Sciences", "Life Sciences", "Mathematics"}
        for label in ax.get_xticklabels():
            if label.get_text() in bold_labels: label.set_fontweight("bold"); label.set_fontsize(15); label.set_rotation(30)

        
        plt.tight_layout(); plt.savefig("static/graph.png"); plt.close()
        
        
        ############# graph 2

        plt.figure(figsize=(6.5, 6))
        ax = plt.gca()

        plt.scatter(Q2x, Q2y, s=150, color="tomato")

        plt.xlim(-10, 10); plt.ylim(-10, 10)
        plt.axhline(0, color="black", linewidth=1)
        plt.axvline(0, color="black", linewidth=1)
        
        ax.set_xticks([]); ax.set_yticks([])
        
        ax.text(0, 11, "Structured Thoughts", ha="center", va="center", fontsize=18, fontweight="bold")
        ax.text(0, -11, "Freeform Thoughts", ha="center", va="center", fontsize=18, fontweight="bold")
        ax.text(11, 0, "Few Big Steps", ha="center", va="center", fontsize=18, fontweight="bold", rotation=90)
        ax.text(-11, 0, "Many Small Steps", ha="center", va="center", fontsize=18, fontweight="bold", rotation=90)
        # plt.xlabel("Small Builds <-> Big Builds")
        # plt.ylabel("Structured ^ \nFreeform v")
        # plt.title("Execution Style")
        # plt.grid(True)
        plt.tight_layout()
        plt.savefig("static/graph1.png")
        plt.close()

        ############# graph 3


        plt.figure(figsize=(6.5, 6)); ax = plt.gca()


        plt.scatter(Q3x, Q3y, s=150, color="lime")

        plt.xlim(-10, 10); plt.ylim(-10, 10)
        plt.axhline(0, color="black", linewidth=1)
        plt.axvline(0, color="black", linewidth=1)
        
        ax.set_xticks([]); ax.set_yticks([])
        
        ax.text(0, 11, "Human Feedback", ha="center", va="center", fontsize=18, fontweight="bold")
        ax.text(0, -11, "Mechanical Testing", ha="center", va="center", fontsize=18, fontweight="bold")
        ax.text(11, 0, "Systems Thinking", ha="center", va="center", fontsize=18, fontweight="bold", rotation=90)
        ax.text(-11, 0, "Detailed Thinking", ha="center", va="center", fontsize=18, fontweight="bold", rotation=90)
        # plt.xlabel("Human Feedback^\nSystems <---> Details\nMechanical Testing v")
        # plt.ylabel("")#Human Feedback ^\nPressure Testing v")
        # plt.title("Thinking Style")
        # plt.grid(True)
        plt.tight_layout()
        plt.savefig("static/graph2.png")
        plt.close()

        ############# graph 4


        
        labels = ["Fine\nArts", "\n\nHumanities", "Life\nSciences", "Physical\nSciences", "Mathematics"]
        values = [fine, human, life, phys, math]; N = len(labels)

        # find our angles for each axis
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values += values[:1]; angles += angles[:1]

        fig = plt.figure(figsize=(5, 5))
        ax = plt.subplot(111, polar=True)
        
                # rainbow colors?
        # colors = ["purple", "gold", "green", "blue", "white"]#plt.cm.hsv(np.linspace(0, 1, N))
        colors = ["cyan", "lime", "yellow", "coral", "violet"]#plt.cm.hsv(np.linspace(0, 1, N))

        # draw colored segments
        for i in range(N):
            ax.fill(
                [angles[i], angles[i+1], angles[i+1], angles[i]],
                [0, 0, values[i+1], values[i]],
                color=colors[i],
                alpha=0.5
            )
        
        ax.plot(angles, values, linewidth=2, color="black")
        ax.fill(angles, values, alpha=0.35)#, color="dodgerblue")

        ax.tick_params(axis='x', pad=25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=18, fontweight="bold")
        ax.set_yticklabels([])
        ax.set_ylim(0, 5)

        plt.tight_layout(); plt.savefig("static/graph3.png"); plt.close()



        graph_exists = True

    return render_template(
        "index.html",
        graph_exists=graph_exists
    )


if __name__ == "__main__":
    app.run(debug=True)