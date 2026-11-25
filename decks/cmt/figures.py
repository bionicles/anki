"""Original, synthetic worked examples and chart-reading prompts for the three CMT levels."""
import numpy as np
from finance_figures import bars, curves, points, sessions, trace


def register(add):
    def line(ids,title,desc,values,unit="Price ($)",**kw):
        add(ids,title,desc,trace(values,unit),**kw)
    def bar(ids,title,desc,labels,values,unit,**kw):
        add(ids,title,desc,bars(labels,values,unit),**kw)

    add("bars-1 bars-2 los-I-bars-4-2 los-I-bars-1-1","Read an OHLC bar",
        "Open 52 (left tick), high 57, low 49, close 54 (right tick). The vertical stroke spans the session's range.",sessions([(52,57,49,54)],ticks=True))
    add("bars-3","One trading session","The bar spans 49 to 57, opens at 52 and closes at 54.",sessions([(52,57,49,54)],ticks=True),cue="What is the high–low range of the illustrated session, in dollars?")
    add("candles-1 los-I-bars-4-3 los-I-bars-5-2","Body and shadows","Open 40 and close 44 bound the hollow body. High 47 and low 38 mark the wick ends.",sessions([(40,47,38,44)]))
    add("candles-2","A hollow candle","The candle opens at 40, closes at 44, and trades from 38 to 47.",sessions([(40,47,38,44)]),cue="How many dollars long is the upper shadow?")
    add("candles-3","A filled candle","The session opens at 52 and closes at 49. The upper body edge is the open.",sessions([(52,54,47,49)]))
    add("candlepatterns-1 los-I-bars-6-2","A session ends where it started","The horizontal body marks an open and close at 50 despite trades between 46 and 54.",sessions([(50,54,46,50)]))
    add("candlepatterns-2","Three successive sessions","The last candle opens at 44, reaches 39, and closes near its high at 45 after a decline.",sessions([(52,53,48,49),(49,50,43,44),(44,45.2,39,45)]),cue="What classic single-candle pattern appears at the end of this decline?")
    add("candlepatterns-3","The preceding trend changes the name","After rising prices, the small real body near the top and long lower shadow form a hanging man.",sessions([(40,44,39,43),(43,48,42,47),(47,48.3,41,48)]))
    line("trend-1","Successive swings","Swing lows are 41 and 46. Swing highs are 50 and 55.",[41,50,46,55],cue="What trend do the successive highs and lows establish?")
    line("trend-2 phases-3","A breakout revisits its old ceiling","The old ceiling at 50 becomes a potential support area when price returns from 54 and rebounds.",[46,50,47,50,48,54,50,55])
    line("trend-3 dow-3 los-I-dow-6-2 los-I-dow-6-3 los-I-interval-1-2","A downswing inside an advance","Each major low is higher, although prices fall between sessions 4 and 6. Trend depends on the observation window.",[40,44,43,50,48,46,52,56])
    line("pattern-1","Identifying a neckline","The head peaks at 64. Joining the two reaction lows of 48 produces the neckline.",[44,56,48,64,48,56,46])
    line("pattern-4","A second peak needs confirmation","Two highs reach 60. The close through the intervening 50 low completes this example.",[46,60,50,60,54,49])
    add("pattern-3","Two nonoverlapping trading ranges","The first session peaks at 45. Every trade in the second takes place at 46 or above.",sessions([(42,45,41,44),(46,49,46,48)]),cue="What directional price gap separates the two sessions?")
    line("phases-1 phases-2 phases-5 phases-6","A schematic Wyckoff cycle","A base precedes markup. A high range can represent distribution before markdown. Phase labels describe the schematic example.",[40,41,39,41,46,52,59,58,60,58,52,46,41])
    add("dow-2 los-I-dow-1-3 los-I-dow-3-2","Compare the two closing highs","Both indexes first peak at 110. Industrials reach 114 on the next advance while transports stop at 108.",
        curves([1,2,3,4],{"Industrials":[100,110,104,114],"Transports":[100,110,103,108]},"Session","Rebased close"))
    add("following-2 los-I-dow-4-1","A high can cross while the close stays below","With resistance at 80, trading at 82 intraday and closing at 79 fails the close-only rule.",sessions([(77,82,76,79)]))
    line("fib-3","Retracing part of a rally","The rally spans 20 points from 40 to 60. Giving back 38.2% subtracts 7.64 from 60.",[40,60,52.36])
    x=np.arange(1,17)
    price=np.array([21,20,19,17,16,15,14,14,15,17,19,21,23,24,26,28])
    def sma(n): return np.r_[[np.nan]*(n-1),np.convolve(price,np.ones(n)/n,"valid")]
    add("averages-5 following-3","Fast and slow averages after a turn","The 3-session average catches the rebound before the 6-session average and crosses above it.",
        curves(x,{"Close":price,"3-session SMA":sma(3),"6-session SMA":sma(6)},"Session","Price ($)"))
    bar("averages-1","Three closing prices","Prices are 8, 10 and 12, with equal weight.",["1","2","3"],[8,10,12],"Close ($)",cue="What is the three-session simple moving average?")
    bar("averages-2","Updating an exponential average","The prior average contributes 75% × 20 = 15. The new close contributes 25% × 24 = 6. Their sum is 21.",["Prior contribution","Latest contribution"],[15,6],"Contribution ($)")
    bar("averages-4","Weights from oldest to newest","The weight total is 6. The newest price accounts for 3/6.",["Oldest","Middle","Newest"],[1,2,3],"Weight")
    bar("breadth-2","Counting issues","310 stocks advance and 270 decline.",["Advances","Declines"],[310,270],"Stocks",cue="What is today's net number of advancing issues?")
    bar("internals-1","Updating cumulative breadth","Net advances are 170 minus 200. Add −30 to the prior A/D line of 1,000.",["Advances","Declines"],[170,200],"Stocks")
    bar("health-2","Count new extremes","80 stocks make new highs and 25 make new lows.",["New highs","New lows"],[80,25],"Stocks",cue="What is the net number of new highs?")
    bar("surveys-2","Bullish, neutral and bearish respondents","Subtracting the bear share from the bull share gives a 20-percentage-point spread.",["Bulls","Neutral","Bears"],[50,20,30],"Respondents (%)")
    bar("positioning-2","Two sides of options volume","600 put contracts and 400 calls trade.",["Puts","Calls"],[600,400],"Contracts",cue="What is the put/call volume ratio?")
    x=np.arange(21)
    add("cycle-1 cycle-2 cycle-3 spectrum-3","Read period, amplitude and phase","A fluctuates 3 units around zero and repeats every 10 sessions. B has the same period but reaches each peak two sessions later.",
        curves(x,{"A":3*np.cos(2*np.pi*x/10),"B":3*np.cos(2*np.pi*(x-2)/10)},"Session","Displacement"))
    add("cycletrend-1 los-II-cycletrend-4-2","A peak between two troughs","Troughs occur at sessions 0 and 20. The peak is six sessions after the first trough.",curves([0,6,20],{"Cycle":[0,6,0]},"Session","Cycle level"))
    bar("spectrum-1","Reading a spectrum","Power is greatest at 0.05 cycles per trading day, corresponding to 1/0.05 = 20 days.",["0.025","0.05","0.10"],[1,6,2],"Relative power")
    add("bands-1 bands-2 bands-3","Changing dispersion around a moving center","The center is 60. With a two-standard-deviation multiplier, increasing SD from 1 to 3 widens the channel from 58–62 to 54–66.",
        curves([1,2,3],{"Upper":[62,64,66],"Middle":[60]*3,"Lower":[58,56,54]},"Rolling SD ($)","Price ($)"))
    bar("bandwidth-1 bandwidth-2","Locate a price within its channel","The width is 20. Price 105 is 15 above the lower band, or three quarters of the width.",["Lower","Middle","Price","Upper"],[90,100,105,110],"Price ($)")
    line("signals-5 divergence-3","Price can rise at a slowing rate","Price rises by 4 and then by 2 over equal intervals. Both gains are positive, but the slope flattens.",[20,24,26])
    add("divergence-1 divergence-2","Compare successive extremes","The first two highs show a higher price high and lower RSI high. The last two lows show a lower price low and higher RSI low.",
        curves(range(1,6),{"Price ($)":[100,110,96,115,92],"RSI (index)":[50,72,30,64,38]},"Session","Price ($) or RSI points"))
    bar("signals-2 signals-3","Subtract one line from another","Fast EMA 52 minus slow EMA 49 yields MACD 3. Subtract its signal line 4 for a histogram value of −1.",["Fast EMA","Slow EMA","MACD","Signal","Histogram"],[52,49,3,4,-1],"Price units")
    bar("vwap-1 vwap-3","Trade size sets the weight","Three quarters of the 400 shares trade at 12, one quarter at 10. The weighted price is 11.50.",["At $10","At $12"],[100,300],"Shares")
    add("avwap-1 anchors-3 avwap-3","Start the average at its anchor","With one equal-size trade per session, the full-window average uses every dot. The second average begins at the day-3 event.",
        curves([1,2,3,4,5],{"Trade":[10,10,16,18,17],"From day 1":[10,10,12,13.5,14.2],"From day 3":[np.nan,np.nan,16,17,17]},"Session","Price ($)"))
    line("targets-1","Project the rectangle height","Range boundaries 44 and 50 are 6 apart. Adding 6 to the breakout level gives a conventional target of 56.",[44,50,44,50,46,50,52,56])
    line("targets-2","Measure the head above the neckline","A head at 72 is 8 above a neckline at 64. Projecting 8 below the neckline gives 56.",[62,68,64,72,64,68,63,56])
    bar("range-1","Measure a gap against the preceding close","Yesterday closed at 100. Today trades only between 90 and 94. The previous close to today's low spans 10.",["Prev. close","High","Low"],[100,94,90],"Price ($)")
    add("relative-1 relative-2","Relative strength in a falling market","Both start at 100. The stock ends at 95 and the benchmark at 90. The price ratio rises from 1 to about 1.056.",
        curves([1,2],{"Stock":[100,95],"Benchmark":[100,90]},"Observation","Rebased price"))
    add("term-1 term-2","Compare adjacent VIX futures maturities","Curve A rises from 18 to 20. Curve B falls from 30 to 25. Read left to right across expiries.",
        curves([1,2],{"Curve A":[18,20],"Curve B":[30,25]},"Contract month","VIX futures price"))
    bar("debt-2","Maturity-matched yields","The corporate yield is 5.1% and Treasury yield is 3.9%.",["Corporate","Treasury"],[5.1,3.9],"Yield (%)",cue="What is the corporate yield spread in basis points?")
    bar("premium-1","Implied versus subsequent realized volatility","Implied volatility of 22% exceeds subsequently realized volatility of 16% by six percentage points.",["Implied","Realized"],[22,16],"Annualized volatility (%)")
    x=np.arange(-3.5,3.51,.025)
    def normal(ax):
        y=np.exp(-x*x/2)/np.sqrt(2*np.pi)
        ax.plot(x,y,color="#135f76"); ax.fill_between(x,0,y,where=abs(x)<=2,alpha=.32)
        ax.set(xlabel="Standard deviations from mean",ylabel="Probability density")
    add("prob-1 los-I-prob-4-1 los-I-prob-4-2 los-I-prob-5-2 los-I-prob-5-3","Area under a normal curve","The shaded middle from −2 to +2 standard deviations covers about 95.45%; the remaining area splits equally between the tails.",normal)
    add("regress-3","An exact nonlinear relationship","The points lie on y=x². Symmetry makes their linear correlation zero despite the exact relationship.",points([-2,-1,0,1,2],[4,1,0,1,4],"x","y"))
    add("regress-2 los-I-regress-7-1 los-I-regress-8-1","Reading a fitted line","The line has intercept 1 and slope 0.5. At x=4 its fitted y is 3.",curves(range(6),{"Fit":1+.5*np.arange(6)},"Predictor x","Fitted y"))
    line("stats-3 stats-5 los-I-stats-6-2","Compound successive returns","A 25% gain lifts 100 to 125. A 20% decline then takes 125 back to 100.",[100,125,100],"Wealth")
    bar("expectancy-1","Probability-weighted trade outcomes","A 40% chance of +3R contributes +1.2R; a 60% chance of −1R contributes −0.6R. Gross expectancy is +0.6R.",["Wins","Losses","Expected"],[1.2,-.6,.6],"Risk units per trade")
    bar("expectancy-2","A high win rate can coexist with losses","An 80% chance of +1R contributes +0.8R. A 20% chance of −5R contributes −1R. Net of the two outcomes, expectancy is −0.2R before costs.",["Wins","Losses","Expected"],[.8,-1,-.2],"Risk units per trade")
    bar("implementation-1 backtest-6","Crossing from gross to net","Costs of 0.22R consume more than a gross edge of 0.18R, leaving −0.04R per trade.",["Gross","Cost impact","Net"],[.18,-.22,-.04],"Risk units per trade")
    add("counter-2 pfplan-3","Position size falls as risk per share rises","Under a $300 risk budget, doubling risk per share from $1.50 to $3 halves the share count from 200 to 100.",
        curves([1,1.5,2,2.5,3],{"Shares":300/np.array([1,1.5,2,2.5,3])},"Risk per share ($)","Shares"))
    bar("tactical-3","Restore the policy mix","At fixed total value, sell ten percentage points of equities and buy bonds to return to a 60/40 target.",["Equity now","Equity target","Bonds now","Bond target"],[70,60,30,40],"Weight (%)")
    bar("rank-4","An active weight is a difference","The sector is 14% of the portfolio versus 10% of the benchmark.",["Portfolio","Benchmark"],[14,10],"Sector weight (%)",cue="What is this sector's active weight in percentage points?")
    bar("pfplan-1","Distances from a long entry","The stop is 3 below entry and the target is 9 above. The planned reward/risk ratio is 9/3.",["Stop distance","Target distance"],[3,9],"Dollars per share")
    bar("portfolio-1","Weights proportional to inverse volatility","Volatilities of 10% and 20% imply inverse weights in a 2:1 ratio. The first asset receives two thirds.",["Asset A","Asset B"],[200/3,100/3],"Portfolio weight (%)")
    x=np.arange(50,151)
    add("premium-3","Short straddle at expiration","Selling a call and put struck at 100 for total premium 10 yields 10 minus the absolute distance from 100. Large moves in either direction create losses.",
        curves(x,{"Profit":10-abs(x-100)},"Underlying price ($)","Profit per share ($)"))

    def pf(ax):
        for i,(mark,levels) in enumerate([("X",[46,48,50,52]),("O",[50,48,46]),("X",[48,50,52,54])]):
            for level in levels: ax.text(i,level,mark,ha="center",va="center",fontsize=16,weight="bold")
        ax.set(xlim=(-.5,2.5),ylim=(44,56),xticks=[0,1,2],xticklabels=["1","2","3"],yticks=range(46,55,2),xlabel="Reversal column",ylabel="Box price ($)")
    add("pf-1 pf-2 pftarget-1","Read a point-and-figure reversal","Each box is $2. X marks rising prices; O marks falling prices. The three-box reversal from 52 reaches 46. The final X exceeds the previous X high.",pf)
    def rrg(ax):
        ax.axhline(100,color="#66747a"); ax.axvline(100,color="#66747a")
        for x,y,t in [(96,104,"Improving"),(104,104,"Leading"),(104,96,"Weakening"),(96,96,"Lagging")]:
            ax.text(x,y,t,ha="center",fontsize=10)
        ax.plot([97,98,101,104],[98,102,103,102],"o-",color="#135f76")
        ax.annotate("End",(104,102),xytext=(4,-12),textcoords="offset points")
        ax.set(xlim=(92,108),ylim=(92,108),xlabel="RS-Ratio",ylabel="RS-Momentum")
    add("rrg-1 rrg-2 rrg-3 rrg-4 rotation-3 rotation-4","Follow a relative rotation trail","The trail crosses above 100 vertically before crossing 100 horizontally, moving from lagging to improving to leading.",rrg)
    def prof(ax):
        ax.barh([48,49,50,51,52],[1,3,5,2,1],color="#135f76")
        ax.set(yticks=range(48,53),xlabel="Time brackets visiting this price",ylabel="Price ($)")
    add("profile-1 profile-2 profile-4","Turn the price axis upright","Each row counts time brackets visiting that price. The $50 row has five, more than any other row. It is the TPO point of control.",prof)
    add("reversal-1 reversal-2","Two sessions after a downswing","The last session opens below the prior down body's close, then closes above its open. The second body engulfs the first.",sessions([(55,56,50,51),(51,52,48,49),(48,54,47,53)]))
    add("reversal-3","One candle after an advance","Open and close both sit at 49. The high reaches 55, leaving a long upper shadow.",sessions([(49,55,49,49)]),cue="What type of doji has this arrangement of body and shadow?")
    add("confirm-1","A three-session reversal formation","A long down body is followed by a small star and an up body that closes deep inside the first. The formation is a morning star.",sessions([(55,56,48,49),(47,48,46,47.5),(48,55,47.8,54)]))
    add("confirm-3","Read the second session's close","After the hammer, the next high clears 52 but the close at 51 remains below the hammer high of 52.",sessions([(50,52,44,51.5),(51.5,54,50,51)]))
    add("options-4 options-7 term-3","Put payoff before premium","At expiry a put struck at 50 pays max(50 − stock price, 0). A finish at 43 pays 7 per share before the premium.",curves(np.arange(31,71),{"Put":np.maximum(50-np.arange(31,71),0)},"Underlying at expiry ($)","Payoff per share ($)"))
    t=np.arange(5)
    def scales(ax):
        from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
        ax.set_yscale("log");ax.plot(t,10*2**t,"o-",color="#135f76")
        ax.yaxis.set_major_locator(FixedLocator([10,20,40,80,160]))
        ax.yaxis.set_major_formatter(FixedFormatter(["10","20","40","80","160"]))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.set(xticks=t,xlabel="Period",ylabel="Price ($, log scale)")
    add("scale-1 scale-3 los-I-scale-2-1 los-I-scale-2-2","Each doubling travels the same height","A log axis gives 10→20, 20→40 and 40→80 equal height because all have the same percentage gain.",scales)
    line("scale-2 los-I-scale-2-3","Equal dollar changes on a linear scale","A $2 increase from $10 to $12 has the same height as $16 to $18 on a linear chart.",[10,12,14,16,18])
    bar("momentum-5","Locate the close within the range","Low 40, high 60, close 55. The close is 15 of the 20 range points above the low, or 75%.",["Low","Close","High"],[40,55,60],"Price ($)")
    x=np.arange(1,13)
    changes=np.array([0,1,-1,2,0,3,-2,1,-1,0,2,-1])
    totals=np.cumsum(np.sign(changes)*np.array([8,4,6,5,9,4,3,6,3,7,5,4]))
    add("momentum-4 momentum-6","Add or subtract volume by the close direction","In sessions 5 and 10 the close is unchanged, so the running total stays flat; an up close adds that day's volume.",
        curves(x,{"On-balance volume":totals},"Session","Cumulative signed volume (thousands)"))
    add("debt-3","A yield curve on one date","Each observation is for comparable credit quality on the same date. The horizontal axis changes maturity.",curves([1,2,5,10],{"Yield":[3,3.2,3.4,3.5]},"Maturity (years)","Annual yield (%)"))
    x=np.linspace(1,9,65)
    add("debt-1","Discounting a fixed bond payment","A five-year zero repays 100. Higher required yields discount that fixed payment to a lower current price.",curves(x,{"Price":100/(1+x/100)**5},"Annual yield (%)","Price per 100 face"))
    line("metrics-2","Peak to trough","The equity curve reaches 125 and then falls to 100.",[110,118,125,115,100,108],"Equity index",cue="What is the magnitude of the illustrated peak-to-trough drawdown as a percentage of the peak?")
    line("risk-7","Recovery starts from a smaller base","Falling from 100 to 75 loses 25%. Recovering the 25 points from 75 requires a gain of one third.",[100,75,100],"Equity index")
    bar("trade-1","A long trade plan","Long entry 51, protective exit 49, target 59. No costs or gaps.",["Exit","Entry","Target"],[49,51,59],"Price ($)",cue="For this long trade, what is planned reward divided by planned risk?")
    bar("trade-3 los-III-trade-1-3 los-III-trade-2-1","For a short, the stop is above entry","For example, short at 78, cover at 70 for a gain of 8, or stop at 82 for a loss of 4. Reward/risk is 2.",["Target","Entry","Stop"],[70,78,82],"Price ($)")
    bar("metrics-1","Gross profits and gross losses","Winning trades generate 900, losing trades cost 600. Profit factor divides the first magnitude by the second.",["Profits","Loss magnitude"],[900,600],"Dollars")
    add("risk-5 los-III-risk-6-1 los-III-risk-6-2","Market moves and leveraged equity","With fixed debt and before costs, 1.5× and 2× gross long exposure scale the equity response proportionally.",curves([-5,0,5],{"Unlevered":[-5,0,5],"1.5×":[-7.5,0,7.5],"2×":[-10,0,10]},"Asset return (%)","Equity return (%)"))
    x=np.linspace(50,200,151)
    add("los-III-risk-1-1 los-III-risk-2-1 los-III-risk-2-2","Diminishing marginal utility","A log utility curve rises throughout, but equal additional dollars produce smaller gains in utility at higher wealth.",curves(x,{"Utility":np.log(x)},"Wealth ($)","Log utility"))
    x=np.linspace(0,6,241)
    def tail(ax):
        ax.plot(x,np.exp(-x),color="#135f76")
        v=-np.log(.05)
        ax.fill_between(x,0,np.exp(-x),where=x>=v,alpha=.35)
        ax.axvline(v,ls="--",label="95% VaR");ax.axvline(v+1,ls=":",color="#aa461c",label="Expected shortfall")
        ax.legend(fontsize=8);ax.set(xlabel="Loss (model units)",ylabel="Probability density")
    add("risk-1 risk-2 los-III-risk-5-1","A tail threshold and a tail average","In an exponential loss model the last 5% lies beyond the VaR line. Expected shortfall is the mean within that tail and lies farther right.",tail)
    x=np.linspace(-1,1,65)
    add("risk-6 tactical-2 los-III-risk-9-2 los-III-risk-10-3 los-III-portfolio-4-3","Correlation changes portfolio volatility","A 50/50 portfolio of two assets with 10% volatility has zero volatility at correlation −1 in this idealized model and 10% at +1.",curves(x,{"Portfolio":10*np.sqrt((1+x)/2)},"Return correlation","Portfolio volatility (%)"))
    bar("portfolio-2 los-III-tactical-3-1 los-III-risk-7-1","Hold risk fixed by changing exposure","For an 8% risk target, annualized estimates of 8%, 16% and 32% imply exposures of 100%, 50% and 25% under linear scaling.",["8% vol","16% vol","32% vol"],[100,50,25],"Exposure (%)")
    bar("los-III-tactical-2-2 los-III-tactical-2-4","Same trend slope, different fit","At a fixed 20% annualized slope, multiplying by R² of 0.80 and 0.40 gives scores of 16% and 8%. A noisy trend can score much lower.",["R² = .80","R² = .40"],[16,8],"Illustrative momentum score (%)")
    bar("backtest-7 los-III-backtest-1-1","Overlapping labels reuse observations","Window A uses days 1–10. Window B uses days 2–11. Nine of the ten daily return intervals are counted twice.",["Only A","Shared","Only B"],[1,9,1],"Daily return intervals")
    add("backtest-4 los-III-backtest-3-1 los-III-backtest-3-2","Log returns accumulate by addition","Successive log returns of +0.08 and −0.03 move cumulative log return from 0 to 0.08 to 0.05.",curves([0,1,2],{"Cumulative":[0,.08,.05]},"Period","Cumulative log return"))
    def sizes(ax):
        for left,width,label in [(0,2,"Train"),(2,1,"Select"),(3,1,"Test")]:
            ax.barh(0,width,left=left,height=.35,edgecolor="#263d44",color=["#dceceb","#c4d8dc","#e7d0bc"][[0,2,3].index(left)])
            ax.text(left+width/2,0,label,ha="center",va="center")
        ax.set(xlim=(0,4),xticks=range(5),yticks=[],xlabel="Chronological order")
    add("backtest-3 seasontest-3 los-III-tactical-3-3","Hold out later observations","Fit on early observations, select the rule in a later window, then assess it on an untouched final period.",sizes)
    x=np.linspace(0,30,61)
    add("tail-5 iv-5","Scale volatility by the square root of time","With independent equal-variance increments, doubling horizon multiplies volatility by √2. A quarter-year at 16% annual volatility gives 8%.",curves(x,{"Volatility":16*np.sqrt(x/12)},"Horizon (months)","Standard deviation (%)"))

    line("los-I-trend-1-2","Compare corresponding swing points","Swing highs fall from 75 to 70 while lows fall from 66 to 60.",[75,66,70,60],cue="Which trend do these successive swing highs and lows show?")
    line("los-I-trend-1-3 counter-1","Repeated tests of a range","Price repeatedly turns near 40 and 50. A sustained break below the floor would undermine the range-fading premise.",[40,49,41,50,40,49,41])
    line("los-I-pattern-1-2","A double bottom and its trigger","Two troughs form around 40. A later move above the intervening peak at 48 confirms this textbook pattern.",[55,46,40,48,41,45,50])
    line("los-II-waves-3-2 waves-1 los-II-waves-1-3","A schematic five-wave advance","Counting from the starting low, legs 2 and 4 are pullbacks. Leg 3 is longer than either 1 or 5 in this example. The idealized next phase is corrective.",[40,50,45,63,55,66])
    line("waves-2","An invalid second wave","An initial move from 40 to 50 followed by a decline to 38 passes below the origin of wave 1. The proposed upward impulse count fails.",[40,50,38])
    line("waves-3","An overlapping fourth wave","The first leg reaches 50. The fourth leg falls to 48, entering wave 1 territory and invalidating this standard impulse interpretation.",[40,50,45,63,48])
    line("correction-1 los-II-waves-5-3","Count the legs inside a zigzag","In this schematic downward correction, A falls in five small legs, B rises in three, and C falls in five. The major turns are at sessions 6 and 9.",[70,65,67,58,62,55,60,57,63,57,59,51,54,46])
    line("los-II-waves-5-2","Contracting corrective swings","Five alternating legs shrink into a narrower range. Elliott labels these corrective triangle legs A through E.",[65,45,60,49,57,52])
    x=np.arange(1,7)
    for keys,title,vol,price,desc in [
            ("pv-1 participation-1 los-II-pv-1-1","Price and participation on advances",[10,15,8,18,9,22],[100,104,102,107,105,111],"Rising price legs attract more volume than the intervening pullbacks."),
            ("pv-2 los-II-pv-1-3","Weakening participation on an advance",[22,20,19,16,14,10],[100,103,104,108,109,112],"The close rises while volume contracts, a weak-demand reading in the four-phase framework."),
            ("pv-3 los-II-pv-1-4","Expanding participation on a decline",[10,12,14,17,19,22],[112,109,108,104,103,100],"Falling price and expanding volume are consistent with the strong-supply phase."),
            ("los-II-pv-1-2","Contracting participation on a decline",[22,20,18,15,13,10],[112,109,108,104,103,100],"Price falls with diminishing volume, the weak-supply phase in this framework.")]:
        def draw(ax,vol=vol,price=price):
            ax.plot(x,price,"o-",color="#135f76");ax.set(xlabel="Session",ylabel="Close ($)",xticks=x)
            ax2=ax.twinx()
            ax2.bar(x,vol,width=.45,color="#be8051",alpha=.30);ax2.set(ylabel="Volume (000 shares)",ylim=(0,34))
        add(keys,title,desc,draw)
    x=np.arange(6)
    add("breadth-1 breadth-3 health-1 internals-3 los-III-portfolio-3-2","Breadth can diverge from the index","Both series are rebased to 100. A cap-weighted index makes a second higher high but the breadth line's second high is lower, indicating narrowing participation.",
        curves(x,{"Index":[100,104,110,106,109,113],"A/D line":[100,106,111,104,107,108]},"Session","Rebased level"))
    bar("rank-5","Rank can be positive while return is negative","Among three falling sectors, −2% ranks first because the other losses are larger. Rank compares peers; absolute return retains its sign.",["Sector A","Sector B","Sector C"],[-2,-5,-8],"Return (%)")
    add("multiple-2 los-III-crypto-8-2","Start competing price series at the same value","Rebasing both assets to 100 isolates cumulative percentage change. A ends at 92 versus 85 for B, so A outperforms despite a loss.",
        curves([0,1,2,3],{"A":[100,97,94,92],"B":[100,95,90,85]},"Period","Rebased value"))
    add("bandplan-1","Price can walk an upper band","A rising close stays near its rising upper band for several sessions. A band touch by itself provides little evidence that the advance has ended.",
        curves(range(1,8),{"Close":[49,51,53,55,57,59,61],"Upper":[50,52,54,56,58,60,62],"Middle":[46,47,49,51,53,55,57]},"Session","Price ($)"))
    x=np.arange(1,9)
    add("bandwidth-3","A squeeze before a directional move","As the upper and lower bands converge toward the middle, BandWidth contracts. The direction of the next move is still unknown.",
        curves(x,{"Upper":[112,110,108,106,104,103,102,101],"Middle":[100]*8,"Lower":[88,90,92,94,96,97,98,99]},"Session","Price ($)"))
    bar("los-III-bandplan-4-1 bandplan-3","Two indicators can repeat one signal","Example signals A and B classify all four sessions identically. Counting both votes as independent overstates the amount of evidence.",["Agree","Disagree"],[4,0],"Sessions")
    add("cycletrend-2 cycletrend-3","A centered window reaches into the future","A Wednesday-centered five-session average uses Monday through Friday. Wednesday's value cannot be computed until Friday's close.",
        bars(["Mon","Tue","Wed","Thu","Fri"],[1,1,1,1,1],"Included observations"))
    bar("los-III-tactical-1-2","Read the two Treasury sleeves","The stated static example allocates 15% to intermediate Treasuries and 40% to long Treasuries. These are separate parts of total portfolio capital.",["Intermediate","Long"],[15,40],"Portfolio weight (%)")
    bar("portfolio-3","Apply a portfolio weight cap","A 22% signal exceeds a 15% cap. The maximum permitted sector weight is 15%.",["Signal","Cap","Permitted"],[22,15,15],"Weight (%)")


# Each previously shipped market chart illustrates the named cards on reveal.
    # Readings progress from recognizing a shape to applying a trading rule.
    add("multiple-1","Prices during the current trading week",
        "Monday, Tuesday and Wednesday close at 47, 49 and 51. Resistance is 50. Thursday and Friday have yet to trade.",
        curves([1,2,3,4,5],{"Close":[47,49,51,np.nan,np.nan],"Resistance":[50]*5},"Weekday (1 = Monday, 5 = Friday)","Price ($)"),
        cue="It is Wednesday. This breakout rule uses weekly closes. When can this week's move through resistance first be confirmed?")
    line("los-I-phases-4-2","A move through an old ceiling",
         "The previous peak is 60. Price closes at 64, returns to 60, then rises to 65.",
         [55,60,56,59,57,64,60,65],cue="What is the upward-breakout-specific term for the return to the old ceiling?")
    line("los-I-phases-4-1","A move through an old floor",
         "The price twice touches 40, falls to 36, then returns to 40 from below.",
         [45,40,43,40,42,36,40],cue="What is the classical downside-breakout term for the final move back to former support?")
    add("los-I-screening-4-2","Stock and index from a common starting value",
        "Both start at 100. The stock ends at 95 and the index at 85.",
        curves([1,2,3],{"Stock":[100,97,95],"Index":[100,91,85]},"Session","Rebased price"),
        cue="Both prices fell. Can this stock's price relative rise before an absolute breakout? Explain from the paths.")
    add("los-III-rotation-4-3","Three holdings and their common benchmark",
        "The benchmark falls from 100 to 80. Holdings A, B and C finish at 96, 92 and 88.",
        curves([1,2,3],{"Benchmark":[100,90,80],"A":[100,98,96],"B":[100,97,92],"C":[100,94,88]},"Session","Rebased price"),
        cue="Every holding beats the benchmark. What portfolio risk does their relative strength leave in place?")
    add("los-I-following-4-2","Price and two trailing averages",
        "The latest price is 52. The fast average has risen to 49 and the slow average is 50.",
        curves([1,2,3],{"Price":[46,49,52],"Fast":[47,48,49],"Slow":[51,50.5,50]},"Session","Price ($)"),
        cue="Price finishes above both averages. What further event would trigger a bullish two-average crossover?")
    line("los-I-range-3-2","Width of the envelope before the next trade",
         "BandWidth falls from 18% to 4%. No subsequent prices are shown.",
         [18,15,13,10,7,4],"BandWidth (%)",cue="The bands have compressed. What about the next breakout remains unknown?")
    line("los-II-bandwidth-5-1","A history of BandWidth readings",
         "Width rises from its recent range near 8% to a 26% peak, then falls back.",
         [8,9,7,8,14,26,16,10],"BandWidth (%)",cue="In Bollinger's terminology, what is the prominent peak in this series called?")
    add("los-II-signals-4-1","Two indicator lines at successive closes",
        "Yesterday MACD was 0.6 and its signal was 1.0. Today MACD is 1.2 and its signal is 1.1.",
        curves([1,2],{"MACD":[.6,1.2],"Signal":[1,1.1]},"Close (1 = yesterday)","Indicator value"),
        cue="The rule buys on the first MACD cross above its signal. Which signal fires at the second close?")
    bar("los-III-crypto-8-1","One token index closes higher","Of 100 constituents, 25 advance and 75 decline.",
        ["Advances","Declines"],[25,75],"Constituents",cue="The capitalization-weighted index rose. What does the constituent breadth say about the advance?")
    bar("los-III-rank-5-2","Equal-weight sector ranks before a rebalance",
        "A is rank one both months. B falls from rank two to three and C rises from three to two.",
        ["A before","A now","B before","B now","C before","C now"],[1,1,2,3,3,2],"Sector rank (1 = best)",
        cue="Hold the top two equally. With unchanged prices before this rebalance, what fraction of portfolio value is sold?")
    add("los-III-tactical-1-3","Two sleeves drift from their policy weights",
        "The fixed target is 50% per sleeve. After market moves, A is 60% and B is 40%.",
        curves([0,1],{"A":[50,60],"B":[50,40],"Target per sleeve":[50,50]},"Observation","Portfolio weight (%)"),
        cue="A fixed-weight policy is rebalanced now. What trade does it require in sleeve B?")
    add("los-I-debt-6-1","Treasuries observed on one date","Two-year yield is 5% and ten-year yield is 4%.",
        curves([2,10],{"Yield":[5,4]},"Years to maturity","Annual yield (%)"),
        cue="How would you describe the slope of this Treasury curve segment?")
    line("los-II-signals-2-2","Successive oscillator peaks","Peaks decline from 72 to 66 to 60, then rise to 67.",
         [72,66,60,67],"Peak reading",cue="What feature of momentum changes at the fourth peak?")
    add("los-III-rotation-3-3 rotation-2","One stock relative to two benchmarks",
        "With all starting at 100, the stock ends at 108, its sector at 115 and the market at 103. It leads the market while trailing its sector.",
        curves([1,2,3],{"Stock":[100,104,108],"Sector":[100,108,115],"Market":[100,101,103]},"Observation","Rebased price"))
    line("los-II-divergence-5-3","Price can continue up after momentum slows",
         "The sequence still makes higher highs. Gains per interval shrink from 8 to 6 to 4 to 2, without a price reversal.",
         [100,108,114,118,120])
    line("los-I-bands-1-1 los-III-bandplan-1-1","Changing width around a moving reference",
         "The distance from the average to a volatility-based band can increase as observed variation rises.",
         [1,1.2,1.1,2.4,3.6,3.1],"Band half-width ($)")
    add("los-I-momentum-2-2","A trailing average after a price turn",
        "After a flat period, price rises. The four-close average responds gradually as the older prices leave its window.",
        curves(range(1,9),{"Price":[10,10,10,10,12,14,16,18],"4-close SMA":[np.nan]*3+[10,10.5,11.5,13,15]},"Session","Price ($)"))

WORKED_CHARTS = [
    ("cmt_study_01.png","following-1 los-I-trend-1-1","Read the sequence of swing lows under the rising price. Successively higher reaction lows can anchor an uptrend support line."),
    ("cmt_study_03.png","targets-5","In this rectangle example, measure the height first and project it from the breakout in its direction. The triangle in the question uses its widest span and a downside projection."),
    ("cmt_study_06.png","trade-2","The price breaks above resistance and then closes back inside. Under this particular exit rule the return inside invalidates the breakout."),
    ("cmt_study_11.png","rank-1","Both series begin at 100, so the higher endpoint has the higher cumulative return. Here asset B leads. Apply the same comparison to the assets in the question."),
    ("cmt_study_12.png","los-I-bands-2-1 los-III-bandplan-2-3","Price repeatedly closes near its rising upper band. This band walk illustrates why touching an outer band can persist; in a decline look for an actual change in the swing structure."),
    ("cmt_study_13.png","los-I-volume-2-1","Price reaches new highs while volume shrinks. Fewer shares change hands on the later highs."),
    ("cmt_study_25.png","los-II-vwap-7-1","The volume profile is high near the open and close and lower around midday. A volume-proportional schedule would allocate more trading to busier intervals."),
    ("cmt_study_28.png","bandplan-2","The second trough is lower in price but higher on the %b panel. Relative to its bands, price held up better at the second low."),
    ("cmt_study_39.png","targets-3","The dotted threshold is 3% above resistance. Compare closing prices with that threshold, rather than treating any move over resistance as sufficient."),
    ("cmt_study_40.png","targets-4 trade-4","This downside example subtracts an ATR buffer from support. For an upside rule, add the specified multiple of ATR to resistance."),
    ("cmt_study_43.png","relative-3 los-I-screening-3-1 los-I-screening-3-2 los-III-portfolio-2-4","Compare both rebased series through the selloff. Asset A loses less and therefore shows relative resilience even as its own price falls."),
    ("cmt_study_45.png","rotation-1","Both sector-to-market ratios use the same market benchmark. The higher final ratio after rebasing indicates stronger relative performance over the window."),
    ("cmt_study_46.png","cycle-4 los-II-cycletrend-4-1 los-II-cycletrend-4-3","Between two consecutive troughs, compare the peak date with the midpoint. This chart peaks early (left translation); a late peak reverses that timing."),
    ("cmt_study_51.png","vol-1 vol-3 los-III-backtest-2-3","The late observations swing farther from zero and large moves cluster. A constant-variance model obscures the change in the size of returns."),
    ("cmt_study_54.png","spectrum-2","The strongest spectral band moves from a four-session to a sixteen-session period. A spectrogram retains when the dominant period changes."),
    ("cmt_study_63.png","los-II-waves-1-2 los-II-waves-4-1","The extended third wave contains smaller marked swings. Wave degree distinguishes that internal sequence from the larger impulse."),
    ("cmt_study_64.png","cycle-6 timing-2","The schematic cycles share a trough again after 40 sessions. When one period is a whole-number multiple of the other, recurring phase alignments become possible."),
]
