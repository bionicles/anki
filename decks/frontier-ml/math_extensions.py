"""Additional worked examples for statistical, sequential and systems concepts."""
import numpy as np
from visual_examples import add, bars, flow, lines, matrix, arrows, scatter


def network(title, nodes, edges):
    """Render a small directed graph. Coordinates are chosen to fit node labels."""
    def draw(ax):
        ax.axis("off")
        ax.set(xlim=(-.18,1.18),ylim=(-.16,1.16))
        for start,end in edges:
            ax.annotate("",nodes[end],nodes[start],arrowprops={"arrowstyle":"->","shrinkA":17,"shrinkB":17,"color":"#526c76","lw":1.7})
        for label,(x,y) in nodes.items():
            ax.text(x,y,label,ha="center",va="center",fontsize=11,
                    bbox=dict(boxstyle="round,pad=.32",fc="#e7f3f6",ec="#176487"))
    return title,draw


def spectrogram():
    def draw(ax):
        sr=8000
        samples=np.arange(sr)/sr
        hz=300+1200*samples
        signal=np.sin(2*np.pi*np.cumsum(hz)/sr)
        # Original synthetic chirp; overlapping Hann windows and triangular mel filters.
        width=256
        windows=np.lib.stride_tricks.sliding_window_view(signal,width)[::64]
        energy=np.abs(np.fft.rfft(windows*np.hanning(width),axis=1))**2
        freqs=np.fft.rfftfreq(width,d=1/sr)
        mel_max=2595*np.log10(1+(sr/2)/700)
        edges=700*(10**(np.linspace(0,mel_max,34)/2595)-1)
        filters=np.array([np.maximum(0,np.minimum((freqs-a)/(b-a),(c-freqs)/(c-b)))
                          for a,b,c in zip(edges,edges[1:],edges[2:])])
        power=energy@filters.T
        db=10*np.log10(np.maximum(power,1e-12)/power.max())
        ax.imshow(db.T,origin="lower",aspect="auto",extent=(0,1,-.5,31.5),cmap="magma",vmin=-55,vmax=0)
        ax.set(xlabel="Time (seconds)",ylabel="Mel filter index")
    return "A rising synthetic tone, time →",draw


def equivalence_panel(ax):
    ax.axvspan(-.02, .02, alpha=.22, color="#23877a", label="Equivalence region")
    ax.axvline(0, color="gray", linestyle=":")
    ax.plot([-.035,.05], [1,1], "o-", color="#176487", label="95% interval")
    ax.set(xlim=(-.05,.06), ylim=(.9,1.1), yticks=[], xlabel="Difference in outcome")
    ax.legend(loc="upper left", fontsize=9)


def register():
    add("statistics-3","An interval can span both zero and a meaningful effect",
        "This interval crosses zero and also extends beyond the allowed ±0.02 equivalence margin. A nonsignificant difference does not establish equivalence.",
        ("Compare both on the same scale", equivalence_panel))
    add("statistics-4","Selection magnifies the luckiest estimate",
        "All ten groups below were sampled from the same zero-effect model. Selecting the tallest bar after seeing the results picks positive noise. Check it on independent data.",
        bars("Independent noise, fixed seed",range(1,11),np.random.default_rng(31).normal(0,.08,10),"Estimated effect"))
    add("bootstrap-1 bootstrap-2 bootstrap-4 measurement-4","A bootstrap makes many new samples from one observed set",
        "Resample items with replacement and recompute the statistic each time. This example resamples five binary outcomes. Varying training seeds is a separate source of uncertainty.",
        bars("Exact bootstrap distribution for three wins in five",["0",".2",".4",".6",".8","1"],[.4**5,5*.6*.4**4,10*.6**2*.4**3,10*.6**3*.4**2,5*.6**4*.4,.6**5],"Probability of resampled mean"))
    add("actorcritic-4","Two gradient directions can interfere",
        "These gradients point in partly opposing directions. Their negative dot product indicates conflict on shared parameters; adding them partly cancels an update.",
        arrows("Shared-parameter gradients",[("Actor",(0,0),(2,1)),("Critic",(0,0),(-2,1)),("Sum",(0,0),(0,2))]))
    add("dqn-1 dqn-2 actorcritic-1 doubleq-1","Freeze the target during a critic update",
        "The loss compares the current prediction against a target computed from reward and a next-state value. Backpropagation updates only the prediction side for this step.",
        network("Which branch receives this gradient?",{"Q current":(0,.75),"fixed target":(0,.22),"loss":(.52,.5),"update Q":(1,.5)},[("Q current","loss"),("fixed target","loss"),("loss","update Q")]))
    add("doubleq-3","Maximization selects favorable noise",
        "Each action estimate is equally likely to be −1 or +1 around a true value of zero. The maximum of two independent estimates is +1 in three of four cases.",
        matrix("Max over two noisy value estimates",[[-1,1],[1,1]],"Action B (−1,+1)","Action A (−1,+1)"))
    add("modelbased-1 modelbased-2 modelbased-3","Small dynamics errors accumulate across rollout steps",
        "Starting from the same real state, toy models advance by 0.9 or 1.1 instead of 1. Their predictions fan apart. Short branches limit this compounding error.",
        lines("Predicted state from a shared start",np.arange(8),[("Environment",np.arange(8)),("Model A",.9*np.arange(8)),("Model B",1.1*np.arange(8))],"Rollout step","State"))
    add("planning-1 planning-2 planning-3","Search allocates visits to competing branches",
        "A leaf value estimates future return. Backups change the next search choices. At the root, 8 visits versus 2 give a normalized visit target of 0.8 versus 0.2.",
        network("Illustrative search tree",{"root":(.5,1),"A · 8":(.22,.52),"B · 2":(.81,.52),"leaf 1":(0,.05),"leaf 2":(.42,.05),"leaf 3":(.82,.05)},[("root","A · 8"),("root","B · 2"),("A · 8","leaf 1"),("A · 8","leaf 2"),("B · 2","leaf 3")]))
    add("offline-1 offline-3 offlinecql-1 offlinecql-2 offlinecql-3","An unseen action can look best to an extrapolating critic",
        "Actions A and B have data; C has none. Its high predicted value is unsupported. Conservative penalties can reduce overestimation but excessive penalties can suppress useful actions.",
        bars("Logged action counts",list("ABC"),[60,40,0],"Transitions"),
        bars("Example fitted critic",list("ABC"),[1,.8,3],"Predicted value"))
    add("td-3 advantage-3 advantage-atom7","A trace interpolates between short and long targets",
        "A residual k steps ahead gets weight (γλ)ᵏ. At λ=0 only the current residual survives; increasing λ incorporates more future observations.",
        lines("γ = 0.9",range(7),[(str(lam),(lam*.9)**np.arange(7)) for lam in (0,.5,1)],"Residual lag","Weight"))
    add("policy-3","A state baseline cancels in expectation",
        "For a fair two-action sigmoid policy, the score values are +½ and −½. Multiplying both by the same state-only baseline still gives zero average contribution.",
        bars("Score contributions weighted by action probability",["A","B"],[.25,-.25],"Weighted score"))
    add("vtrace-1 vtrace-2 vtrace-3 vtrace-4 rlsystems-1 rlsystems-2 rlhf-3","Policies can give the same action different probabilities",
        "For behavior probability 0.2 and current probability 0.3, the correction ratio is 1.5. Use the distribution that actually sampled the action; a reference policy has a different role.",
        bars("Probabilities on the same logged action",["Behavior","Current","Reference"],[.2,.3,.4],"Probability"))
    add("dpcontrol-3","A transition matrix supplies the expectation",
        "In row 0 the next state is 0 with probability ¼ or 1 with probability ¾. With values 0 and 4, its expected next value is 3 without drawing a rollout.",
        matrix("Rows: current states; columns: next states",[[.25,.75],[.5,.5]],"Next state","Current state"))
    add("entropy-4","A chain of random choices rarely completes a long path",
        "If each of ten required independent actions is chosen with probability ½, the chance of the whole sequence is only 1/1,024 despite high per-step entropy.",
        lines("Probability every action matches",np.arange(1,11),[("Success",.5**np.arange(1,11))],"Required actions","Probability"))
    add("ppo-4 policyconstraint-2 policyconstraint-4","Clipping one sampled ratio is a local intervention",
        "These policies both assign 0.5 to A, so A’s ratio is one. The probabilities for B and C differ greatly. A single sampled ratio cannot bound the full KL.",
        matrix("Rows: old and new policies",[[.5,.45,.05],[.5,.05,.45]],"Action A, B, C","Policy"))
    add("group-3 group-4","Centering removes a common reward",
        "If every sampled answer gets zero then all deviations from the within-prompt mean are zero. More identical outcomes add no relative reward contrast.",
        bars("Centered reward for four failures",list("ABCD"),[0,0,0,0],"Deviation from group mean"))
    add("dpo-3 dpo-4 dpo-atom7","A pair margin can improve even when both answers lose probability",
        "If the chosen log ratio falls by 1 and the rejected one falls by 3, the chosen-minus-rejected margin improves by 2. The loss is softplus of the negative scaled margin.",
        bars("Changes in policy/reference log ratio",["Chosen","Rejected","Margin"],[-1,-3,2],"Change"))
    add("sft-1 sft-2","Prompt tokens supply context even when their targets are masked",
        "Only response targets create direct loss terms. The response can still read the prompt through attention, so gradients can travel back through prompt representations.",
        matrix("Input positions: two prompt, two response",[[0,0,1,1]],"Target position","Loss mask"))
    add("preferences-2 preferences-3 judge-1 causaltest-1 causaltest-3","Use matched pairs to isolate a cue",
        "Evaluate the same content in both orders. If the preferred identity flips with position, the comparison is sensitive to order. Crossing the conditions separates position from identity.",
        matrix("Which answer appears first? 0=A, 1=B",[[0,1],[1,0]],"Presentation","Item"))
    add("distprefs-1 distprefs-2 evaldata-3","The distribution of examples changes the estimated result",
        "A dataset with 80% easy prompts will emphasize them more than traffic with 30% easy prompts. Performance on that dataset need not equal the deployment average.",
        bars("Easy-prompt share",["Dataset","Traffic"],[.8,.3],"Fraction"))
    add("masked-1 masked-4 cross-3","Encoder and decoder have different access patterns",
        "A target position may read all available source positions. Self-attention on target positions still cannot read future target tokens.",
        matrix("Rows: target queries; columns: 2 source, 3 target",[[1,1,1,0,0],[1,1,1,1,0],[1,1,1,1,1]],"Source then target tokens","Target index"))
    add("dedup-2","Overlap of sets can be measured before training",
        "Two token-shingle sets share 2 of their 4 distinct elements, so their Jaccard similarity is ½. MinHash can screen candidates before exact checks.",
        matrix("Membership in sets A and B",[[1,1,1,0],[0,1,1,1]],"Shingle","Document"))
    add("tokenizer-1","Merge adjacent symbols that frequently occur together",
        "In this tiny training corpus, the pair a,b appears three times across words. BPE can merge that pair into one symbol for the next round.",
        bars("Pair counts in ab, ab, abc",["ab","bc"],[3,1],"Occurrences"))
    add("mup-1 mup-2 mup-3 mup-4","Check whether a tuned learning rate transfers with width",
        "Plot held-out loss at several rates for each width under the same parametrization. Aligned minima are evidence of transfer in this experiment.",
        lines("Illustrative width sweep",[-4,-3,-2],[("Narrow",[2.2,1.6,2.5]),("Wide",[1.9,1.4,2.1])],"log₁₀(learning rate)","Held-out loss"))
    add("distillation-2 selfdistill-1 selfdistill-2 selfdistill-3","The teacher supplies a target distribution",
        "A student can chase a softened or moving target while the teacher is held fixed for the backward pass. Equal outputs on every image provide no discriminating signal.",
        matrix("Illustrative teacher probabilities",[[.7,.2,.1],[.1,.25,.65]],"Class","Image"))
    add("diffusion-3","Reverse generation uses a chain of transitions",
        "Training can sample a single time index for an example. A sampler repeatedly predicts an update at its current noise level to move toward a less noisy sample.",
        flow("Reverse path",["Start at high noise","Estimate a denoising update","Step to a lower noise level","Repeat using the new sample"]))
    add("position-4 decodetests-1 decodetests-3 context-1 context-2 context-3","Causal eligibility uses global token positions",
        "A query at global position 2 may read keys 0, 1 and 2. Splitting the sequence after position 1 must not reset the causal rule for the second block.",
        matrix("Full causal mask before sharding",np.tri(4),"Global key index","Global query index"))
    add("accumulate-3 ograd-3","Accumulated gradients add until cleared",
        "Two microbatches with identical mean gradient 2 give sum 4, but their combined mean is 2. Scaling and resetting at the right boundaries preserve the intended update.",
        bars("Two equally sized microbatches",["Batch 1","Batch 2","Sum","Mean"],[2,2,4,2],"Gradient"))
    add("ograd-1 ograd-2 ograd-4","Detach cuts a backward path",
        "A detached value can still be used numerically. The loss has no backward route across the cut to earlier operations, and a saved scalar need not retain the graph.",
        flow("Backward route",["Loss","Downstream operation","Detached activation","Earlier operations get no gradient here"]))
    add("compilation-4 jax-1","Batching repeats the same function across rows",
        "Applying f(x)=x² to a batch returns one squared value per row. Its gradient 2x can be checked on the same batch; identical forward outputs alone do not test a backward rule.",
        matrix("Columns: x, f(x), derivative",[[-2,4,-4],[0,0,0],[3,9,6]],"Quantity","Example"))
    add("measurement-3","Rounded addition depends on grouping",
        "In float32, adding 1 to 100,000,000 can lose the unit. Canceling the large positive and negative numbers before adding 1 preserves it.",
        bars("Result of two float32 groupings",["(a+b)+c","a+(b+c)"],[float((np.float32(1e8)+np.float32(-1e8))+np.float32(1)),float(np.float32(1e8)+(np.float32(-1e8)+np.float32(1)))],"Stored result"))
    add("rngseed-1 rngseed-4 remat-3","Reusing a random stream reproduces its draws",
        "Two workers initialized from the same seed draw the same sequence. During stochastic checkpoint recomputation, replaying the original mask is precisely what is needed.",
        matrix("Top two rows share a seed",np.array([np.random.default_rng(seed).integers(0,10,5) for seed in [2,2,3]]),"Draw","Stream"))
    add("sampling-3","Temperature changes odds between tokens",
        "With logits 1 and 0, lowering temperature multiplies their log odds by 1/T. The already leading token takes a larger probability share.",
        lines("Probability of the leading token",[.25,.5,1,2,4],[("Leader",1/(1+np.exp(-1/np.array([.25,.5,1,2,4]))))],"Temperature","Probability"))
    add("heapstream-4","Normalize retained weights",
        "A top-k filter keeping probabilities 0.4 and 0.1 retains half the original mass. Dividing by that half produces a valid [0.8,0.2] sampling distribution.",
        bars("New probabilities",["Token A","Token B"],[.8,.2],"Probability"))
    add("beam-3","A product of conditional probabilities shrinks with length",
        "At constant token probability 0.8, a longer sequence has less joint probability. A decoder optimizing raw sequence log probability can favor early termination.",
        lines("Constant probability 0.8 per token",np.arange(1,9),[("Joint",.8**np.arange(1,9))],"Length","Probability"))
    add("ablation-1 ablation-2 ablation-3 curriculumdata-4","Cross two changes to estimate their separate effects",
        "Run both algorithm choices at both budgets. Comparing cells within a column fixes budget; a diagonal comparison confounds budget with algorithm.",
        matrix("Illustrative score by algorithm and budget",[[.70,.76],[.72,.78]],"Small / large budget","Baseline / new"))
    add("mechanismtest-1 mechanismtest-2 circuits-3 features-4","Intervene while controlling for perturbation size",
        "An ablation changes the output under the proposed intervention. Comparing a matched-size random direction helps distinguish a specific feature effect from generic damage.",
        bars("Illustrative score after intervention",["Baseline","Target","Random"],[.83,.61,.81],"Score"))
    add("audio-1","Hear a pitch sweep as a moving band",
        "Time runs horizontally. Brighter cells have more acoustic energy. A rising tone traces a rising band across the log-energy mel filterbank.",
        spectrogram())
    add("launch-editor alignment-2","Check feasibility before comparing tradeoffs",
        "A 200 ms latency cap excludes the high-quality 240 ms configuration. Pareto comparisons under this mandate use the feasible candidates.",
        scatter("Illustrative candidate models",[("Within cap",[110,165],[.76,.81]),("Over cap",[240],[.87])],"p99 latency (ms)","Quality"))
    add("validation-1 process-4","Split related observations as a group",
        "Rows are subjects or source problems. Each contributes three related observations. Splitting whole rows prevents a group from appearing on both sides.",
        matrix("0 = train, 1 = test", [[0,0,0],[1,1,1],[0,0,0]], "Observation", "Group"))
    add("validation-2 validation-3","Draw the prediction cutoff first",
        "At triage, only information on or before time zero is available. Later measurements can be useful labels, but using them as inputs gives the model a view of the future.",
        scatter("Example timeline", [("Available",[-3,-1,0],[0,0,0]),("Future",[1,3],[0,0])], "Hours relative to triage", ""))
    add("validation-4","Tune inside each outer training fold",
        "Hold group C aside. Tune on A and B, refit on A+B, and score once on C. Rotate the outer held-out group to evaluate the tuning procedure.",
        matrix("Rows: inner run 1, inner run 2, outer score",[[0,1,2],[1,0,2],[0,0,3]],"Group A, B, C","0 fit · 1 tune · 2 reserve · 3 test"))
    add("nonconvex-2","Trace gradient sizes back through the network",
        "The output-layer gradient is healthy, but the early layers receive almost no signal. The first large drop narrows the search for saturation or an unstable chain of derivatives.",
        lines("One backward pass",range(1,6),[("Log magnitude",[-7,-6,-3,-1,0])],"Layer from input to output","log₁₀ gradient norm"))
    add("curriculumdata-3","Compare task mixtures on the same axes",
        "Here eight in ten generated tasks are easy, versus two in ten real tasks. Separate results by difficulty to see what an aggregate improvement conceals.",
        matrix("Rows: generated and real; columns: easy and hard",[[.8,.2],[.2,.8]],"Difficulty band","Source"))
    add("databudget-4 lossmask-atom6","Count positions that contribute to the loss",
        "Six text positions are processed. Only the three entries marked 1 contribute a target. Average their summed loss over three and count them as useful work.",
        matrix("Supervision mask for two sequences",[[0,1,1],[0,1,0]],"Token position","Sequence"))
    add("lmobjective-atom5","A unigram model ignores the prefix",
        "Training counts A:B:C = 3:2:1 yield the same next-token probabilities after either prefix.",
        matrix("Rows: two different prefixes",[[.5,1/3,1/6],[.5,1/3,1/6]],"Next token A, B, C","Prefix index"))
    add("kernelgpu-1","Count active lanes on each branch",
        "In a four-lane illustration, lanes 0 and 2 take one branch while lanes 1 and 3 take the other. Only half the lanes do useful work during each branch instruction.",
        matrix("1 = active; columns are lanes",[[1,0,1,0],[0,1,0,1]],"Lane index","Branch instruction"))
    add("kernelgpu-4","Add independent pairs before combining them",
        "Inputs 1, 3, 2 and 6 can produce 4 and 8 in parallel. A final addition gives 12. The final accumulator sees only two partial sums.",
        network("A tree reduction",{"1+3":(.1,.83),"2+6":(.1,.18),"4":(.52,.83),"8":(.52,.18),"12":(.94,.5)},[("1+3","4"),("2+6","8"),("4","12"),("8","12")]))
    add("collective-3 collective-4","Smaller buckets incur more startup costs",
        "For 8 MB and 1 MB/ms, payload transfer costs 8 ms. With 1 ms startup per bucket, eight buckets cost 16 ms in isolation. They can start earlier during backpropagation.",
        bars("Communication time before overlap",["1 bucket","2 buckets","8 buckets"],[9,10,16],"Milliseconds"))
    add("mfutime-4","Match the peak to the executed operations",
        "A dense workload at 3 PFLOP/s reaches 50% of a 6 PFLOP/s dense peak. Dividing by a 12 PFLOP/s structured-sparse peak incorrectly reports 25%.",
        bars("Hardware rates in one example",["Achieved","Dense peak","Sparse peak"],[3,6,12],"PFLOP/s"))
    add("retriever-1 retriever-4","Score a query against stored document vectors",
        "The fixed query (1,2) gives dot products 2 and 5 with the two stored rows. Re-encoding documents after an encoder change can alter both scores and their ranking.",
        matrix("Each row is a document",[[2,0],[1,2]],"Feature","Document index"))
    add("verifiers-3 rubrics-2","Check a grader at its numerical boundary",
        "With a target of 10 m and absolute tolerance 0.2 m, 9.9 m passes and 10.3 m fails. Hand-labeled cases on either side detect mistaken comparisons.",
        scatter("Measured answers after parsing units",[("Accepted",[9.9,10.1],[0,0]),("Rejected",[9.7,10.3],[0,0])],"Answer (meters)",""))
    add("agentcredit-2 process-1 process-2","Locate an error along a trajectory",
        "Both runs finish unsuccessfully. Marking each step as valid (1) or invalid (0) locates different first errors in runs A and B. The terminal reward alone is zero for both.",
        matrix("Per-step checks",[[1,0,0],[1,1,0]],"Step index","Run A or B"))
    add("weightquant-3","Look past the average reconstruction error",
        "A small change in one high-sensitivity weight can cause a large output change for a rare activation. Compare model outputs on representative slices.",
        bars("Illustrative absolute output error",["Frequent","Rare"],[.02,.9],"Output units"))
    add("decodetests-4","Find the first disagreeing decoding step",
        "The two decoders agree at step 0 and first diverge at step 1 on the same forced prefix. After they choose different tokens, their later inputs can differ as well.",
        lines("One vocabulary logit on matched prefixes",[0,1,2],[("Reference",[1,1.3,1.6]),("Candidate",[1,1.1,1.55])],"Step","Logit"))
    add("complexity-1","A constant lookup can have different latency",
        "Both examples perform one hash lookup. Different key placement changes memory access cost. Average lookup counts alone cannot predict end-to-end latency.",
        bars("Illustrative timings",["Cache hit","Cache miss"],[5,80],"Nanoseconds per lookup"))
    add("budgetdesign-1-part3","A short memory peak can exceed capacity",
        "Four allocations of 4, 7, 13 and 4 GiB average 7 GiB. The peak still exceeds a device capacity of 12 GiB.",
        lines("Memory during one step",range(4),[("Allocated",[4,7,13,4]),("Capacity",[12]*4)],"Phase index","GiB"))
    add("frontierstudy-2 launch-3","The mean can hide a failure on one slice",
        "With equally sized groups, both profiles average 0.8. The second falls to 0.65 on group B. A held-out test on B distinguishes them.",
        matrix("Rows: two profiles; columns: groups A and B",[[.8,.8],[.95,.65]],"Group","Profile"))
    add("frontierstudy-3","Thresholding can turn a slope into a jump",
        "An underlying score improves smoothly across models. Scoring every value below 0.5 as a failure creates an abrupt jump when that threshold is crossed.",
        lines("Same predictions, two scoring rules",range(1,6),[("Partial credit",[.2,.35,.49,.51,.65]),("Thresholded",[0,0,0,1,1])],"Model index","Score"))
    add("scalingbreak-4","Count cost per successful request",
        "If attempts cost 1 unit each and succeed independently with probability p, the expected cost until success is 1/p. At p=0.5, retries double effective cost.",
        lines("Independent retries",np.linspace(.25,1,60),[("Expected cost",1/np.linspace(.25,1,60))],"Success probability per attempt","Cost units per success"))
    add("experiments-4","Repeated looks give noise more chances",
        "For intuition, independent tests at 5% have chance 1−0.95ᵏ of at least one false alarm. Looks at accumulating data are dependent, so this curve is illustrative. Prespecify a sequential boundary for that design.",
        lines("Independent tests under the null",range(1,11),[("Any false positive",1-.95**np.arange(1,11))],"Number of tests","Probability"))
    add("trees-3","A tiny leaf can memorize an observation",
        "With minimum leaf size 2, a split isolating one training example is disallowed. Larger leaves average over more observations.",
        network("Candidate split of ten observations",{"10":(.1,.5),"1":(.85,.8),"9":(.85,.2)},[("10","1"),("10","9")]))
    add("trees-4","Shuffle one feature on the held-out set",
        "Keep outcomes and the fitted model fixed. If accuracy drops from 0.84 to 0.66 after shuffling feature A, its permutation importance on this set is 0.18.",
        bars("Held-out accuracy",["Original","Shuffle A","Shuffle B"],[.84,.66,.82],"Fraction correct"))
    add("multilabel-4","Look for the true class inside the first k",
        "For scores A=0.4, B=0.3, C=0.2 and D=0.1, a ground truth of C misses at k=1 and hits at k=3. Top-k accuracy averages that indicator across cases.",
        bars("Predicted probabilities",list("ABCD"),[.4,.3,.2,.1],"Probability"))
    add("init-3","Identical hidden units can remain copies",
        "If incoming and outgoing weights and biases start identically, two units can receive exactly the same gradients. After each update their rows still match, wasting independent features.",
        matrix("Rows are units, columns are update steps",[[.1,.24,.37],[.1,.24,.37]],"Update","Hidden unit"))
    add("contrast-1 contrast-3 retriever-3","A contrastive loss moves pairs in opposite ways",
        "Place the anchor at zero on a line. Pull its positive view from 2 toward 1 and push a negative from −2 toward −3. A mislabeled negative pushes related items apart.",
        arrows("Illustrative pairwise updates",[("Pull positive",(2,.5),(1,.5)),("Push negative",(-2,-.5),(-3,-.5))]))
    add("cross-4","Mask padded source positions for every query",
        "A source of length two pads to four positions. Every target query can read the two real source keys. No query may read either padding slot.",
        matrix("1 = source key may be read",[[1,1,0,0],[1,1,0,0],[1,1,0,0]],"Source position","Target query"))
    add("lmobjective-3 lossmask-editor lossmask-4","Sum losses and counts before dividing",
        "Two groups have 2 and 8 targets with mean losses 1 and 3. Their global mean is (2+24)/10=2.6. An empty group adds zero to both sums; an entirely empty batch needs an explicit rule.",
        bars("Contribution to the loss numerator",["2 targets","8 targets","0 targets"],[2,24,0],"Summed token loss"))
    add("mixture-3","Sampling documents and sampling tokens differ",
        "One long document of 90 tokens and nine short documents of 10 tokens supply equal token totals. The long-document domain is only one tenth of the document count.",
        matrix("Rows: long domain, short domain",[[1,90],[9,90]],"Documents (0) or tokens (1)","Domain"))
    add("scalegrad-3","Changing only one variable leaves the other untested",
        "All measured points lie at one model size. These measurements reveal variation along the token axis. They cannot identify a size exponent separately.",
        scatter("Training configurations",[("Observed",[4,4,4,4],[1,2,4,8])],"Model size (billion parameters)","Training tokens (billions)"))
    add("packing-atom5 packing-4","Prevent a boundary from joining independent texts",
        "Positions 0–1 belong to document A and 2–3 to B. A block-causal mask keeps attention inside each document. Separately mask the next-token target that crosses from A to B.",
        matrix("Allowed query–key pairs",[[1,0,0,0],[1,1,0,0],[0,0,1,0],[0,0,1,1]],"Key position","Query position"))
    add("onlineattention-3","Re-express earlier weights at a new maximum",
        "A score of 2 used to have weight exp(2−2)=1. When the maximum rises to 3, the old weight becomes exp(2−3)≈0.368. Multiply both cached sums by this same factor.",
        bars("Unnormalized weight of the old score",["Old max 2","New max 3"],[1,np.exp(-1)],"Weight"))
    add("failcost-3","A job needs every required device to survive",
        "If devices survive an interval independently with probability 0.99, all n survive with probability 0.99ⁿ. More devices mean more opportunities for the job to be interrupted.",
        lines("Independent failures, one fixed interval",range(1,101),[("Job survives",.99**np.arange(1,101))],"Required devices","Survival probability"))
    add("scans-3 scans-4","Repeated boundaries encode an empty sequence",
        "Lengths [2,0,3] give cumulative boundaries [0,2,2,5]. The second sequence occupies [2,2) and owns no token. Token index 2 belongs to the third sequence.",
        matrix("Owner of each packed token",[[0,0,2,2,2]],"Packed token index","Sequence ID in cell"))
    add("complexity-4","Copying an ever-longer prefix adds a triangle",
        "Appending by reallocating and copying the entire result writes 1+2+3+4+5=15 elements for length five. The sum n(n+1)/2 grows quadratically.",
        bars("Elements written on each append",list("12345"),[1,2,3,4,5],"Elements written"))
    add("streaming-4","Equal shard quotas can change sampling probabilities",
        "Taking ten rows from each of two shards includes every row of the small shard but just one in ten of the large shard. Each original row needs the same inclusion probability for a uniform sample.",
        bars("Sampling ten rows per shard",["10-row shard","100-row shard"],[1,.1],"Inclusion probability"))
    add("fp8-3","An outlier sets a coarse shared scale",
        "In a toy uniform quantizer with integer codes up to 7, a peak of 70 sets a step of 10. A channel with peak 0.7 can use a step of 0.1 when scaled separately. Floating-point formats have nonuniform spacing too.",
        bars("Toy quantization step",["Shared","Small channel"],[10,.1],"Weight units"))
    add("context-4","Overlapping two tasks hides the shorter one",
        "If transfers and compute overlap perfectly, a 4 ms transfer fits inside a 6 ms compute block. Serial execution needs 10 ms. This comparison ignores pipeline fill and drain.",
        bars("One steady-state block",["Serial","Overlapped"],[10,6],"Milliseconds"))
