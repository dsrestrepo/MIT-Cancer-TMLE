import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb

import matplotlib
matplotlib.use('TKAgg')


df = pd.read_csv("results/tmle/2A.csv")
df[~((df.sofa_start == 0) & (df.sofa_end == 24))]

# Transform into percentages
df.psi = df.psi * 100
df.i_ci = df.i_ci * 100
df.s_ci = df.s_ci * 100

t_dict = dict(zip(["mech_vent", "rrt", "vasopressor"],
                ["Mechanical Ventilation", "RRT", "Vasopressor(s)"]))

fig, axes = plt.subplots(1, len(t_dict.keys()), sharex=True,  figsize=(8.5,2.5), constrained_layout=True)

fig.suptitle(f'Effect of Invasive Interventions on Mortality, Cancer vs. Non-Cancer Patients')

for i, t in enumerate(t_dict.keys()):

    df_temp1 = df[(df.treatment == t) & (df.cohort == "all")]
    df_temp2 = df[(df.treatment == t) & (df.cohort == "cancer")]
    axes[i].set(xlabel=None)
    axes[i].set(ylabel=None)

    axes[i].errorbar(x=df_temp1.sofa_start, y=df_temp1.psi, 
                    yerr=((df_temp1.psi- df_temp1.i_ci), (df_temp1.s_ci-df_temp1.psi)),
                    fmt='-o', c='tab:gray', ecolor='tab:gray',
                    elinewidth=.4, linewidth=1.5, capsize=4, markeredgewidth=.4,
                    label="Non-Cancer")
    
    axes[i].errorbar(x=df_temp2.sofa_start, y=df_temp2.psi,
                    yerr=((df_temp2.psi- df_temp2.i_ci), (df_temp2.s_ci-df_temp2.psi)),
                    fmt='-o', c='tab:red', ecolor='tab:red',
                    elinewidth=.4, linewidth=1.5, capsize=4, markeredgewidth=.4,
                    label="Cancer")

    axes[i].axhline(y=0, xmin=0, xmax=1, c="black", linewidth=.7, linestyle='--')
    axes[i].set_ylim([-30, 30])
    axes[i].set_title(t_dict[t])
    axes[0].set(ylabel="ATE (%)\nTreated vs. Not Treated")
    axes[2].legend(bbox_to_anchor=(1.05, 0.7), loc='upper left')

    axes[i].set_xticklabels(["0-3", "4-6", "7-10", ">10"])
    axes[i].set_xticks([0, 4, 7, 11])

fig.supxlabel('SOFA Range            ')

fig.savefig(f"results/tmle/2A.png", dpi=300)



