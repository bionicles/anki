"""Worked examples for inference, evaluation, algorithms and scaling decisions."""
from math import comb
import numpy as np
from visual_examples import add, arrows, bars, flow, lines, matrix, scatter, transform


def register():
    add("decode-1 decode-3 decode-4","Separate the first token from later intervals",
        "The first token arrives at 0.5 s. Token 101 arrives 100 intervals later. At 20 ms per interval, that gives 2.5 s overall.",
        lines("Cumulative arrival time",[1,26,51,76,101],[("Arrival",[.5,1,1.5,2,2.5])],"Token number","Seconds"))
    add("kv-1 kv-2 kv-3 kv-4 cachemath-2 cachemath-atom7","Cache memory grows with token count",
        "Two arrays (K and V) × 32 layers × 8 heads × 128 coordinates × 2 bytes gives 128 KiB per token. At 8,192 tokens that reaches 1 GiB.",
        lines("Fixed architecture",[0,2048,4096,8192],[("Payload",[0,256,512,1024])],"Cached tokens","MiB"))
    add("paging-1 paging-2 cachemath-1 cachemath-editor cachemath-atom6","Allocation jumps one page at a time",
        "Pages hold 16 tokens. Counts 31 and 32 need two pages; 33 needs three. The new page has 15 spare slots. Separate sequences can each have a partly filled page.",
        lines("Allocated slots for one sequence",[1,16,17,32,33,48],[("Allocated",[16,16,32,32,48,48]),("Used",[1,16,17,32,33,48])],"Used tokens","Slots"))
    add("batch-4 latency-3 benchmark-3","More time in the system means more live requests",
        "In steady state at 20 arrivals per second, a mean residence of 0.5 s implies 10 in flight. Sustained overload has no steady-state queue of this kind.",
        lines("Little’s law at 20 requests/s",[.1,.25,.5,1],[("In flight",[2,5,10,20])],"Mean residence (s)","Mean requests"))
    add("sampling-1 sampleexact-1 sampleexact-2 sampleexact-3","Remove excluded mass, then renormalize",
        "The retained probabilities sum to 0.8. Divide each by 0.8 to get [0.5,0.25,0.25]. A token outside the retained set gets no new mass.",
        bars("Before truncation",list("ABCD"),[.4,.2,.2,.2],"Probability"),
        bars("Retaining A, B and C",list("ABCD"),[.5,.25,.25,0],"Probability"))
    add("spec-1 spec-2 spec-3","Accept the mass shared by draft and target",
        "For A the draft assigns 0.4 and the target only 0.1. Accept one quarter of proposed As. Rejection correction samples from the positive target-minus-draft remainder.",
        matrix("Rows: draft and target",[[.4,.6],[.1,.9]],"Token A or B","Distribution"))
    add("quant-1 quant-2 weightquant-1 weightquant-2","Integer codes lie on a grid",
        "With scale 0.5 and zero point 2, codes 0 through 4 decode to −1 through +1. Larger ranges at the same bit width put the grid points farther apart. Two 4-bit codes fit in one byte.",
        lines("Decoded values",range(5),[("Value",[-1,-.5,0,.5,1])],"Integer code","Reconstructed value"))
    add("latency-1 latency-atom5","Look at the tail as well as the mean",
        "An observed p99 of 240 ms exceeds a 200 ms limit by 40 ms, or 20% of the limit. A fast median does not offset this breach.",
        bars("Tail latency",["Limit","Canary p99"],[200,240],"Milliseconds"))
    add("latency-2","An error budget is a fraction of a time window",
        "A 30-day month has 43,200 minutes. The allowed 0.1% unavailable share is 43.2 minutes.",
        lines("Budget at 99.9% availability",[1,7,14,30],[("Unavailable",[1.44,10.08,20.16,43.2])],"Days","Allowed minutes"))
    add("beam-1 beam-2","Expansion multiplies paths before pruning",
        "Each of four paths can extend by any of 50,000 tokens. Score 200,000 extensions, then keep four live paths. The simplified example uses three tokens per path.",
        matrix("Toy choices: one cell per extension",np.arange(1,13).reshape(4,3),"Next token","Live path"))
    add("toolbudget-1 toolbudget-2","Reserve time before assigning the remainder",
        "Subtract both 1.8 s already spent and 0.4 s reserved from a 3 s deadline. Tools can consume at most 0.8 s.",
        bars("Where the three seconds go",["Spent","Render","Tools"],[1.8,.4,.8],"Seconds"))
    add("prefillcache-1 prefillcache-2 prefillcache-3","Only repeated prefix work is saved",
        "The first request still computes the 2,000-token prefix. Across 100 requests perfect reuse avoids 99×2,000 = 198,000 prefix token evaluations.",
        lines("Prefix work under ideal reuse",[1,25,50,100],[("No cache",[2,50,100,200]),("Reuse",[2,2,2,2])],"Requests","Thousand token evaluations"))
    add("servesplit-2 servesplit-3 budgetdesign-1-part2","Transfer time divides bytes by bandwidth",
        "Moving 2 GiB over a 20 GiB/s link takes at least 0.1 s before latency, contention or overlap. Keep units consistent.",
        lines("Ideal transfer of 2 GiB",[5,10,20,40],[("Time",[.4,.2,.1,.05])],"Bandwidth (GiB/s)","Seconds"))
    add("paired-1 paired-2 paired-atom5","Keep both model results for each sampled item",
        "Only disagreements change the accuracy difference. On 1,000 items, 80 B-only wins minus 50 A-only wins gives +3 points. Resample paired items together.",
        bars("Outcomes that change the difference",["B only","A only","Net B wins"],[80,50,30],"Items"))
    add("passk-1 passk-2 passk-editor passk-atom6 passk-atom7","Count all-failing subsets",
        "With five candidates and two correct, three of ten possible pairs contain only failures. Pass@2 is 1−3/10. At k=4 there are too few failures to form an all-failing subset.",
        bars("Success probability by subset size",["k=1","k=2","k=3","k=4"],[1-(comb(3,k) if k<=3 else 0)/comb(5,k) for k in range(1,5)],"Pass@k"))
    add("agenteval-2","Repeated success multiplies probabilities",
        "All three independent trials must succeed, so the chance is 0.8³ = 0.512. This is a different event from at least one success.",
        lines("Probability all trials succeed",[1,2,3,4,5],[("All succeed",.8**np.arange(1,6))],"Trials","Probability"))
    add("safety-1 safety-2","Translate percentages back to counts",
        "In a slice of 100, four failures versus three means one fewer observed event. The counts help assess how much sampling noise matters.",
        bars("Same 100-item slice",["Before","After"],[4,3],"Failures"))
    add("uncertainty-1 uncertainty-2 uncertainty-3 uncertainty-4","Separate coverage from selective risk",
        "Of 1,000 requests, 800 were answered and 40 of those were wrong. Coverage uses 1,000 as denominator; selective risk uses 800.",
        bars("Breakdown of all requests",["Correct","Wrong","Abstained"],[760,40,200],"Requests"))
    add("uncertaintybench-1 uncertaintybench-2 uncertaintybench-3","Zero observed failures still permits a small rate",
        "Under independent representative trials, the approximate one-sided 95% upper bound is 3/n. At n=3,000 it is 0.1%.",
        lines("Rule of three",[300,600,1500,3000],[("Upper bound",[1,.5,.2,.1])],"Trials with zero failures","Upper rate (%)"))
    add("multilingual-1 multilingual-2 multilingual-4 construct-3","Two averaging rules answer different questions",
        "Accuracy is 90% in A and 10% in B. Equal language weighting gives 50%; pooling the 110 items gives 91/110 = 82.7%.",
        bars("Same results, different weights",["A","B","Macro","Micro"],[.9,.1,.5,91/110],"Accuracy"))
    add("features-1 features-2","Sparsity and reconstruction compete",
        "This illustrative curve shows lower error as more latent features activate. Score both reconstruction and active-feature count to compare operating points.",
        lines("Example autoencoder tradeoff",[1,2,4,8],[("Error",[.5,.32,.20,.14])],"Features active per input","Reconstruction error"))
    add("circuits-1 circuits-2","Attention weights gate value contributions",
        "A tiny value can contribute little even with high attention. For weights [0.9,0.1] and scalar values [0,10], the second item supplies the entire output.",
        matrix("Columns: weight, value, product",[[.9,0,0],[.1,10,1]],"Quantity","Item"))
    add("bootstrap-3 paired-4","Sample independent clusters",
        "Twenty answers sharing one prompt provide information about that prompt, with fewer independent prompt effects than twenty distinct prompts.",
        matrix("Each row repeats one underlying prompt",[[1]*5,[2]*5,[3]*5],"Repeated sample","Prompt"))
    add("streaming-1 streaming-2","Entry and survival odds cancel",
        "Item five enters the reservoir with probability 1/5. Its chance of surviving items six through ten is 5/10, leaving unconditional probability 1/10.",
        lines("Chance item 5 is still selected",range(5,11),[("Probability",1/np.arange(5,11))],"Items processed","Probability"))
    add("scans-1 scans-2","Lengths become buffer boundaries",
        "Lengths [3,0,2,4] give boundaries [0,3,3,5,9]. Equal consecutive boundaries encode an empty span.",
        lines("Position after each segment",range(5),[("Boundary",[0,3,3,5,9])],"Segments consumed","Offset"))
    add("complexity-3","An all-pairs array grows quadratically",
        "Doubling the number of items quadruples the number of cells. At 100,000 items, a dense float32 pair matrix uses 40 GB decimal.",
        lines("Four bytes per pair",[10,25,50,100],[("Payload",[.4,2.5,10,40])],"Thousand items","GB"))
    add("interviewgraph-1 interviewgraph-3 graphnets-1 graphnets-2 graphnets-4","Neighborhoods expand one hop per layer",
        "On a chain A–B–C–D, starting from A reaches B in one hop and C in two. BFS examines adjacency entries; graph aggregation pools reachable neighbors’ messages.",
        matrix("Undirected adjacency: 1 means an edge",[[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]],"Destination A–D","Source A–D"))
    add("heapstream-1 heapstream-2 heapstream-3","Retain only the best k values",
        "With k=3, the smallest retained value is the cutoff. Replacing it when a higher value arrives costs logarithmic heap work while storage stays at three values.",
        flow("Stream 2, 8, 4, 7; k=3",["Retain 2, 4, 8","Incoming 7 beats minimum 2","Retain 4, 7, 8"]))
    add("lrucache-1 lrucache-2 lrucache-3","A hit changes the eviction order",
        "In a two-slot cache the second access to A makes B oldest. C then evicts B. The lists run from least recent to most recent.",
        flow("Requests A, B, A, C",["[A]","[A, B]","[B, A]","[A, C]"]))
    add("twopointers-1 twopointers-2 twopointers-3","Slide the boundary past a repeated token",
        "For A B B A, the second B forces the left boundary past the first B. The longest duplicate-free windows AB and BA both have length two.",
        flow("Current valid window",["A","A B","B","B A"]))
    add("binary-1 binary-2 binary-3","Search for the first true predicate",
        "In [1,2,2,4], values at positions 1, 2 and 3 satisfy x≥2. Lower bound locates the transition, at index 1.",
        matrix("Top row: values; bottom row: x ≥ 2",[[1,2,2,4],[0,1,1,1]],"Index",""))
    add("tensor-1 tensor-3 tensor-4","Transpose changes how storage is read",
        "The physical order can stay [0,1,2,3,4,5]. A transposed view walks that memory with different strides. Writing a shared cell changes the original too.",
        matrix("Original indices",[[0,1,2],[3,4,5]]),
        matrix("Indices as seen through the transpose",[[0,3],[1,4],[2,5]]))
    add("tensor-2","Broadcasting can pair every example with every target",
        "Column predictions [1,3] minus row targets [1,2] form all four pairwise differences. For a per-example residual, align the shapes first.",
        matrix("Pairwise subtraction",[[0,-1],[2,1]],"Target","Prediction"))
    add("cfg-1 cfg-2","Guidance extends a conditional difference",
        "Start at 0.2. The conditional prediction is 0.3 farther along. Applying scale 2 reaches 0.2+2×0.3=0.8.",
        lines("Guided prediction by scale",[0,1,2,3],[("Prediction",[.2,.5,.8,1.1])],"Guidance scale","Predicted noise"))
    add("capstone-2 report-2","Compare gain per unit of budget",
        "Plan A gives 0.4/400=0.001 points per GPU-hour. Plan B gives 0.2/100=0.002, twice the gain per unit.",
        bars("Expected gain per 100 GPU-hours",["A","B"],[.1,.2],"Metric points"))
    add("launch-2 launch-atom8 scalingbreak-1 scalingbreak-2","Savings accumulate across requests",
        "At $0.003 saved per request, 100 million requests repay $300,000 extra training cost. The slope is the per-request saving.",
        lines("Cumulative cost comparison",[0,50,100,150],[("Saved",[0,150,300,450]),("Up-front",[300]*4)],"Million requests","Thousand dollars"))
    add("weaksupervision-1 weaksupervision-2 weaksupervision-3","Measure the recovered part of a gap",
        "The student gains 0.1 over the weak model. The fully supervised baseline is 0.2 ahead of the weak model, so the recovered fraction is one-half.",
        bars("Score by supervision",["Weak","Student","Full"],[.6,.7,.8],"Score"))
    add("audio-4","Count edits against the reference length",
        "Five substitutions plus two deletions plus three insertions make ten errors. Divide by the 100 reference words to obtain 10% WER.",
        bars("Edits aligning reference to transcript",["Substitute","Delete","Insert"],[5,2,3],"Word edits"))
    add("orthopt-1 orthopt-2","Equalize the stretches of a matrix update",
        "In this ideal diagonal example, both nonzero singular values become one. Muon approximates an orthogonalizing transform of a matrix-shaped update.",
        transform("Before: unequal stretches",[[3,0],[0,.5]]),transform("Ideal orthogonal factor",[[1,0],[0,1]]))
    add("peftmerge-1 peftmerge-2 peftmerge-3","Equivalent functions can order hidden units differently",
        "Both models can represent the same two features in opposite row order. Averaging their weights row by row collapses these two directions into identical rows.",
        matrix("Model A",[[1,0],[0,1]]),matrix("Mean after swapping A’s two rows in model B",[[.5,.5],[.5,.5]]))
    add("privacy-1 privacy-2","Clip each example before aggregation",
        "With clip bound 2, gradients +10 and −1 become +2 and −1, summing to +1. Clipping the raw sum +9 gives +2 instead and does not enforce the per-example bound.",
        bars("Scalar gradients before averaging",["Clipped 1","Clipped 2","Sum"],[2,-1,1],"Gradient"))
