import os

from flask import Flask, render_template, request
import matplotlib

matplotlib.use("Agg") # supress matplotlib from trying to open a GUI

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

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

        # df = pd.DataFrame({ "Category": [ "Fine Arts", "Humanities", "Physical Sciences", "Life Sciences", "Mathematics"], "Value": [0, 0, 0, 0, 0] })
        # q2xa, q2xb, q2ya, q2yb, q3xa, q3xb, q3ya, q3yb = 0, 0, 0, 0, 0, 0, 0, 0
        # math, phys, life, human, fine = 0, 0, 0, 0, 0

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

        
        plt.tight_layout(); plt.savefig(os.path.join(STATIC_DIR, "graph.png")); plt.close()
        
        
        ############# graph 2

        plt.figure(figsize=(6.5, 6))
        ax = plt.gca()

        plt.scatter(Q2x, Q2y, s=150, color="tomato")

        plt.xlim(-11, 11); plt.ylim(-11, 11)
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
        plt.savefig(os.path.join(STATIC_DIR, "graph1.png"))
        plt.close()

        ############# graph 3


        plt.figure(figsize=(6.5, 6)); ax = plt.gca()


        plt.scatter(Q3x, Q3y, s=150, color="lime")

        plt.xlim(-11, 11); plt.ylim(-11, 11)
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
        plt.savefig(os.path.join(STATIC_DIR, "graph2.png"))
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

        plt.tight_layout(); plt.savefig(os.path.join(STATIC_DIR, "graph3.png")); plt.close()

        ############# CSV
        
        # print to file
        out = pd.DataFrame([{ "Fine Arts": fine, "Humanities": human, "Physical Sciences": phys, "Life Sciences": life, "Mathematics": math,
            "Q2x": Q2x, "Q2y": Q2y, "Q3x": Q3x, "Q3y": Q3y }])
        out.to_csv( "Survey app/responses.csv", mode="a", header=not os.path.exists("Survey app/responses.csv"), index=False)

        # read from file
        try:
            cohort = pd.read_csv("Survey app/responses.csv")#, index_col=0) #this thingy prevents cohort graphs from updating since it messes with which CSV row is index
            cohort.columns = cohort.columns.str.strip()
            print(cohort.head())
            print("COLUMNS:", cohort.columns.tolist())
            required = ["Fine Arts","Humanities","Physical Sciences","Life Sciences","Mathematics", "Q2x","Q2y","Q3x","Q3y" ]#; cohort = cohort[required]
            cohort = cohort.reindex(columns=required)

            ############# cohort graph 1
            colors = ["magenta", "yellow", "coral", "yellowgreen", "turquoise"]
            plot_df = cohort[["Fine Arts","Humanities","Physical Sciences","Life Sciences","Mathematics"] ].melt(var_name="Category", value_name="Value")
            plt.figure(figsize=(4.5,4.5))
            ax = sns.boxplot(data=plot_df, x="Category", y="Value", palette=colors, width=0.5, showfliers=False)
            sns.stripplot(data=plot_df, x="Category", y="Value", palette=colors, jitter=0.1, size=6, alpha=0.65 )
            ax.set_ylim(0,5); ax.set_xlabel(""); ax.set_ylabel(""); ax.set_yticks([])
            for label in ax.get_xticklabels():
                label.set_rotation(30); label.set_fontsize(15); label.set_fontweight("bold")
            plt.tight_layout(); plt.savefig(os.path.join(STATIC_DIR, "cohort_graph.png")); plt.close()

            ############# cohort graph 2
            plt.figure(figsize=(6.5,6)); ax = plt.gca()
            plt.scatter(cohort["Q2x"], cohort["Q2y"], s=70, color="tomato", alpha=0.5 )
            plt.xlim(-11,11); plt.ylim(-11,11); plt.axhline(0,color="black"); plt.axvline(0,color="black")
            ax.set_xticks([]); ax.set_yticks([])

            ax.text(0,11,"Structured Thoughts", ha="center", va="center", fontsize=18, fontweight="bold")
            ax.text(0,-11,"Freeform Thoughts", ha="center", va="center", fontsize=18, fontweight="bold")
            ax.text(11,0,"Few Big Steps", rotation=90, ha="center", va="center", fontsize=18, fontweight="bold")
            ax.text(-11,0,"Many Small Steps", rotation=90, ha="center", va="center", fontsize=18, fontweight="bold")
            plt.tight_layout(); plt.savefig(os.path.join(STATIC_DIR,"cohort_graph1.png")); plt.close()

            ############ cohort graph 3
            plt.figure(figsize=(6.5,6))
            ax = plt.gca()
            plt.scatter(cohort["Q3x"], cohort["Q3y"], s=70, color="lime", alpha=0.5 )
            plt.xlim(-11,11); plt.ylim(-11,11); plt.axhline(0,color="black"); plt.axvline(0,color="black")
            ax.set_xticks([]); ax.set_yticks([])
            ax.text(0,11,"Human Feedback", ha="center", va="center", fontsize=18, fontweight="bold")
            ax.text(0,-11,"Mechanical Testing", ha="center", va="center", fontsize=18, fontweight="bold")
            ax.text(11,0,"Systems Thinking", rotation=90, ha="center", va="center", fontsize=18, fontweight="bold")
            ax.text(-11,0,"Detailed Thinking", rotation=90, ha="center", va="center", fontsize=18, fontweight="bold")
            plt.tight_layout(); plt.savefig(os.path.join(STATIC_DIR,"cohort_graph2.png")); plt.close()

            ############ cohort graph 4
            labels = ["Fine\nArts", "\n\nHumanities", "Life\nSciences", "Physical\nSciences", "Mathematics"]
            angles = np.linspace(0,2*np.pi,N,endpoint=False).tolist(); angles += angles[:1]
            fig = plt.figure(figsize=(5,5)); ax = plt.subplot(111, polar=True); ax.set_ylim(0,5)

            for _, row in cohort.iterrows():
                values = [row["Fine Arts"], row["Humanities"], row["Life Sciences"], row["Physical Sciences"], row["Mathematics"] ]; values += values[:1]
                ax.plot(angles, values, color="dodgerblue", alpha=0.12, linewidth=1 ); ax.fill(angles, values, color="dodgerblue", alpha=0.015 )
            colors = ["magenta","yellow","yellowgreen","coral","turquoise"]
            columns = ["Fine Arts", "Humanities", "Life Sciences", "Physical Sciences", "Mathematics" ]
            for angle, column, color in zip(angles[:-1], columns, colors):
                ax.scatter(np.full(len(cohort), angle), cohort[column], color=color, s=18, alpha=0.75, zorder=10 )
            ax.tick_params(axis='x', pad=25)
            ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels, fontsize=18, fontweight="bold"); ax.set_yticklabels([])
            plt.tight_layout(); plt.savefig(os.path.join(STATIC_DIR,"cohort_graph3.png")); plt.close()
        except Exception as e:
            print("cohort graph error:", e)


        graph_exists = True

    return render_template(
        "index.html",
        graph_exists=graph_exists
    )


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)