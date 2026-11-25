"""Worked examples for prediction, representation learning and model architecture."""
import numpy as np
from visual_examples import add, arrows, bars, flow, lines, matrix, scatter, transform


def register():
    t=np.linspace(-4,4,101)
    probs=np.linspace(.01,.99,99)
    sigmoid=lambda x: 1/(1+np.exp(-x))
    add("linear-1 linear-2 linear-3 linear-4","Penalties reshape coefficients",
        "With orthonormal inputs and squared error, ridge with λ=1 halves each coefficient. Lasso soft-thresholding instead sets sufficiently small coefficients exactly to zero.",
        bars("Least squares",["A","B","C"],[2,.4,-1],"Weight"),
        bars("Ridge",["A","B","C"],[1,.2,-.5],"Weight"))
    add("classification-1 classification-2","Log odds map the real line to probability",
        "A score of zero means even odds. At predicted probability 0.8 and target one, the gradient is −0.2, so gradient descent raises the score.",
        lines("Binary logistic link",t,[("p",sigmoid(t))],"Log odds","Positive-class probability"))
    add("classification-3","Compare the cost of each decision",
        "A negative prediction costs 9p in expectation and a positive costs 1−p. The two are equal at p=0.1.",
        lines("Correct decisions cost zero",probs,[("Predict negative",9*probs),("Predict positive",1-probs)],"Probability of positive","Expected cost"))
    add("classification-4 metricrep-1","A single line cannot separate XOR",
        "Opposite corners have the same label. Every straight boundary leaves at least one point on the wrong side. A probe only detects linearly accessible structure.",
        scatter("Feature space",[("A",[0,1],[0,1]),("B",[0,1],[1,0])],"Feature 1","Feature 2"))
    add("trees-1 trees-2 boost-1 boost-2","Correct a prediction in stages",
        "At target 5 and prediction 3, the residual is +2. Squared-error boosting fits this remaining gap. Forests instead average independently varied trees.",
        bars("One training case",["Target","Current fit","Residual"],[5,3,2],"Response"))
    add("boost-3 boost-4 regularize-4","Track the cost of fitting ever finer detail",
        "In this illustrative run, training error keeps falling after held-out error turns upward. Choosing the earlier round limits how closely the ensemble fits noise.",
        lines("An illustrative boosting run",[1,5,10,20,40],[("Training",[.5,.32,.20,.11,.03]),("Validation",[.52,.38,.30,.32,.42])],"Rounds","Error"))
    add("kernel-1 kernel-2 kernel-4","A Gram matrix compares every pair",
        "For points 0, 1 and 2, the RBF entry one unit from the diagonal is exp(−1). Adding a new point requires a new row and column.",
        matrix("RBF similarities, γ=1",np.exp(-(np.arange(3)[:,None]-np.arange(3))**2),"Point j","Point i"))
    add("pca-1","Find the longest direction in the cloud",
        "The points spread mostly along the rising diagonal. Projecting there preserves more variation than projecting across it.",
        scatter("Centered samples",[("Samples",[-2,-1.6,-.7,-.3,.3,.7,1.6,2],[-1.9,-1.3,-.9,-.1,.1,.9,1.3,1.9])],"Feature 1","Feature 2"))
    add("pca-2","Principal components divide up the variance",
        "The covariance eigenvalues add to 10. Keeping components 1 and 2 keeps 9/10 of the variation.",
        bars("Variance along each principal axis",["PC1","PC2","PC3"],[6,3,1],"Variance"))
    add("pca-3 missing-1","Fit preprocessing inside each training fold",
        "The projection axes and means are fitted parameters. Validation labels may guide a choice, but validation features must not change the fitted transforms being evaluated.",
        flow("One held-out fold",["Fit means and axes on training rows","Apply that frozen map to validation rows","Evaluate the resulting predictions"]))
    add("clustering-1 clustering-2 clustering-4","Moving a center changes its squared-error bill",
        "For points 0, 2 and 7 the sum of squared distances is smallest at their mean, 3. With several centers, assignments can change as centers move.",
        lines("Try possible locations for one center",np.arange(8),[("cost",sum((np.arange(8)-v)**2 for v in [0,2,7]))],"Center location","Sum of squared distances"))
    add("clustering-3","Units can dominate a distance",
        "A change of 100 on one axis overwhelms a change of 1 on another in raw Euclidean distance. Scaling alters which differences count most.",
        bars("Two feature changes",["Distance (cm)","Time (s)"],[100,1],"Numeric change in own units"))
    add("imbalance-1 imbalance-3 roc-2","Sort cases by truth and prediction",
        "Rows are actual classes. Of 10,000 cases, 80 true positives and 99 false positives were flagged. Precision uses the flagged column, giving 80/179.",
        matrix("Columns 0 and 1 = predicted negative and positive",[[9801,99],[20,80]],"Prediction","Actual"))
    add("imbalance-4 rankmetrics-1 rankmetrics-2 rankmetrics-3","Rank changes the value of a hit",
        "When the only useful result is fourth, its reciprocal rank is ¼. A budget of three reviews misses it entirely even if recall at ten is perfect.",
        bars("Relevance by rank",["1","2","3","4","5"],[0,0,0,1,0],"Relevant"))
    add("calibration-1 calibration-2 distillation-1","Temperature changes confidence",
        "At higher temperature the winning class keeps its rank but probability spreads to the alternatives. A calibrated 0.8 forecast should succeed about eight times in ten.",
        bars("Logits [2, 1, 0], temperature 1",list("ABC"),np.exp([2,1,0])/sum(np.exp([2,1,0])),"Probability"),
        bars("Same logits, temperature 2",list("ABC"),np.exp([1,.5,0])/sum(np.exp([1,.5,0])),"Probability"))
    add("shift-1 shift-2 shift-4","Separate input mix from the label rule",
        "If group B grows from 20% of training to 60% in deployment, its covariate-shift weight is 3. This correction assumes the outcome rule within B stays the same.",
        bars("Group B share",["Training","Deployment"],[.2,.6],"Fraction"))
    add("retrieval-1 retrieval-2 retrieval-3 retrieval-4","Measure what survives candidate generation",
        "If eight of the exact top ten survive approximation, recall is 0.8. A reranker only sees the candidate pool and cannot restore the other two.",
        bars("Reference top ten",["Retrieved","Missing"],[8,2],"Items"))
    add("experiments-2 experiments-3","The denominator determines the lift",
        "A move from 10 to 11 conversions per hundred is one percentage point. Relative to the original ten conversions it is a 10% increase.",
        bars("Conversions per 100",["Control","Treatment"],[10,11],"Conversions"))
    add("generative-1 generative-2 generative-3 generative-4","Combine prior weight and evidence",
        "Equal-variance Gaussian classes differ by their centers. Comparing their weighted densities yields a straight boundary in one dimension. Repeating dependent evidence can overstate confidence.",
        lines("Equal-prior class densities",t,[("A",np.exp(-.5*(t+1)**2)/2.507),("B",np.exp(-.5*(t-1)**2)/2.507)],"Feature","Density"))
    add("roc-1","AUC counts pairwise wins",
        "Scores 0.9 and 0.4 for positive items beat negative scores 0.8 and 0.3 in three of four pairs. With no ties, AUC is 0.75.",
        matrix("1 = positive outranks negative",[[1,1],[0,1]],"Negative item","Positive item"))
    add("em-1 em-2 em-3","Soft assignments split ownership of a point",
        "At equal priors, likelihoods 0.3 and 0.1 give responsibilities ¾ and ¼. Each component’s updated center uses its share as a weight.",
        bars("Normalized responsibility",["Component A","Component B"],[.75,.25],"Share"))
    add("em-4","A tiny variance can create a density spike",
        "Narrowing a Gaussian around one observation raises its peak while its total area remains one. Variance floors can prevent collapse.",
        lines("Same center, different standard deviations",t,[("σ=1",np.exp(-t*t/2)/2.507),("σ=0.25",np.exp(-t*t/.125)/(.25*2.507))],"Feature","Density"))
    add("multilabel-1 multilabel-2 multilabel-3","Two labels can both be present",
        "Independent predictions 0.8 and 0.5 need not sum to one. When both labels are positive their joint likelihood under this model is 0.4.",
        bars("Two sigmoid outputs",["Label A","Label B"],[.8,.5],"Probability"))
    add("robustloss-1 robustloss-2 robustloss-4","Changing the loss changes the best prediction",
        "For targets 0, 0 and 9, squared loss favors the mean, 3. Absolute loss favors the median, 0. Asymmetric penalties can move the optimum again.",
        lines("Mean loss over three examples",np.arange(10),[(name,fn(np.arange(10)[:,None]-[0,0,9]).mean(axis=1)) for name,fn in [("Squared",np.square),("Absolute",np.abs)]],"Constant prediction","Loss"))
    add("layers-1 layers-3 layers-4","A bend gives the network new shapes",
        "ReLU is flat to the left of zero, so a negative preactivation sends no gradient through that unit. Sigmoid slopes also become tiny far from zero.",
        lines("Two activation functions",t,[("ReLU",np.maximum(0,t)),("Sigmoid",sigmoid(t))],"Preactivation","Activation"))
    add("layers-2 embedding-2","Each input–output pair owns one weight",
        "A small 3-to-2 dense layer has six weights and two output biases. The same counting rule gives 256×128+128 for the larger example. An embedding table uses rows times width.",
        matrix("One row per input, one column per output",[[1,2],[3,4],[5,6]],"Output","Input"))
    add("init-1 init-2 init-4","Fan-in controls the scale of each weight",
        "Adding more independent incoming terms increases their combined variance. He initialization compensates with variance 2/fan-in, or standard deviation √(2/fan-in).",
        lines("He-normal initialization",[32,64,128,256,512],[("std",np.sqrt(2/np.array([32,64,128,256,512])))],"Fan-in","Weight std"))
    add("sgd-1 sgd-2 sgd-3","A batch averages individual gradient estimates",
        "Four independent examples cut the standard deviation of a mean in half. At a fixed number of examples, larger batches also leave fewer updates.",
        bars("Scalar gradients in one batch",["1","2","3","4","Mean"],[-1,1,3,5,2],"Gradient"))
    add("sgd-4 adam-1 adam-2 adam-4 optlr-1 optlr-2 optlr-3","Recent gradients carry more weight",
        "With decay 0.9, an observation ten updates old has about 35% of the influence of a new one. Adam applies exponential averages to gradients and squared gradients.",
        lines("Relative weight by age",np.arange(21),[("β=.9",.9**np.arange(21))],"Age (updates)","Relative influence"))
    add("adam-3 adamw-1 adamw-2 adamw-3 adamw-4","Decoupled decay shrinks the weight directly",
        "At learning rate 0.01 and decay 0.1, the multiplier is 0.999 per step. From weight 10 the next value is 9.99 even when the optimizer direction is zero.",
        lines("Decay only",np.arange(11),[("weight",10*.999**np.arange(11))],"Step","Weight"))
    add("lr-1 lr-3","Clip length while preserving direction",
        "Reducing (3,4) to (1.2,1.6) multiplies both coordinates by 0.4. The arrow shortens along the same ray.",
        arrows("Same direction before and after clipping",[("Before",(0,0),(3,4)),("After",(0,0),(1.2,1.6))]))
    add("lr-4 optlr-4","Warmup changes the scale of early updates",
        "A schedule that restarts its ramp after a checkpoint gives a different next update even when the weights are identical.",
        lines("Example schedule",[0,1,2,3,4,5,6],[("LR",[0,.001,.002,.003,.003,.002,.001])],"Update","Learning rate"))
    add("norm-1 norm-2 rms-1 rms-2 rms-3","Normalize the feature row of one token",
        "LayerNorm centers [1,3] at mean 2 and scales to [−1,1]. RMSNorm rescales without subtracting the mean, so a shared offset affects the result.",
        matrix("Two tokens, two features",[[1,3],[5,7]],"Feature","Token"),
        matrix("Each row after LayerNorm (ε=0)",[[-1,1],[-1,1]],"Feature","Token"))
    add("norm-3 bn-1 bn-2 bn-3 bn-4","A batch boundary changes the statistics",
        "Separate batches [0,2] and [8,10] have means 1 and 9. Normalizing once over both uses mean 5. Accumulating gradients does not merge these forward statistics.",
        matrix("Samples within one channel",[[0,2],[8,10]],"Observation","Batch"))
    add("norm-4 blocks-3","The residual connection carries the input directly",
        "For x=2 and F(x)=3x, the output is 2+6. Backward sensitivity contains a direct 1 from the bypass in addition to 3 through the branch.",
        bars("Two paths to the output",["Bypass","Branch","Sum"],[2,6,8],"Value"))
    add("regularize-1 regularize-2 regularize-3","Dropout preserves the expected activation",
        "A value of 3 survives as 4 with probability ¾ and becomes 0 with probability ¼. Its average is still 3.",
        bars("Possible training activations",["Dropped","Retained","Mean"],[0,4,3],"Activation"))
    add("conv-1 conv-2 conv-3 conv-4","Slide one kernel along the input",
        "Each row shows one width-three window on ten positions. Stride two gives four valid outputs. A one-position shift changes which input groups get sampled.",
        matrix("Shaded cells contribute to that output",[[int(2*r<=c<2*r+3) for c in range(10)] for r in range(4)],"Input index","Output index"))
    add("sequence-1 sequence-2 sequence-3 sequence-4","Repeated multiplication fades distant gradients",
        "A local derivative of 0.9 repeated 50 times leaves about 0.005 of the initial signal. A gated path near one can preserve it longer.",
        lines("Fraction of sensitivity remaining",np.arange(51),[("0.9 per step",.9**np.arange(51)),("0.99 per step",.99**np.arange(51))],"Steps apart","Relative sensitivity"))
    add("contrast-4 retrievalgrad-2","A contrastive loss is a classification loss",
        "With logits [ln 2,0,0], exponentiating gives weights [2,1,1]. The positive has probability ½ and loss ln 2. Four equal candidates give loss ln 4.",
        bars("Normalized candidate probabilities",["Positive","Other 1","Other 2"],[.5,.25,.25],"Probability"))
    add("latent-1 latent-3 latent-4","The ELBO balances fit and a distribution penalty",
        "An improvement of 2 nats in expected log likelihood is outweighed by an increase of 3 nats in KL. The lower bound drops by one nat.",
        bars("Change in the lower bound",["Better fit","KL cost","Net"],[2,-3,-1],"Nats"))
    add("latent-2","Move and stretch a reusable noise sample",
        "For μ=2 and σ=3, noise values −1, 0 and 1 map to −1, 2 and 5. Gradients can flow through this location-scale transformation.",
        lines("z = μ + σε",[-1,0,1],[("z",[-1,2,5])],"Standard noise ε","Latent z"))
    add("transfer-1 transfer-2 transfer-3 transfer-4 latentkv-1","Route a vector through a low-rank bottleneck",
        "Two thin maps communicate through r middle coordinates. For a LoRA update of a square 4096-wide layer with rank 8, they store 2×4096×8 trainable weights.",
        flow("LoRA update path",["4096 input features","Project to 8 coordinates","Expand to 4096 output features","Add update to frozen layer output"]))
    add("metricrep-3","A readable direction need not drive behavior",
        "Removing the horizontal component erases that coordinate. A predictor using only the vertical component still returns the same result.",
        arrows("Original and ablated representation",[("Original",(0,0),(3,2)),("After ablation",(0,0),(0,2))]))
    add("embedding-1 embedding-3 embedding-4","A one-hot vector selects a row",
        "Multiplying [0,1,0] by this table gives [4,5]. When the table is reused for output scoring, gradients can also arrive from its role in predicting tokens.",
        matrix("One embedding per vocabulary item",[[2,1],[4,5],[0,3]],"Feature","Token ID"))
    add("forwardad-1 forwardad-2 forwardad-3 forwardad-atom5","Differentiate along one chosen direction",
        "Along (2+t,3−t), the product is 6+t−t². The slope at t=0 is 1. Perturb both coordinates together to check the directional derivative.",
        lines("Product along the chosen line",np.linspace(-.6,.6,61),[("product",6+np.linspace(-.6,.6,61)-np.linspace(-.6,.6,61)**2)],"Step t","f(x+tv)"))
    add("forwardad-4","Check whether a local slope exists",
        "At the ReLU kink the left slope is 0 and the right slope is 1. A centered secant gives ½; autodiff may choose a different subgradient there.",
        lines("Zoom in near zero",[-1,0,1],[("ReLU",[0,0,1])],"Input","Activation"))
    add("nonconvex-4","Compare update size to parameter size",
        "The same absolute update can be tiny in one layer and huge in another. Divide by the corresponding parameter norm before comparing.",
        bars("Example update-to-weight ratios",["Layer A","Layer B"],[.01,.5],"Norm ratio"))
    add("retrievalgrad-1 retrievalgrad-3 multimodal-1 multimodal-2 multimodal-3","Paired examples lie on a score-matrix diagonal",
        "Every query compares with every candidate. For n aligned pairs, n diagonal scores are matches and n(n−1) off-diagonal scores are potential negatives.",
        matrix("Example similarity scores",[[3,1,0],[0,4,1],[1,0,3]],"Candidate","Query"))
    add("attention-1 attention-editor attnback-atom5","Attention takes a weighted mixture of values",
        "With two equally weighted allowed keys, scalar values 3 and 9 contribute 1.5 and 4.5. The result is 6. With one allowed key its value passes through unchanged.",
        bars("Contributions to the output",["Key A","Key B","Sum"],[1.5,4.5,6],"Weighted value"))
    add("attention-2","Dot-product scale grows with key width",
        "Independent centered unit-variance coordinate products contribute variances that add. The raw score’s standard deviation grows as √d; dividing by √d stabilizes it.",
        lines("Before and after scaling",[1,4,16,64],[("Raw std",[1,2,4,8]),("Scaled std",[1,1,1,1])],"Key width","Score std"))
    add("attention-3 attention-atom7 cross-1 cross-2 cross-atom5 attnback-4","Follow the two rectangular products",
        "Three queries and five keys give a 3×5 weight matrix. Multiplying by five 2-D value vectors yields one 2-D output per query. The key width is summed out earlier.",
        flow("One attention head",["Q: 3 × d and Kᵀ: d × 5","QKᵀ → 3 × 5 scores","Softmax across the 5 keys","(3 × 5) × (5 × 2) → 3 × 2"]))
    add("attention-atom6 masked-2","A mask chooses entries before normalization",
        "A causal row can read its own and earlier positions. Set excluded logits to −∞ before softmax so allowed entries receive all of the row’s weight.",
        matrix("Causal access: 1 means allowed",np.tri(4),"Key position","Query position"))
    add("heads-1 heads-2 heads-3 heads-4 latentkv-2","Several query heads can share a key/value head",
        "Here four query heads read two KV heads. Conventional multi-head attention would store four; multi-query attention would store one.",
        matrix("Mapping of queries to KV heads",[[1,0],[1,0],[0,1],[0,1]],"KV head","Query head"))
    add("position-1 position-3","Position rotates a pair of feature coordinates",
        "Rotating (1,0) by a quarter-turn gives (0,1) without changing its length. Resetting a cached key or query position changes the relative angle.",
        arrows("A 90-degree positional rotation",[("Before",(0,0),(1,0)),("After",(0,0),(0,1))]))
    add("blocks-1 blocks-2 gatedmlp-1 gatedmlp-2 gatedmlp-3 gatedmlp-4","Width determines the parameter bill",
        "Two d→4d→d maps store 8d² weights. A gated block with two input branches and one output projection stores 3dh. Matching budgets gives h≈8d/3.",
        bars("Example at d=3, h=8",["Plain input","Plain output","Gated total"],[36,36,72],"Weights"))
    add("experts-1 experts-2 experts-3 experts-4","Count routed assignments per expert",
        "Three tokens with two selections each produce six assignments. Totals per expert can differ sharply even with fixed per-token compute.",
        matrix("1 = routed to this expert",[[1,1,0],[1,0,1],[1,1,0]],"Expert","Token"))
    add("ssm-3","Group adjacent transitions in a scan",
        "For four ordered updates, the first pair and last pair can compose independently. Composing the two results preserves the original order. A prefix scan can reuse such partial results.",
        flow("Example updates on x",["T₁: +1, T₂: ×2, T₃: +3, T₄: ×4","Pair 1 maps x to 2x+2","Pair 2 maps y to 4y+12","Compose pairs → 8x+20"]))
    add("ssm-1 ssm-2","A recurrent state has a fixed width",
        "A four-coordinate state is updated in place each step. A cache storing four coordinates per token grows linearly with the prefix instead.",
        lines("Example persistent state",[1,2,3,4],[("Recurrence",[4]*4),("Cache",[4,8,12,16])],"Tokens","Stored scalars"))
    add("vision-1 vision-2 vision-3 vision-4 masklearn-1 masklearn-2","Turn patches into positions",
        "A 4×4 patch grid gives 16 tokens. Hiding three quarters leaves four visible. Halving patch side at fixed image size gives four times the tokens and sixteen times the dense score entries.",
        matrix("Toy patch indices",np.arange(16).reshape(4,4),"Patch column","Patch row"))
    add("diffusion-2 diffusion-4 diffobject-1 diffobject-2 diffobject-3 diffobject-4","Signal and noise split the power budget",
        "At ᾱ=0.8 the signal and noise coefficients are √0.8 and √0.2. Their powers are 0.8 and 0.2 for standardized independent inputs, giving SNR 4.",
        bars("Power contributions",["Signal","Noise"],[.8,.2],"Power"))
    add("flow-1 flow-2 flow-3 flow-4","A velocity points along the transport path",
        "Moving from (1,1) to (4,3) in one unit of time on a straight path gives constant velocity (3,2). A varying learned field requires integration along the path.",
        arrows("Displacement from the starting sample",[("Start to finish",(1,1),(4,3)),("Same velocity at origin",(0,0),(3,2))]))
    add("tokenizer-2 tokenizer-4","Token counts change the loss denominator",
        "The same 300 nats over 100 tokens gives 3 nats/token. Spread over 150 tokens it gives 2. Comparing token losses needs a common unit.",
        bars("Same text, different token counts",["100 tokens","150 tokens"],[3,2],"Nats/token"))
    add("relative-1 relative-2 relative-3 relative-4","Local mixing builds up over layers",
        "With one previous neighbor per layer, the oldest reachable token moves back one step per layer. A dense implementation may still allocate the entire matrix.",
        matrix("Causal mask, one step back",[[int(0<=i-j<=1) for j in range(5)] for i in range(5)],"Source token","Target token"))
    add("ctc-1 ctc-2 ctc-3","Several frame paths can spell the same text",
        "CTC merges adjacent repeats, then removes blanks. The blank between the two As preserves the second A. Transcript probability sums all compatible path probabilities.",
        flow("Collapse a single alignment",["A A blank A B B","Merge repeats → A blank A B","Remove blank → A A B"]))
    add("modalfusion-1","A connector changes each visual embedding",
        "In this example two image patches each supply three features. Applying the same learned projection to both gives two vectors of width four for the language model.",
        flow("Follow the patch and feature axes",["Vision encoder → 2 × 3","Learned projection: 3 × 4","Projected image tokens: 2 × 4","Text tokens also have width 4"]))
    add("modalfusion-3","Attention spans the combined token sequence",
        "Image and text positions form four score blocks. For 576 image and 424 text positions, a full head has (576+424)² = 1,000,000 entries.",
        matrix("Rows and columns split into image and text",[[576**2,576*424],[424*576,424**2]],"Key group","Query group"))
    add("attnback-1 attnback-2 attnback-3","A value receives gradients from every reader",
        "With weights [0.25,0.75] and upstream gradient 4, value gradients are [1,3]. With multiple queries, sum their contributions down each key column.",
        bars("Gradient sent to each value",["Value 1","Value 2"],[1,3],"Upstream × weight"))
