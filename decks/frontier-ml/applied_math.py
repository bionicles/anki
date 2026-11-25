"""Visual calculations for training budgets, parallel systems and reinforcement learning."""
import numpy as np
from visual_examples import add, bars, flow, lines, matrix


def register():
    add("mixture-1 mixture-2 memorization-1","Sampling weight sets expected exposure",
        "A 12% share of 5 billion token draws is 0.6 billion code tokens. Repeating a record changes its effective sampling weight.",
        bars("Expected allocation",["Code","Other"],[.6,4.4],"Billion tokens"))
    add("samplingdata-1 samplingdata-2","Partition before workers start sampling",
        "Eight ranks with three workers each give 24 workers. Giving each four disjoint shards uses all 96 exactly once.",
        matrix("Shard counts for each rank and worker",np.full((8,3),4),"Worker","Rank"))
    add("packing-1 packing-2 packing-3","Distinguish allocated and valid positions",
        "Of 16,384 positions, 12,288 are useful and 4,096 are padding. Three quarters contribute real tokens.",
        bars("Allocated batch slots",["Useful","Padding"],[12288,4096],"Token positions"))
    add("lmobjective-1 lmobjective-2","From mean surprise to perplexity",
        "A model assigning one-fifth to each observed token has mean NLL ln 5 and perplexity 5. Perplexity exponentiates mean NLL in nats.",
        lines("One observed token probability per example",[.1,.2,.4,.5,1],[("Perplexity",[10,5,2.5,2,1])],"Observed probability","Effective choices"))
    add("budget-1 budget-2 budget-3 budgetdesign-2","Follow the units from work to time",
        "Dense training at 7B parameters and 100B tokens costs about 4.2×10²¹ FLOPs. Divide by 2×10¹⁸ FLOP/s to get 2,100 s. Multiply a token rate by productive time for the inverse calculation.",
        flow("Compute ledger",["Parameters × tokens × 6","Total training FLOPs","Divide by sustained FLOP/s","Elapsed seconds"]))
    add("scaling-1 scalegrad-1 scalegrad-2","Balance two sources of reducible loss",
        "At fixed ND=16 with equal terms 1/N and 1/D, the total is minimized at N=D=4. Quadrupling compute allows each balanced dimension to double.",
        lines("Fixed product in normalized units",[1,2,4,8,16],[("Total",[1+1/16,.5+.125,.5,.125+.5,1/16+1])],"Parameters N","Loss above floor"))
    add("dataquality-1 dataquality-2","Filtering changes the mixture",
        "Retaining 900k majority examples and 30k minority examples leaves 30/930=3.23% minority share. Overall retention can obscure this shift.",
        bars("Minority share",["Before","After"],[100/1100,30/930],"Fraction"))
    add("databudget-1 databudget-2","Revisiting data increases exposures",
        "A 12B-token corpus supplies 30B draws in 2½ epoch-equivalents. With random sampling, individual records may be seen more or fewer times.",
        lines("Uniform nominal accounting",[0,1,2,2.5],[("Draws",[0,12,24,30])],"Epoch-equivalents","Billion draws"))
    add("trainhealth-1 curriculum-2","An average can hide a domain regression",
        "With 90% weight on domain A, improving A can lower aggregate loss even while B worsens. Inspect the component curves.",
        lines("Illustrative loss after adaptation",[0,1,2],[("A",[2,1.7,1.4]),("B",[2,2.3,2.6]),("Average",[2,1.76,1.52])],"Training stage","Loss"))
    add("lossmask-1 lossmask-2 lossmask-3 lossmask-atom7 datapar-1 datapar-2","Weight ranks by valid tokens",
        "Ranks with loss sums 6 and 10 over 2 and 5 tokens give 16/7 globally. Averaging the two local means would over-weight the smaller rank. DDP’s rank average requires a factor R/N on each local sum.",
        matrix("Columns: sum and valid tokens",[[6,2],[10,5]],"Statistic","Rank"))
    add("multitoken-1 multitoken-2","Auxiliary horizons add separate losses",
        "The hidden state at position 0 can predict targets 1 and 2. Their losses have separate weights; a good auxiliary score need not mean lower next-token loss.",
        matrix("Supervised future positions",[[0,1,1,0],[0,0,1,1]],"Target token","Source token"))
    add("roof-1 roof-3 roof-atom5","A roofline has two ceilings",
        "With 2 TB/s and 20 FLOP/byte, memory allows at most 40 TFLOP/s. A higher 200 TFLOP/s compute limit leaves bandwidth as the bottleneck.",
        lines("Hardware bounds",[0,20,50,100,125],[("Bandwidth",[0,40,100,200,250]),("Compute",[200]*5)],"FLOP/byte","TFLOP/s"))
    add("tiling-1 tiling-2 flash-1 flash-3","Process a matrix in tiles",
        "Numbers label four tiles of one 4×4 array. A kernel can load a tile once and reuse it locally. Exact attention still processes all query–key pairs.",
        matrix("Tile IDs in a full array",[[1,1,2,2],[1,1,2,2],[3,3,4,4],[3,3,4,4]],"Column","Row"))
    add("flash-2 onlineattention-1 onlineattention-2","Bring blocks to one exponential scale",
        "Logits 0 and ln 3 carry unnormalized weights 1 and 3. Their weighted average of 2 and 6 is 5. Subtracting a shared max rescales both numerator and denominator equally.",
        bars("Normalized block weights",["Block 1","Block 2"],[.25,.75],"Share"))
    add("precision-1 precision-2 precision-3 rms-4","Scale up small gradients, then undo the scaling",
        "Scaling multiplies backward gradients without changing their intended unscaled values. Undo the scale before clipping; it cannot repair an overflow already present in the forward pass.",
        flow("Example loss scale 128",["Unscaled gradient 0.00001","Scaled gradient 0.00128","Divide by 128","Clip and update in original units"]))
    add("precision-4 fp8-1 fp8-2","Exponent and fraction bits buy different things",
        "In an 8-bit float, giving an extra bit to the exponent leaves one fewer for the fraction. The exponent controls range; the fraction controls spacing within a range.",
        matrix("Rows: E4M3 and E5M2; columns: sign, exponent, fraction",[[1,4,3],[1,5,2]],"Field","Format"))
    add("memory-1 memory-2 sharding-1 sharding-2","Inventory the persistent arrays",
        "Weights and gradients cost 2 bytes each, the master copy 4 and the two moments 8 together. That is 16 bytes per parameter. Sharding divides selected arrays across ranks.",
        bars("Bytes per parameter",["Weight","Grad","Master","Moments"],[2,2,4,8],"Bytes"))
    add("parallel-1 parallel-2","A pipeline fills and drains",
        "Four stages processing eight microbatches need eleven forward time slots. Each row is busy for eight, giving ideal utilization 8/11.",
        matrix("One means a busy stage",[[int(i<=j<i+8) for j in range(11)] for i in range(4)],"Time slot","Stage"))
    add("collective-1 collective-2","Sum shards, then share the results",
        "On four ranks each ring phase sends three quarter-sized chunks per rank. Reduce-scatter plus all-gather sends 1.5 times the original payload.",
        bars("Bytes per rank as fraction of payload",["Scatter","Gather","Total"],[.75,.75,1.5],"Payloads sent"))
    add("profiling-2 profiling-atom5","Only the improved part speeds up",
        "In a 100 ms step with 40 ms of attention, halving attention saves 20 ms. The speedup is 100/80 = 1.25×.",
        bars("Time per step",["Before","After"],[100,80],"Milliseconds"))
    add("pipeline-1 pipeline-2","The slowest stage sets throughput",
        "Six workers at 100 samples/s can just match demand of 600 samples/s under perfect scaling. Overlap keeps independent stages busy.",
        lines("Ideal input supply",[1,2,4,6,8],[("Supply",[100,200,400,600,800]),("Demand",[600]*5)],"Workers","Samples/s"))
    add("accumulate-1 accumulate-2","Build a batch across devices and steps",
        "Sixteen ranks × four examples supplies 64 examples per microstep. Sixteen such microsteps supply 1,024 before an optimizer update.",
        lines("Cumulative examples",[1,4,8,16],[("Batch",[64,256,512,1024])],"Accumulation steps","Examples"))
    add("mfutime-1 mfutime-2","Compare useful arithmetic to peak",
        "3.2 PFLOP/s of model work divided by an 8 PFLOP/s peak is 40%. Idle slots and non-model work consume the remaining capacity.",
        bars("Same precision and hardware",["Model work","Peak"],[3.2,8],"PFLOP/s"))
    add("memoryio-1 memoryio-2 remat-1 remat-2","Compare serial and overlapping work",
        "Twelve milliseconds of compute and eight of independent copy take 20 ms in series or at best 12 ms overlapped. Recomputing discarded activations trades extra work for memory.",
        bars("Ideal elapsed time",["Serial","Overlapped"],[20,12],"Milliseconds"))
    add("collectiveops-1 collectiveops-2 collectiveops-3","Partition a matrix along its output axis",
        "Color-coded IDs mark column owners. Each device computes its own output columns. Splitting input rows instead produces partial sums for the same outputs.",
        matrix("Two ranks share the columns",[[0,0,1,1],[0,0,1,1],[0,0,1,1]],"Output","Input"))
    intervals=np.arange(10,101,2)
    add("failcost-1 failcost-2","Balance saving too often against losing work",
        "A first-order overhead estimate is C/T + T/(2M). With two-minute checkpoints and M=400 minutes, the minimum occurs at T=40 minutes.",
        lines("Expected overhead fraction",intervals,[("Saving",2/intervals),("Lost work",intervals/800),("Total",2/intervals+intervals/800)],"Interval (min)","Fraction"))
    add("mdp-2 mdp-atom5 capstonerl-3-part4","Discount later rewards before adding",
        "With rewards 2 then 4 and discount ½, both contribute 2 at the first step. Later rewards are multiplied by progressively higher powers of the discount.",
        bars("Value at the first step",["Now","Next","Sum"],[2,2,4],"Discounted reward"))
    add("bellman-1 bellman-3 qlearn-1 qlearn-2 doubleq-2","Selection and evaluation can use different values",
        "The online network picks B because 5 exceeds 4. The target network evaluates B at 3. With reward 1 and discount ½ the Double DQN target is 2.5.",
        matrix("Columns: actions A and B",[[4,5],[7,3]],"Action","Online (0), target (1)"))
    add("td-1 td-2 qlearn-3 actorcritic-2 advantage-atom6","A TD error compares prediction with target",
        "Current value 3 and target 0 + 0.9×4 = 3.6 leave an error of +0.6. A value update moves toward the target; the squared-loss gradient has the opposite sign.",
        bars("One transition",["Prediction","Target","Error"],[3,3.6,.6],"Value"))
    add("td-atom5 capstonerl-3 capstonerl-3-part2","A time limit can hide future value",
        "At a true terminal state no future value remains. If a continuing rollout is only truncated, dropping its continuation removes γV(next) from the target.",
        bars("Reward 0, γ=0.9, V(next)=10",["True terminal","Truncation"],[0,9],"Target"))
    add("policy-1 policy-2 advantage-1 capstonerl-3-part3","Advantage measures value above a baseline",
        "An action worth 4 in a state worth 6 has advantage −2. Its sampled policy-gradient term favors reducing that action’s log probability.",
        bars("Same state",["Action Q","Baseline V","Advantage"],[4,6,-2],"Value"))
    add("advantage-2","Give later residuals a smaller vote",
        "Residuals 1 and 2 with γλ=0.45 contribute 1 and 0.9. Their sum gives the two-residual advantage estimate 1.9.",
        bars("Weighted residuals",["Now","Next","Sum"],[1,.9,1.9],"GAE contribution"))
    ratios=np.linspace(.4,1.6,121)
    add("ppo-1 ppo-2 ppo-3 ppo-editor ppo-atom6","PPO clips different tails for different signs",
        "The objective takes the smaller of raw and clipped contributions. At ratio 1.4, advantage +2 gives 2.4 but −2 gives −2.8. A ratio of one means no change.",
        lines("Clipped surrogate as a function of ratio",ratios,[(str(a),np.minimum(ratios*a,np.clip(ratios,.8,1.2)*a)) for a in (2,-2)],"New / behavior probability","Contribution"))
    add("offline-2","Trajectory weights multiply",
        "A target probability twice the behavior probability at each step yields a three-step ratio of 8. Long products can amplify a few trajectories; clipping changes that influence.",
        lines("Ratio 2 at each sampled step",[0,1,2,3,4],[("Product",[1,2,4,8,16])],"Steps","Importance ratio"))
    add("bandits-1 bandits-2","Exploration also sometimes picks the greedy arm",
        "With ε=0.2 and four arms, exploration contributes 0.05 to each. The greedy arm also receives the 0.8 exploitation mass.",
        bars("Action probabilities",list("ABCD"),[.85,.05,.05,.05],"Probability"))
    add("dpcontrol-1 dpcontrol-2","A contraction shrinks the worst-case error bound",
        "With discount 0.9, an initial sup-norm error bound of 4 becomes at most 3.6 after one exact fixed-policy backup.",
        lines("Repeated upper bound",range(9),[("Bound",4*.9**np.arange(9))],"Backups","Value error bound"))
    add("credit-1 credit-2","Potential shaping rewards a discounted change",
        "The current potential is 2 and the discounted next potential is 2.7. Their difference adds 0.7 to the transition reward.",
        bars("Potential terms",["Current","Discounted next","Difference"],[2,2.7,.7],"Potential"))
    add("pomdp-1 pomdp-2","An observation shifts a belief distribution",
        "Start with equally likely states. Multiplying by likelihoods 0.8 and 0.2 gives 0.4 and 0.1; normalize to get posterior 0.8 and 0.2.",
        matrix("Rows: prior, unnormalized, posterior",[[.5,.5],[.4,.1],[.8,.2]],"Hidden state","Update stage"))
    p=np.linspace(.001,.999,101)
    add("entropy-1 entropy-2 entropy-3","Entropy peaks when probability is spread evenly",
        "A two-action policy has maximum entropy ln 2 at equal probabilities. For four equally likely actions the same calculation gives ln 4 nats.",
        lines("Binary policy entropy",p,[("Entropy",-p*np.log(p)-(1-p)*np.log(1-p))],"Probability of action A","Nats"))
    add("rewardmodel-1 rewardmodel-2 bradley-2","Reward difference controls preference odds",
        "A reward gap ln 3 gives odds 3:1 and probability ¾. Reward gaps add along chains, so the corresponding odds multiply.",
        lines("Bradley–Terry link",np.linspace(-4,4,81),[("Choice",1/(1+np.exp(-np.linspace(-4,4,81))))],"Reward of A minus B","Probability of A"))
    add("rlhf-2 rewardlength-1 rewardlength-2","Token log probabilities add",
        "For three tokens with log probabilities −1, −2 and −0.5, the sequence log probability is −3.5. Subtracting reference log probabilities gives sampled log ratios.",
        lines("Running log probability",[0,1,2,3],[("Sum",[0,-1,-3,-3.5])],"Tokens","Log probability"))
    z=np.linspace(-4,4,101)
    add("dpo-1 dpo-2 dpo-atom6","A preference margin controls logistic loss",
        "Take the chosen policy/reference log ratio minus the rejected ratio, then multiply by β. At zero the loss is ln 2. Increasing a positive margin lowers it.",
        lines("Pair loss",z,[("Loss",np.logaddexp(0,-z))],"Scaled margin","Nats"))
    add("group-1 group-2","Put rewards on a within-prompt scale",
        "Rewards 0 and 1 have mean ½ and population standard deviation ½. Centering and dividing yields −1 and +1.",
        bars("Standardized completions",["A","B"],[-1,1],"Relative reward"))
    n=np.arange(1,11)
    add("bestofn-1 bestofn-2 testtrain-1 testtrain-2 reasoning-1 reasoning-2","More attempts raise oracle coverage",
        "For independent draws with success probability p, all n fail with probability (1−p)ⁿ. A selector still has to find a correct answer in the pool.",
        lines("Chance at least one succeeds",n,[("p=.2",1-.8**n),("p=.3",1-.7**n)],"Attempts","Oracle success"))
    add("bestofn-atom5","Separate candidate coverage from selection",
        "Fifteen of twenty pools contain a solution. The selector succeeds on nine. Its accuracy conditional on an available solution is 9/15, while end-to-end success is 9/20.",
        bars("Success at each stage",["Prompts","Solvable pools","Selected"],[20,15,9],"Count"))
    add("rlrollout-1 rlrollout-2","Count generated tokens across nested batches",
        "128 prompts × eight completions gives 1,024 completions. At 256 tokens each this produces 262,144 generated tokens.",
        flow("Rollout accounting",["128 prompts","8 completions per prompt","256 tokens per completion","262,144 tokens"]))
    add("outcomesparse-1 outcomesparse-2","A group needs both outcomes for contrast",
        "Four fair independent binary outcomes have 16 equally likely patterns. One is all success and one all failure. Fourteen mixed patterns remain.",
        bars("Patterns of four completions",["All fail","Mixed","All pass"],[1,14,1],"Patterns"))
    add("policyconstraint-3","A small group can exceed the global mean",
        "The high-KL group contributes 0.10×0.03=0.003. The remaining 90% contribute zero. An average constraint can hide a much larger local change.",
        bars("KL by population",["10% group","90% group","Overall"],[.03,0,.003],"Mean KL"))
    add("capstonerl-2-part2","Divide rollout cost by total cost",
        "Generation uses 24 GPU-seconds out of a total of 32. Its share is ¾; the learner accounts for the other quarter.",
        bars("One update",["Generate","Learn"],[24,8],"GPU-seconds"))
