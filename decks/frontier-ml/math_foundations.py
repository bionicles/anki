"""Worked numerical examples for the mathematics and statistics stage."""
import numpy as np
from visual_examples import add, matrix, bars, lines, arrows, transform, flow, scatter


def power_panel(ax):
    z = np.linspace(-3, 6, 361)
    for mean, label, style in [(0, "Null", "--"), (2, "Alternative", "-")]:
        density = np.exp(-.5 * (z - mean)**2) / np.sqrt(2 * np.pi)
        ax.plot(z, density, style, label=label)
        if mean == 2:
            ax.fill_between(z, density, where=z >= 1.645, color="#acd8ce", interpolate=True)
    ax.axvline(1.645, linestyle=":", color="black", label="Cutoff 1.645")
    ax.set(xlabel="Test statistic z", ylabel="Density", ylim=(0, .47))
    ax.legend(fontsize=9)


def register():
    t = np.linspace(-2,2,101)
    p = np.linspace(.01,.99,99)
    add("shapes-1","One output is a row meeting a column",
        "Read across one example and down one output column. Match features before adding: 2×4 + 3×5 = 23.",
        matrix("One example, two features",[[2,3]],"Feature","Example"),
        matrix("Weights for one output",[[4],[5]],"Output","Feature"))
    add("shapes-2","Apply the same map at every position",
        "Batch and token tell you where to look. Only the feature vector changes width, from 64 numbers to 24.",
        flow("Zoom in on one token",["8 batches × 16 tokens","One token has 64 features","Multiply by a 64 × 24 matrix","Put 24 outputs back at that token"]))
    add("shapes-3","Each weight collects evidence across examples",
        "For one input feature and one output, the gradient is 2×4 + 3×5 = 23. The batch axis disappears in XᵀG.",
        matrix("Rows are examples; columns are input and upstream signal",[[2,4],[3,5]],"Input (0) or signal (1)","Example"))
    add("shapes-4","A transpose swaps the axes",
        "Two examples with three features become three rows of two after transposition. A square test fixture hides this shape change.",
        matrix("Before",[[1,2,3],[4,5,6]],"Feature","Example"),
        matrix("After",[[1,4],[2,5],[3,6]],"Example","Feature"))
    add("geometry-1","A projection is a shadow on a line",
        "For x=(3,2) and horizontal unit u, the shadow reaches (3,0). The vertical leftover is perpendicular to u.",
        arrows("Input, shadow and leftover",[("x",(0,0),(3,2)),("shadow",(0,0),(3,0)),("leftover",(3,0),(3,2))]))
    add("geometry-3 geometry-4","Separate direction from vector length",
        "Relative to a horizontal query, A points closer, but B reaches farther right. Normalization removes B’s length advantage.",
        arrows("Original candidates",[("A",(0,0),(1,0)),("B",(0,0),(3,3))]),
        arrows("Both rescaled to unit length",[("A",(0,0),(1,0)),("B",(0,0),(.7071,.7071))]))
    add("svd-1","Rank one keeps one direction of stretch",
        "The full map stretches the square by 3 horizontally and 1 vertically. The best rank-one approximation keeps the stronger stretch and collapses the other axis.",
        transform("Full map",[[3,0],[0,1]]),transform("Rank-one map",[[3,0],[0,0]]))
    add("svd-3","A thin factorization has a narrow middle",
        "The input first becomes two coordinates. A second map uses those coordinates to build the four outputs. The large product need never be stored.",
        flow("Example with rank two",["6 input coordinates","2 × 6 matrix → 2 coordinates","4 × 2 matrix → 4 outputs"]))
    add("svd-4","Forming the Gram matrix squares the spread",
        "A diagonal X with stretches 10 and 1 has condition number 10. Its Gram matrix stretches by 100 and 1, giving condition number 100.",
        matrix("X",[[10,0],[0,1]]),matrix("XᵀX",[[100,0],[0,1]]))
    add("prob-1","Conditioning restricts the denominator",
        "Among the ten observations in column 1, eight are in row 0. Conditioning on that column gives 8/10.",
        matrix("Joint counts",[[2,8],[8,2]],"B category","A category"))
    add("prob-2 prob-3","Prior frequency changes what an alert means",
        "Among 10,000 cases, 100 are positive. Nine hundred ninety false alerts outweigh 90 true ones. The positive-alert fraction is 90/1,080.",
        bars("Alerts from two populations",["True alerts","False alerts"],[90,990],"Cases"))
    add("prob-4","A shared cause can move two measurements",
        "In this example, temperature drives both counts. Their association alone cannot identify a causal effect from either count to the other.",
        scatter("One observation per day",[("days",[2,4,6,8,10],[3,5,7,8,12])],"Cold drinks sold","Swimmers"),
        bars("Common driver across the five days",list("ABCDE"),[15,19,22,25,30],"Temperature (°C)"))
    add("variance-1 statistics-2","Averaging reduces independent noise",
        "The curve follows 1/√n. Moving from 25 to 100 observations halves standard error, which lets a comparable design distinguish a smaller effect.",
        lines("Unit population standard deviation",[4,16,25,64,100],[("SE",[.5,.25,.2,.125,.1])],"Independent observations","Standard error"))
    add("variance-3","Repeated turns share their conversation",
        "Turns within each conversation cluster closely. Counting every dot as independent misses the larger variation between conversations.",
        scatter("Example turn scores",[(str(i),[i-.04,i,i+.04],[m-.02,m,m+.02]) for i,m in enumerate([.20,.55,.85],1)],"Conversation","Score"))
    add("variance-4","Pairing removes shared case difficulty",
        "The models rise and fall on the same cases. Their paired differences are much steadier than either set of raw scores.",
        lines("Same cases for both models",[1,2,3,4],[("A",[.25,.8,.45,.95]),("B",[.20,.73,.40,.87])],"Case","Score"))
    add("chain-1","Backprop sends sensitivity upstream",
        "For y=3x and loss L=y² at x=2, a small increase in y changes loss at rate 12. The local multiplier 3 sends 36 back to x.",
        flow("Read backward from the scalar loss",["L = y², y = 6","Sensitivity to y = 2y = 12","y changes 3× as fast as x","Sensitivity to x = 12 × 3"]))
    add("chain-2 chain-3","Two routes contribute to one gradient",
        "At x=2, y=x² changes at rate 4. The y and 3y branches contribute 4 and 12 to the final sum. Add both paths.",
        bars("Contribution to dL/dx",["y path","3y path","Total"],[4,12,16],"Derivative"))
    eps=np.logspace(-8,-1,100)
    add("chain-4","A finite-difference step can be too small",
        "Centered differences lose precision when nearby evaluations round to the same value. Here float32 resolves sin near 1 over only part of the step sweep.",
        lines("Measured error for sin′(1), float32",np.log10(eps),[("error",np.abs((np.sin(np.float32(1)+eps.astype("f"))-np.sin(np.float32(1)-eps.astype("f")))/(2*eps)-np.cos(1)))],"log₁₀(step)","Absolute error"))
    add("curvature-1 curvature-4","Curvature measures how the slope changes",
        "For L=x² the gradient rises from 0 to 2 over one unit. A Hessian–vector product reports this change in gradient per unit step along the chosen direction.",
        lines("One-dimensional slice",t,[("loss",t*t),("gradient",2*t)],"x","Value"))
    add("curvature-2","A step can shrink or amplify the error",
        "For curvature 2, each error is multiplied by 1−2η. Alternating signs can still converge if the magnitude shrinks.",
        lines("Iterates starting at x=1",range(7),[(str(lr), (1-2*lr)**np.arange(7)) for lr in (.25,.75,1.1)],"Update","x"))
    add("info-1 info-2 klcontrol-1","Average surprise under the data distribution",
        "For a fair source, average the two model surprises equally. Predicting 0.8 and 0.2 costs 1.322 bits on average, above the source entropy of 1 bit.",
        bars("Surprise under q",["Outcome A","Outcome B"],-np.log2([.8,.2]),"Bits"))
    add("info-3 info-4 klcontrol-2","Missing probability mass makes direction matter",
        "Outcome B occurs under q but is impossible under p. A draw from q can therefore face infinite surprise under p. Drawing from p never encounters B.",
        bars("Distribution p",["A","B"],[1,0],"Probability"),
        bars("Distribution q",["A","B"],[.5,.5],"Probability"))
    add("klcontrol-3 klcontrol-4","A sampled log ratio can be negative",
        "With p=(0.8,0.2) and q=(0.5,0.5), drawing only B gives a negative estimate. The probability-weighted sum across both outcomes is positive.",
        bars("Per-outcome log ratio",["A","B"],np.log([1.6,.4]),"Nats"),
        bars("Contributions weighted by p",["A","B"],np.array([.8,.2])*np.log([1.6,.4]),"Nats"))
    add("stable-1 stable-atom7","A shared logit shift preserves the odds",
        "Removing the maximum turns [2,3] into [−1,0]. The relative gap stays one. The largest exponential becomes exactly one.",
        bars("Before subtracting max",["A","B"],[2,3],"Logit"),
        bars("After subtracting max",["A","B"],[-1,0],"Logit"))
    add("stable-2 stable-editor","Equal logits split probability equally",
        "Two identical logits both shift to zero. Their exponentials sum to two. Each class gets probability one-half, whatever the original common offset.",
        flow("Equal logits with a huge common value",["[1000, 1000]","Subtract the max → [0, 0]","exp → [1, 1]","Normalize → [½, ½]"]))
    add("stable-3 stable-atom6","Keep tiny probabilities in log space",
        "Log probability preserves a finite gap of about 2,000. Exponentiating that gap can round to zero before taking a logarithm.",
        bars("Two classes after log-softmax",["Leading class","Rare class"],[0,-2000],"Approx. log probability"))
    add("stable-4","Masking every key leaves an empty row",
        "A masked-out entry contributes no probability. With no allowed key, the row has zero total weight before normalization. Define an explicit empty-row policy.",
        matrix("1 = allowed; 0 = excluded",[[1,0,0],[1,1,0],[0,0,0]],"Key","Query"))
    add("likelihood-1","Large residuals cost disproportionately more",
        "For Gaussian errors at a fixed variance, doubling the residual quadruples its squared penalty. The likelihood and least-squares optima coincide.",
        lines("Gaussian negative log likelihood up to a constant",t,[("cost",t*t/2)],"Residual, in standard deviations","Cost (nats)"))
    add("likelihood-2 mlegrad-3","An improbable observation costs more",
        "A probability of 0.25 costs about 1.386 nats. As the reported probability approaches zero, the penalty grows without bound.",
        lines("Negative log likelihood of the target",p,[("NLL",-np.log(p))],"Assigned probability","Nats"))
    add("likelihood-3 likelihood-4","Variance must pay for its own width",
        "With residual 1, increasing variance lowers the scaled residual penalty. The log-variance term eventually raises the total, preventing unlimited inflation.",
        lines("Gaussian NLL, constant omitted",np.linspace(.2,5,100),[(label,fn(np.linspace(.2,5,100))) for label,fn in [("Residual",lambda v:.5/v),("Total",lambda v:.5/v+.5*np.log(v))]],"Predicted variance","Cost (nats)"))
    add("estimation-1","Refitting the model moves its prediction",
        "At one fixed input, the fits predict 2, 5 and 3. Variation across training sets contributes predictive variance.",
        bars("Prediction at the same input",["Fit A","Fit B","Fit C"],[2,5,3],"Prediction"))
    add("estimation-2 estimation-3","Read training and held-out curves together",
        "A wide gap that closes with more data suggests variance. When both errors remain high and close, inspect model capacity and optimization.",
        lines("Example with a closing gap",[25,50,100,200],[("Training",[.05,.08,.10,.11]),("Held-out",[.37,.26,.19,.15])],"Training examples","Error"),
        lines("Example with underfitting",[25,50,100,200],[("Training",[.30,.31,.31,.31]),("Held-out",[.34,.33,.32,.32])],"Training examples","Error"))
    add("estimation-4","Tune first and evaluate on fresh data",
        "Choosing the best parameter on a split uses its outcomes. Reserve a separate test split for the final estimate.",
        flow("How labels may be used",["Training labels → fit weights","Validation labels → choose penalty","Test labels → final estimate"]))
    add("montecarlo-1 montecarlo-3 montecarlo-4","Rare draws may carry most of the estimate",
        "If a region has target probability 0.50 but proposal probability 0.01, its weight is 50. Capping the weight reduces variability and changes the expected contribution.",
        bars("Probability of the rare region",["Target p","Proposal q"],[.5,.01],"Probability"))
    add("montecarlo-2","Count how concentrated the weights are",
        "Only two samples carry weight. The reciprocal sum of squared normalized weights is 1/(0.25+0.25)=2.",
        bars("Normalized importance weights",list("ABCD"),[.5,.5,0,0],"Weight"))
    add("bayes-1 bayes-2 bayes-4","A posterior has a location and a width",
        "A Beta(2,3) prior and three successes plus one failure yield Beta(5,4). Its mean is 5/9. A single highest point discards the spread.",
        lines("Bernoulli success probability",p,[("Prior",12*p*(1-p)**2),("Posterior",280*p**4*(1-p)**3)],"Success probability","Density"))
    add("bayes-3","Two future successes share an uncertain rate",
        "Given p, the chance of two successes is p². For a Beta(2,2) posterior, averaging p² gives 0.30. Plugging in its mode p=½ gives 0.25.",
        bars("Probability of two successes",["At mode","Posterior average"],[.25,.30],"Probability"))
    add("gradsoftmax-1 gradsoftmax-2 gradsoftmax-3","Subtract the target distribution",
        "Predicted [0.1,0.7,0.2] minus target [0,0,1] gives [0.1,0.7,−0.8]. Raising the correct logit and lowering the others reduces loss.",
        bars("Logit gradient",list("ABC"),[.1,.7,-.8],"p − target"))
    add("gradsoftmax-4","Normalizing probabilities again changes them",
        "Softmax expects scores. Feeding it probabilities [0.9,0.1] treats their difference as a logit gap of only 0.8 and weakens the prediction.",
        bars("Original probabilities",["A","B"],[.9,.1],"Probability"),
        bars("After another softmax",["A","B"],np.exp([.9,.1])/sum(np.exp([.9,.1])),"Probability"))
    add("statistics-1","Power is area beyond the rejection threshold",
        "Under the alternative, observations to the right of the cutoff lead to rejection. Their total probability is the test’s power.",
        ("Shaded area under the alternative", power_panel))
    add("changevar-1 changevar-3 changevar-4","The determinant measures area expansion",
        "A 2× horizontal and 3× vertical stretch multiplies area by 6. The same probability occupies six times the area, so density divides by 6.",
        transform("Track the unit square",[[2,0],[0,3]]))
    add("changevar-2","Stretching support spreads out probability",
        "Tripling interval width requires one-third the height. Both rectangles have area one.",
        lines("Uniform densities before and after scaling",[0,.999,1,2.999,3],[("X",[1,1,0,0,0]),("3X",[1/3,1/3,1/3,1/3,0])],"Value","Density"))
    add("onlinevar-1","Center first when a tiny spread rides on a large offset",
        "The deviations of [10000,10001,10002] from their mean are [−1,0,1]. Squaring these small values avoids subtracting two numbers near 100 million.",
        bars("After subtracting the mean",list("ABC"),[-1,0,1],"Deviation"))
    add("onlinevar-2 onlinevar-3 onlinevar-atom6","Spread is the sum of squared distances",
        "For [2,4,6] the mean is 4. Distances −2, 0 and 2 contribute 4, 0 and 4. The updated M2 is 8.",
        bars("Squared distance from the new mean",["x=2","x=4","x=6"],[4,0,4],"Contribution to M2"))
    add("onlinevar-4 onlinevar-atom7","Two tight groups can have a wide combined spread",
        "Each singleton has zero spread. After merging 0 and 4, the mean is 2. Each point contributes 4 to M2.",
        scatter("The merged observations",[("Observations",[0,4],[0,0]),("Mean",[2],[0])],"Observed value",""))
    add("onlinevar-editor","A larger shard carries more weight",
        "Two examples at 10 and eight at 0 total 20 across ten examples. The combined mean is 2, closer to the larger shard.",
        bars("Number of observations",["Value 10","Value 0"],[2,8],"Count"))
    add("mlegrad-1 mlegrad-2","The likelihood peaks at the observed fraction",
        "For three successes and a failure the likelihood is p³(1−p). Logging converts products into sums and preserves the maximum at p=0.75.",
        lines("Likelihood of the observed sequence",p,[("likelihood",p**3*(1-p))],"Success probability p","Likelihood"))
    add("mlegrad-4","Score contributions cancel in expectation",
        "For Bernoulli p=0.25, success contributes 0.25×4=1 and failure contributes 0.75×(−4/3)=−1. The weighted sum is zero.",
        bars("Probability × score",["Success","Failure"],[1,-1],"Contribution"))
    add("optconstraints-1 optconstraints-2 optconstraints-3","A binding boundary changes the best reachable point",
        "The unconstrained loss is lowest at 3. With x≤1 the optimum is at 1, where loosening the boundary reduces loss. A slack constraint has zero multiplier.",
        lines("Full loss and feasible portion",np.linspace(-1,4,101),[("Full",(np.linspace(-1,4,101)-3)**2),("Feasible",np.where(np.linspace(-1,4,101)<=1,(np.linspace(-1,4,101)-3)**2,np.nan))],"x","Loss"))
    add("optconstraints-4","Track feasibility beside the objective",
        "A falling loss can coexist with repeated positive constraint residuals. Positive residual here means the learner exceeded its budget.",
        lines("Illustrative optimization trace",range(6),[("Loss",[1,.8,.65,.58,.5,.4]),("Residual",[-.2,.4,-.18,.3,-.15,.27])],"Update","Value"))
    add("hessdiag-1 hessdiag-2 hessdiag-3","Rescaling axes can undo unequal curvature",
        "For loss ½(x²+100y²), the gradient at (1,1) is (1,100). Multiplication by diag(1,0.01) changes it to (1,1), exactly the offset from the minimum.",
        matrix("Curvature by axis",[[1,0],[0,100]]),
        matrix("Inverse curvature",[[1,0],[0,.01]]))
    add("hessdiag-4","An indefinite Hessian bends both ways",
        "For L=(x²−y²)/2 the y curvature is negative. Newton can step toward the stationary saddle even when doing so increases loss.",
        lines("Two coordinate slices",t,[("x slice",.5*t*t),("y slice",-.5*t*t)],"Distance from origin","Loss"))
    add("jacobian-1 jacobian-2 jacobian-3 jacobian-4","One score changes both probabilities",
        "At p=(¼,¾), each off-diagonal derivative is −3/16. With upstream weights (2,0), the vector–Jacobian product is (0.375,−0.375).",
        matrix("Rows: output probability; columns: input logit",[[.1875,-.1875],[-.1875,.1875]],"Logit","Probability"))
