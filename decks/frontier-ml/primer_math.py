"""Unsolved beginner-facing figures, with numerical givens available as alt text."""
import numpy as np
from visual_examples import add, arrows, bars, flow, lines, matrix, scatter, transform
from math_extensions import network


def uniform_area(ax):
    ax.fill_between([0, 4], 0, .25, facecolor="#deedf0", edgecolor="#315e70")
    ax.fill_between([1, 3], 0, .25, facecolor="#58a79c", hatch="//", edgecolor="#315e70")
    ax.set(xlim=(-.3, 4.3), ylim=(0, .33), xticks=range(5),
           xlabel="Variable value", ylabel="Probability density")


def decision_boundary(ax):
    ax.axvspan(2, 4, color="#e0efeb")
    ax.axvline(2, color="#305768", linestyle="--", label="Boundary")
    for label, x, y in [("A", 1, 3), ("B", 3, 1)]:
        ax.plot(x, y, "o", color="#176487")
        ax.annotate(label, (x, y), xytext=(7, 3), textcoords="offset points")
    ax.set(xlim=(0, 4), ylim=(0, 4), xlabel="Feature 1", ylabel="Feature 2")
    ax.legend()


def register():
    add("geometry-read-tip","Read the arrow from tail to tip",
        "Both axes use one unit per tick. The arrow starts at (1,1) and ends at (4,3).",
        arrows("A movement on the coordinate plane",[("movement",(1,1),(4,3))]))
    add("geometry-read-length","Length in two perpendicular directions",
        "The arrow runs three units across and four units up. Its length is the straight-line distance between its endpoints.",
        arrows("Displacement from the origin",[("vector",(0,0),(3,4))]))
    add("geometry-read-dot","Compare two directions",
        "The rightward arrow ends at (2,0). The other ends at (−1,2). The angle between them exceeds a right angle.",
        arrows("Both arrows start at the origin",[("A",(0,0),(2,0)),("B",(0,0),(-1,2))]))
    add("shapes-read-cell","Find an entry by its two indices",
        "Rows are examples; columns are features. Counting starts at zero. The rows are [2,5,1] and [4,3,8].",
        matrix("Two examples",[[2,5,1],[4,3,8]],"Feature","Example"))
    add("shapes-read-product","Multiply matching coordinates",
        "One sample has features [1,3]. For one output, their weights are [2,4]. There is no bias.",
        matrix("Rows: features; columns: sample and weight",[[1,2],[3,4]],"Sample (0) or weight (1)","Feature"))
    add("svd-read-rank","Count independent directions after a map",
        "The dashed outline is a unit square. Every point in the filled input square is mapped onto the horizontal line segment from (0,0) to (2,0).",
        transform("Input outline and transformed grid",[[2,0],[0,0]]))
    add("svd-read-stretch","Compare stretches of the two axes",
        "A unit square aligned with the coordinate axes maps to a rectangle 3 units wide and 2 units tall, with no rotation.",
        transform("Linear map of a unit grid",[[3,0],[0,2]]))
    add("changevar-read-area","Compare unit areas",
        "The input square is one unit wide and tall. The output parallelogram has horizontal base 2 and perpendicular height 1.",
        transform("Image of a square under a linear map",[[2,1],[0,1]]))
    add("jacobian-read-entry","Read a local sensitivity table",
        "Rows correspond to outputs y₀ and y₁. Columns correspond to inputs x₀ and x₁. Entries give local output change per unit input change.",
        matrix("Jacobian at the current point",[[2,-1],[4,3]],"Input","Output"))
    add("chain-read-slope","Read slope as rise divided by run",
        "One point on the straight line is (1,3) and another is (3,7).",
        lines("Output as input changes",[1,2,3],[("Output",[3,5,7])],"Input","Output"))
    add("curvature-read-bend","Two curves share the same bottom",
        "Both curves reach zero at the origin. At x=1, A has risen to 1 and B has risen to 4.",
        lines("Local loss in two directions",np.linspace(-1,1,41),[("A",np.linspace(-1,1,41)**2),("B",4*np.linspace(-1,1,41)**2)],"Step","Loss"))
    add("prob-read-conditional","Choose the right group before dividing",
        "The columns contain people who did or did not receive an alert. The counts are [9,1] in the positive row and [3,87] in the negative row.",
        matrix("Rows: positive, negative; columns: alert, quiet",[[9,1],[3,87]],"Alert (0) or quiet (1)","Actual class"))
    add("variance-read-spread","Same center, different spread",
        "Group A contains 4, 5 and 6; group B contains 1, 5 and 9. Each dot represents one observation.",
        scatter("Horizontal position is the measured value",[("A",[4,5,6],[1]*3),("B",[1,5,9],[0]*3)],"Value","Group row"))
    add("bayes-read-weight","Combine a prior with one observation",
        "The two states start equally likely. The observed clue is three times more likely in state A than in state B.",
        bars("Likelihood of the clue",["A","B"],[.6,.2],"Probability"))
    add("likelihood-read-fit","Read likelihood from a curve",
        "The evidence is three successes and one failure in four independent trials. The curve shows how likely this sequence is at each possible success probability.",
        lines("Likelihood over the unknown parameter",np.linspace(0,1,101),[("Likelihood",np.linspace(0,1,101)**3*(1-np.linspace(0,1,101)))],"Success probability","Likelihood"))
    add("info-read-surprise","Outcome frequencies are unequal",
        "A has probability one-half, B one-quarter, and C and D one-eighth each.",
        bars("Four possible outcomes",list("ABCD"),[.5,.25,.125,.125],"Probability"))
    add("montecarlo-read-average","A mean gives each draw one vote",
        "Four equally weighted samples give function values 1, 2, 2 and 7.",
        bars("Value observed on each draw",list("ABCD"),[1,2,2,7],"Function value"))
    add("statistics-read-interval","Read an uncertainty interval",
        "The endpoints shown are −0.02 and +0.05; zero represents equal performance.",
        lines("Estimated difference between models",[-.02,.05],[("Interval",[1,1])],"Difference in accuracy","Interval"))
    add("pca-read-axis","Choose a direction from a point cloud",
        "The cloud extends from lower left to upper right, close to the line y=x, with little spread across that line.",
        scatter("Centered training data",[("Samples",[-2,-1.5,-.5,.5,1.5,2],[-1.8,-1.7,-.3,.3,1.7,1.8])],"Feature 1","Feature 2"))
    add("classification-read-boundary","Read a classifier boundary",
        "The classifier predicts positive when feature 1 exceeds 2, regardless of feature 2. A=(1,3) and B=(3,1).",
        ("Two examples and a threshold", decision_boundary))
    add("clustering-read-distance","Assign a point to a center",
        "On a number line the cluster centers sit at 1 and 8. The new observation lies at 6.",
        scatter("One-dimensional clustering",[("Centers",[1,8],[0,0]),("New point",[6],[0])],"Feature value",""))
    add("sgd-read-update","Read a downhill step",
        "The loss is the parabola (x−2)². You start at x=0 and may move a small distance left or right.",
        lines("Loss along a single parameter",np.linspace(-1,4,51),[("Loss",(np.linspace(-1,4,51)-2)**2)],"Parameter x","Loss"))
    add("conv-read-window","Follow a sliding window",
        "The signal is [2,4,1,3]. Each output adds two adjacent entries with stride one and no padding. Positions are numbered from zero.",
        matrix("One row of signal samples",[[2,4,1,3]],"Input position",""))
    add("attention-read-row","Read a single attention row",
        "A row contains the weights for one query over three keys. The first row is [0.1,0.7,0.2], the second [0.6,0.1,0.3].",
        matrix("Queries read across rows",[[.1,.7,.2],[.6,.1,.3]],"Key index","Query index"))
    add("flow-read-velocity","Read a velocity from two locations",
        "At time 0 a sample sits at (1,2). At time 1 it sits at (4,4). The path is straight and speed is constant.",
        arrows("One unit of elapsed time",[("Path",(1,2),(4,4))]))
    add("scalegrad-read-product","Trace a fixed compute budget",
        "Each plotted pair has parameters × tokens = 24 in normalized units. The parameter counts shown are 2, 3, 4 and 6.",
        lines("Feasible parameter/token pairs",[2,3,4,6],[("Budget",[12,8,6,4])],"Parameters","Tokens"))
    add("parallel-read-bubble","Read a pipeline schedule",
        "One means busy and zero means idle. Each column is one clock tick, and each row represents a different stage.",
        matrix("Two stages processing three microbatches",[[1,1,1,0],[0,1,1,1]],"Time slot","Stage"))
    add("mdp-read-tree","Read a chance branch",
        "Taking one action has two possible outcomes. One pays 4 with probability ¼ and the other pays 0 with probability ¾.",
        network("Two branches from one action",{"Action":(.15,.5),"¼ → reward 4":(.8,.85),"¾ → reward 0":(.8,.15)},[("Action","¼ → reward 4"),("Action","¾ → reward 0")]))
    add("ppo-read-ratio","Read old and new action probabilities",
        "For the same state and sampled action, the old policy assigns 0.2 and the new policy assigns 0.3.",
        bars("Probability of the sampled action",["Old","New"],[.2,.3],"Probability"))
    add("rewardmodel-read-gap","Read a relative reward",
        "Two answers to the same prompt have scores 1 and 3. In this preference model, only the difference between scores matters.",
        bars("Raw scores",["A","B"],[1,3],"Reward"))
    add("quant-read-grid","Round onto a representable grid",
        "The only representable values near this input are 0, 0.5 and 1. The original activation is 0.62. Use nearest-value rounding.",
        scatter("One real input, three representable levels",[("Levels",[0,.5,1],[0,0,0]),("Input",[.62],[.1])],"Activation",""))
    add("uncertainty-read-coverage","Distinguish answered from correct",
        "A model answers 60 items correctly, answers 20 incorrectly and abstains on the other 20.",
        bars("100 incoming requests",["Correct","Wrong","Abstain"],[60,20,20],"Count"))
    add("tensor-read-broadcast","Compare a row and a column",
        "The input column has shape [2,1]. A row has shape [1,3]. Broadcasting adds every row entry to every column entry.",
        matrix("Column",[[2],[5]]),matrix("Row",[[10,20,30]]))
    add("graphnets-read-hop","Read a graph from its neighbor table",
        "Rows and columns follow A, B, C, D. An entry of one means a direct undirected connection, and zero means there is no edge.",
        matrix("One-hop adjacency",[[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]],"Neighbor index","Node index"))

    add("shapes-read-basis","Read the image of a basis vector",
        "The columns of this matrix tell where the two coordinate arrows land. The first input arrow is (1,0).",
        matrix("Matrix A",[[2,-1],[3,4]],"Input axis","Output coordinate"))
    add("geometry-read-add","Follow two arrows head to tail",
        "The first arrow goes from (0,0) to (2,1). The second begins there and ends at (1,4).",
        arrows("Two successive displacements",[("First",(0,0),(2,1)),("Second",(2,1),(1,4))]))
    add("svd-read-eigen","Check which arrow stays on its line",
        "This map sends (1,0) to (2,0), and (1,1) to (2,3). An eigenvector is a nonzero vector whose image is a scalar multiple of itself.",
        arrows("Candidate A and its image",[("A",(0,0),(1,0)),("Map of A",(0,0),(2,0))]),
        arrows("Candidate B and its image",[("B",(0,0),(1,1)),("Map of B",(0,0),(2,3))]))
    add("prob-read-area","Read a density as an area",
        "A continuous variable is uniform from 0 to 4 with density 0.25 everywhere on that interval. Consider the part from 1 to 3.",
        ("Shaded interval from 1 to 3", uniform_area))
    add("variance-read-covariance","Read how two variables move together",
        "As the horizontal values rise from 1 to 5, the vertical values run 8, 7, 6, 3 and 2.",
        scatter("Five paired observations",[("Pairs",[1,2,3,4,5],[8,7,6,3,2])],"Feature x","Feature y"))
    add("stable-read-normalize","Turn nonnegative weights into probabilities",
        "Exponentiating three logits produced weights 2, 1 and 1. These weights still need to be normalized.",
        bars("Exponentiated scores",list("ABC"),[2,1,1],"Weight"))
    add("info-read-kl","Compare a model with the data source",
        "The source gives A and B equal probability. Model X does the same. Model Y assigns A 0.9 and B 0.1.",
        matrix("Rows: source, model X and model Y",[[.5,.5],[.5,.5],[.9,.1]],"Outcome A or B","Distribution"))
    add("estimation-read-bias","Find the average prediction error",
        "The true value at this input is 5. Three equally likely training samples yield predictors with outputs 6, 7 and 8.",
        bars("Repeated model fits",["Fit 1","Fit 2","Fit 3","Truth"],[6,7,8,5],"Prediction"))
    add("gradsoftmax-read-residual","Compare prediction to target",
        "The classifier assigns probability 0.2 to the correct class C. Its one-hot target for C is 1. Use the logit gradient p minus target.",
        matrix("Predicted and target class mass",[[.3,.5,.2],[0,0,1]],"Class A, B, C","Prediction (0), target (1)"))
    add("calibration-read-bin","Read a forecast bin",
        "Ten items have predicted probability 0.8. Exactly six of them turn out positive.",
        bars("Ten outcomes in a single bin",["Positive","Negative"],[6,4],"Items"))
    add("norm-read-center","Center the features within one token",
        "One token’s two feature values are 2 and 6. For this step, subtract their shared mean without dividing by a standard deviation.",
        bars("One row of activations",["Feature 1","Feature 2"],[2,6],"Activation"))
    add("experts-read-load","Read a router assignment matrix",
        "Each row is a token. An entry of 1 means that token uses the expert in that column. Expert indices begin at zero.",
        matrix("Three tokens and three experts",[[1,0,1],[0,1,1],[1,0,1]],"Expert","Token"))
    add("mdp-read-discount","Put a future payoff in today’s units",
        "You receive zero now and 8 exactly two discount steps from now. Each step multiplies the weight by 0.5.",
        bars("Rewards by time",["Now","Step 1","Step 2"],[0,0,8],"Reward"))
    add("passk-read-subset","Count successful candidate pairs",
        "A pool contains one correct answer A and two incorrect answers B and C. Sample two distinct answers uniformly without replacement.",
        matrix("Rows are the three possible pairs; 1 means included",[[1,1,0],[1,0,1],[0,1,1]],"Candidate A, B, C","Pair index"))
    add("weightquant-read-error","Read a quantization residual",
        "An original scalar weight 1.3 is represented by 1.5 after rounding. Define error as reconstructed minus original.",
        bars("Before and after rounding",["Original","Rounded"],[1.3,1.5],"Weight"))
    add("scalingbreak-read-crossing","Find a break-even point",
        "Plan A starts at zero and costs 4 units per request. Plan B has an 8-unit up-front cost and costs 2 units per request.",
        lines("Cumulative cost",[0,1,2,3,4,5],[("A",[0,4,8,12,16,20]),("B",[8,10,12,14,16,18])],"Requests","Cost units"))
