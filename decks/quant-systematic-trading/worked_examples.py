"""Additional worked diagrams, with the data and conventions used to compute them."""
import numpy as np

BLUE, ORANGE, GREEN = "#145974", "#ad4b1b", "#28765f"


def curve(xs, series, xlabel, ylabel):
    def draw(ax):
        for i, (name, ys) in enumerate(series.items()):
            ax.plot(xs, ys, ["-","--","-."][i], color=[BLUE,ORANGE,GREEN][i],
                    marker="o" if len(xs)<=8 else None, label=name, lw=2.4)
        if len(series)>1:
            ax.legend(fontsize=9)
        ax.set(xlabel=xlabel,ylabel=ylabel)
        ax.grid(alpha=.2)
    return draw


def amounts(labels, vals, ylabel):
    def draw(ax):
        rects=ax.bar(range(len(vals)), vals, color=BLUE, width=.65)
        ax.bar_label(rects, fmt="%.4g",padding=3,fontsize=11)
        ax.axhline(0,color="#66777e",lw=.8)
        ax.set_xticks(range(len(vals)),labels)
        ax.set_ylabel(ylabel)
        ax.margins(y=.25)
    return draw


def worked_examples():
    examples=[]
    def add(key,title,description,draw):
        examples.append(("QT-"+key,title,description,draw))
    def line(key,title,desc,x,y,xlabel,ylabel):
        add(key,title,desc,curve(x,y,xlabel,ylabel))
    def bar(key,title,desc,labels,vals,unit):
        add(key,title,desc,amounts(labels,vals,unit))

    line("compound-2","Equal percentage moves start from different bases",
         "From $100, a 20% gain makes $120. A 20% loss on $120 ends at $96.",
         [0,1,2],{"Wealth":[100,120,120*.8]},"Period","Wealth ($)")
    bar("short-2","Buying back a short position","Selling then buying back 100 shares at a $3 difference yields $300 gross. Fees leave $260.",
        ["Gross","Fees","Net"],[300,-40,260],"Position P&L ($)")
    line("futures-2","P&L scales with the futures multiplier","Three $50-per-point contracts gain or lose $150 for each point. A two-point fall costs $300.",
         [-2,-1,0,1,2],{"P&L":np.arange(-2,3)*150},"Futures move (points)","Three-contract P&L ($)")
    line("fx-2","Translate the entire foreign holding","Start at 100. The asset grows to 110 in local terms. Converting at a 5% weaker currency leaves 104.5 in initial home units.",
         [0,1,2],{"Value":[100,110,110*.95]},"0 start · 1 local gain · 2 after FX","Illustrative value")
    x=np.linspace(-.75,.75,61)
    line("bonds-2","Duration gives the slope of a price approximation","A modified duration of four gives about a 1% price decline for a 0.25 percentage point yield rise.",
         x,{"Approximate price change":-4*x},"Yield change (percentage points)","Approximate price change (%)")
    x=np.arange(30,66)
    line("options-2","Subtract the premium from put payoff","The $50 put costs $3. At $42 the difference between payoff and net profit is still $3.",
         x,{"Payoff":np.maximum(50-x,0),"Profit":np.maximum(50-x,0)-3},"Stock at expiry ($)","Dollars per share")
    bar("actions-2","Follow both parts of shareholder wealth","At the ex-date the share is worth $49 and the dividend is $1. The total equals the initial $50.",
        ["Before","Ex-price","Dividend","Together"],[50,49,1,50],"Dollars per share")
    bar("expect-2","Multiply each outcome by its probability","Frequent wins contribute $0.80. Infrequent losses contribute −$1.20. Net expectancy is −$0.40.",
        ["Wins","Losses","Expected"],[.8,-1.2,-.4],"Expected P&L per trade ($)")
    n=np.arange(4,161)
    line("sampling-2","Averaging independent observations reduces noise","With 2% outcome volatility the uncertainty of the mean is 2% divided by the square root of the observation count.",
         n,{"SE":2/np.sqrt(n)},"Independent observations","Standard error (percentage points)")
    x=np.linspace(-3,3,31)
    line("beta-2","Read an intercept and slope together","A 0.1% intercept plus 1.5 times a 2% market return gives a fitted 3.1%.",
         x,{"Fitted excess return":.1+1.5*x},"Market excess return (%)","Fitted return (%)")
    x=np.arange(6)
    line("ar-2","A shock decays geometrically","The expected offset falls from 8 to 4 to 2 under persistence 0.5.",
         x,{"Deviation":8*.5**x},"Steps after shock","Expected deviation")
    bar("garch-2","Build the next conditional variance","The intercept, shock and persistence contribute 0.1, 0.8 and 0.7 respectively.",
        ["Intercept","News","Memory","Total"],[.1,.2*4,.7*1,1.6],"Variance units")
    line("ic-2","Perfectly reversed rankings","Each step up the forecast ranking goes with one step down the outcome ranking, so rank correlation is −1.",
         [1,2,3,4],{"Outcome rank":[4,3,2,1]},"Forecast rank","Outcome rank")
    bar("combine-2","Combine signals in common units","The 60% sleeve contributes 6 bp. The 40% sleeve subtracts 2 bp.",
        ["First","Second","Blend"],[.6*10,.4*-5,4],"Forecast contribution (bp)")
    x=np.linspace(0,1,51)
    line("utility-2","Break-even probability includes the trading cost","The expected net payoff is 3p minus (1−p) minus 0.2. The line crosses zero at a win probability of 0.30.",
         x,{"Net":4*x-1.2,"Flat":0*x},"Probability of a win","Expected P&L per trade")
    bar("selfFinance-2","A rebalance consumes cash at each purchase","Start at $1,000, buy $800, sell $300 and pay $10. The ledger ends at $490.",
        ["Start","After buy","After sale","After fee"],[1000,200,500,490],"Cash balance ($)")
    x=np.arange(0,61,5)
    line("costs-2","A holding fee accrues while the short is open","On constant $100,000 notional and a 360-day basis, 30 days of 6% borrow costs $500.",
         x,{"Accrued cost":1e5*.06*x/360},"Days held","Borrow cost ($)")
    x=np.linspace(1,35,100)
    line("voltarget-2","Higher forecast risk lowers the exposure target","At a fixed 10% target, doubling forecast volatility from 10% to 20% halves desired exposure.",
         x[x>=5],{"Exposure":10/x[x>=5]},"Annualized forecast volatility (%)","Exposure multiplier")
    f=np.linspace(0,.7,141)
    line("kelly-2","Expected log growth peaks before maximum exposure","With 55% even-money wins, 0.55 log(1+f) + 0.45 log(1−f) peaks at f=0.10. Larger fractions eventually produce negative expected log growth.",
         f,{"Expected log growth":100*(.55*np.log1p(f)+.45*np.log1p(-f))},"Fraction of wealth wagered","Expected log growth × 100")
    x=np.linspace(0,.72,100)
    line("drawdown-2","Recovery gets steeper as capital falls","A 40% loss leaves 60 of every 100. Returning to 100 takes 40/60, or 66⅔%.",
         x*100,{"Gain required":100*x/(1-x)},"Drawdown magnitude (%)","Gain needed to recover (%)")
    bar("dv01-2","Offset a parallel yield exposure","Eighty short futures at $75 DV01 each contribute −$6,000 of signed DV01 against the cash bonds.",
        ["Bonds","80 short futures","Combined"],[6000,-6000,0],"Signed DV01 ($ per bp)")
    x=np.arange(4)
    line("liquidity-2","Liquidate only what daily volume permits","At 30,000 shares per day, the 90,000-share position reaches zero after three days.",
         x,{"Remaining":90-30*x},"Days of liquidation","Remaining shares (thousands)")
    h=np.linspace(-.1,1.6,80)
    line("hedge-2","Minimum residual variance as hedge size changes","With asset variance 0.04, hedge variance 0.016 and covariance 0.012, the variance curve reaches its minimum at a 0.75 hedge ratio.",
         h,{"Residual variance":.04-2*h*.012+h**2*.016},"Hedge ratio h","Variance of asset minus h × hedge")
    bar("queue-2","A fill starts only after the queue ahead clears","A 450-share sell consumes 400 ahead, then 50 of your 100 shares.",
        ["Ahead filled","Yours filled","Yours left"],[400,50,50],"Shares")
    x=np.arange(0,11)
    line("impact-2","Dollar impact multiplies size by cost per share","If size and per-share cost both scale by k, total cost scales by k². Doubling both produces four times the cost.",
         x,{"Total cost":x*x},"Common scale factor k","Cost relative to baseline")
    bar("shortfall-2","Add explicit costs to the execution-price loss","A ten-cent disadvantage across 100 shares costs $10. A $2 fee raises total implementation cost to $12.",
        ["Price loss","Fees","Total"],[10,2,12],"Cost ($)")
    bar("turnover-2","Count both executed sides","Selling $100,000 and buying $100,000 trades 20% of $1m NAV on a two-sided basis.",
        ["Sold","Bought","Total traded"],[100,100,200],"Absolute notional ($ thousands)")
    line("hac-2","A larger error bar lowers the t-statistic","With the mean fixed, t is inversely proportional to the standard error. Doubling the denominator halves t.",
         [1,2,3,4],{"t for mean of 6":[6,3,2,1.5]},"Standard error (bp)","t-statistic")
    bar("kalman-2","Move partway from prediction to observation","The innovation is 4. A gain of 0.25 adds only 1 to the prediction, placing the updated state at 11.",
        ["Prediction","Updated","Observation"],[10,11,14],"State units")
    n=np.linspace(10000,80000,100)
    line("montecarlo-2","Monte Carlo precision has diminishing returns","With independent paths, increasing from 10,000 to 40,000 reduces a $0.40 standard error to $0.20.",
         n,{"Standard error":.4*np.sqrt(10000/n)},"Independent simulated paths","Standard error ($)")
    bar("qlearning-2","The continuation value is discounted","Reward 2 and continuation 0.9 × 5 add to a Q-learning target of 6.5.",
        ["Reward","Discounted future","Target"],[2,.9*5,6.5],"Reward units")
    x=np.arange(1,11)
    line("brownian-2","Volatility grows with the square root of time","Independent daily increments of 1% volatility have 2% volatility over four days.",
         x,{"Volatility":np.sqrt(x)},"Trading days","Standard deviation (%)")
    x=np.arange(0,6)
    line("fxforward-2","Hedged currency holdings must match domestic growth","At zero euro interest, spot 1.20 USD/EUR and one year, parity gives 1.20 × (1+rUSD); at 5% the result is 1.26.",
         x,{"Forward":1.2*(1+x/100)},"Annual dollar rate (%)","One-year forward (USD/EUR)")
    x=np.linspace(60,140,81)
    line("parity-2","Two European portfolios match at expiry","At strike 100, a call plus 100 cash at expiry and the stock plus a put both pay max(stock,100). Equal terminal claims underpin parity.",
         x,{"Call + cash":100+np.maximum(x-100,0),"Stock + put":x+np.maximum(100-x,0)},"Stock at expiry ($)","Terminal value ($)")
    bar("gammahedge-2","Bring the stock hedge back to neutrality","Long option delta falls from 40 to 30 shares. A −40 hedge must move to −30, requiring a buy of 10.",
        ["Old hedge","New hedge","Trade"],[-40,-30,10],"Signed shares")
    bar("riskyturnover-2","Cross the cost hurdle before rebalancing","Six basis points of benefit less eight of incremental cost leaves −2 bp.",
        ["Benefit","Cost effect","Net"],[6,-8,-2],"Objective change (bp)")

    # These geometric and distributional examples address misconceptions on diagnostic cards.
    def covariance_cloud(ax):
        rng=np.random.default_rng(31)
        draws=rng.multivariate_normal([0,0],[[1,.72],[.72,1]],180)
        ax.scatter(draws[:,0],draws[:,1]*100,alpha=.48,s=15,color=BLUE)
        ax.set(xlabel="Asset A return (percentage points)",ylabel="Asset B return (basis points)")
    add("covariance-3","The same cloud, different units","Multiplying one axis by 100 stretches its numerical scale and covariance. Positive rescaling leaves correlation unchanged.",covariance_cloud)

    def principal_component(ax):
        rng=np.random.default_rng(4)
        cloud=rng.multivariate_normal([0,0],[[5,3],[3,3]],100)
        cloud-=cloud.mean(axis=0)
        _,vectors=np.linalg.eigh(np.cov(cloud.T))
        direction=vectors[:,-1]
        ax.scatter(*cloud.T,s=15,alpha=.45,color=BLUE)
        ax.plot(*np.outer([-5,5],direction).T,color=ORANGE,lw=3,label="First component axis")
        ax.set(xlabel="Asset A centered return (%)",ylabel="Asset B centered return (%)",aspect="equal")
        ax.legend(fontsize=8)
    add("pca-3","A principal component defines an axis","The centered return cloud has a dominant direction. Reversing the loading vector leaves the same geometric axis.",principal_component)

    def tail(ax):
        x=np.linspace(0,7,281); y=np.exp(-x);var=-np.log(.05)
        ax.plot(x,y,color=BLUE)
        ax.fill_between(x,0,y,where=x>=var,color="#b9dcd6")
        ax.axvline(var,ls="--",color=BLUE,label="95% VaR")
        ax.axvline(var+1,ls=":",color=ORANGE,label="Mean beyond VaR")
        ax.set(xlabel="Loss (model units)",ylabel="Probability density")
        ax.legend(fontsize=9)
    add("var-2","A quantile locates the start of the tail","An exponential loss model has 5% of probability beyond its 95% VaR. The conditional mean in that shaded tail lies farther to the right.",tail)

    def efficient(ax):
        w=np.linspace(0,1,161)
        volatility=np.hypot((1-w)*10,w*20)
        ret=4+6*w
        i=np.argmin(volatility)
        ax.plot(volatility[:i+1],ret[:i+1],ls="--",color=ORANGE,label="Dominated branch")
        ax.plot(volatility[i:],ret[i:],color=BLUE,lw=2.5,label="Efficient branch")
        ax.set(xlabel="Annual volatility (%)",ylabel="Expected annual return (%)")
        ax.legend(fontsize=9)
    add("frontier-3","Trace feasible mixtures in risk–return space","For uncorrelated assets with volatilities 10% and 20% and expected returns 4% and 10%, each point is a long-only mixture. Estimation changes move the curve and its minimum-risk weights.",efficient)

    def growth_paths(ax):
        rng=np.random.default_rng(8)
        shocks=rng.normal(0,1,(120,55))
        paths=np.column_stack([np.zeros(120),np.cumsum(shocks,axis=1)])
        for path in paths[:12]:
            ax.plot(path,color=BLUE,alpha=.20,lw=1)
        t=np.arange(paths.shape[1])
        ax.plot(t,2*np.sqrt(t),ls="--",color=ORANGE,label="±2 standard deviations")
        ax.plot(t,-2*np.sqrt(t),ls="--",color=ORANGE)
        ax.set(xlabel="Time step",ylabel="Cumulative increment")
        ax.legend(fontsize=9)
    add("brownian-3","A diffusion has a widening range of outcomes","Simulated independent normal increments spread out with the square root of elapsed time. The paths shown are discrete observations of a continuous-path model; an instantaneous jump needs a different model.",growth_paths)

    def shrink(ax):
        x=np.linspace(0,1,51)
        ax.plot(x,(1-x)*.001+x*.5,lw=2.5,color=BLUE)
        ax.set(xlabel="Weight on identity-like target",ylabel="Smallest eigenvalue")
    add("shrink-3","Lift a small covariance eigenvalue","A sample eigenvalue of 0.001 is blended with 0.5 from a scaled identity target. The inverse is less sensitive as the smallest eigenvalue moves away from zero.",shrink)

    def cal(ax):
        ax.plot([0,1],[0,1],"--",color=ORANGE,label="Perfect calibration")
        ax.plot([.1,.3,.5,.7,.9],[.22,.36,.5,.65,.75],"o-",color=BLUE,label="Observed")
        ax.set(xlabel="Predicted probability of an up move",ylabel="Observed up frequency",xlim=(0,1),ylim=(0,1))
        ax.legend(fontsize=9)
    add("calibration-3","Overconfident forecasts bend toward the center","At 90% forecast probability, only 75% of this illustrative group goes up. Use separate earlier validation forecasts to learn a correction.",cal)

    def volume_schedules(ax):
        x=np.arange(5)
        ax.step(x,[0,25,50,75,100],where="post",lw=2,color=BLUE,label="TWAP")
        ax.step(x,[0,40,55,65,100],where="post",ls="--",lw=2,color=ORANGE,label="Volume-weighted")
        ax.set(xlabel="Equal time intervals completed",ylabel="Parent order completed (%)",xticks=x)
        ax.legend(fontsize=9)
    add("scheduling-2","Two schedules for the same parent order","TWAP allocates the same quantity to each equal interval. A 40/15/10/35 volume profile executes more near the open and close.",volume_schedules)

    def disagreement(ax):
        x=np.arange(24)
        prior=np.linspace(100,102,len(x))
        levels=prior+np.where(x>=11,-9,0)
        ax.plot(x,levels,color=BLUE,lw=2.3,label="Price after impairment")
        ax.plot(x,prior,"--",color=ORANGE,label="Old reference")
        ax.axvline(11,ls=":",color=GREEN)
        ax.set(xlabel="Observation",ylabel="Illustrative price ($)")
        ax.legend(fontsize=8)
    add("reversion-2","A broken reference can look like a bargain","When a persistent value change shifts price to a new level, a model anchored to the old reference can repeatedly forecast a rebound that fails to arrive.",disagreement)
    return examples
