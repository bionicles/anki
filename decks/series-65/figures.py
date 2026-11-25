"""Synthetic Series 65 examples. Each ID refers to an existing graded card."""
import numpy as np
from finance_figures import bars, curves, points


def register(add):
    def bar(ids,title,desc,labels,values,unit,**kw):
        add(ids,title,desc,bars(labels,values,unit),**kw)
    def plot(ids,title,desc,x,series,xlabel,ylabel,**kw):
        add(ids,title,desc,curves(x,series,xlabel,ylabel),**kw)

    plot("I-001 I-004","Reading the business cycle","Activity peaks at 108, falls to 97, then rises to 102. Expansion resumes at the trough before output regains its old peak.",range(1,7),{"Activity":[100,104,108,101,97,102]},"Quarter","Output index")
    plot("I-023","Yields across maturities","The annual yields on 1-, 5- and 10-year maturities are 5%, 4% and 3%.",[1,5,10],{"Yield":[5,4,3]},"Maturity (years)","Yield (%)",cue="What relationship between the short and long maturities makes this yield curve inverted?")
    plot("I-024 II-071 II-072","Read the vertical gap at equal maturity","In this example the corporate yield rises and the comparable Treasury yield falls. The spread widens from 1 to 2.5 percentage points.",[1,2],{"Corporate":[5,6],"Treasury":[4,3.5]},"Observation","10-year yield (%)")
    plot("I-101","A steepening yield curve","With short yields fixed, a rise in long yields increases the long-minus-short spread.",[1,5,10],{"Before":[3,3.3,3.5],"After":[3,3.8,4.6]},"Maturity (years)","Yield (%)")
    plot("I-131","Match changes in two yields","The 10-year corporate moves 6.35% to 6.65%. The 10-year Treasury moves 4.15% to 4.25%.",[1,2],{"Corporate":[6.35,6.65],"Treasury":[4.15,4.25]},"Observation","Yield (%)",cue="By how many basis points does the corporate spread widen?")
    bar("I-132","Expenditure components","Add the first four categories and subtract imports. 620 + 170 + 220 + 90 − 140 = 960.",["Consumption","Investment","Government","Exports","Imports"],[620,170,220,90,-140],"Contribution ($ billions)")
    rates=np.linspace(0,.20,101)
    plot("I-060","Find the discount rate where NPV crosses zero","An outlay of 100 followed by 110 in one year has NPV 110/(1+r) − 100. It crosses zero at 10%.",100*rates,{"NPV":110/(1+rates)-100},"Discount rate (%)","Net present value ($)")
    rates=np.linspace(0,.32,129)
    plot("I-059","Two sign changes can yield two IRRs","Cash flows −100, +230, −132 at years 0, 1, 2 give NPV zero at both 10% and 20%.",100*rates,{"NPV":-100+230/(1+rates)-132/(1+rates)**2},"Discount rate (%)","Net present value ($)")
    bar("I-150 I-151","Place each machine cash flow in time","The outlay occurs now. The two inflows are each discounted to today before comparing them with the outlay.",["Now","Year 1","Year 2"],[-10000,6000,6000],"Cash flow ($)")
    t=np.arange(4)
    plot("I-062 I-153 I-154","Interest can earn more interest","Starting with $12,000 at 4%, compounding for three years gives $13,498.37. Simple interest gives $13,440.",t,{"Compound":12000*1.04**t,"Simple":12000*(1+.04*t)},"Years","Balance ($)")
    bar("I-063 I-157 I-158","How long does each deposit earn interest?","At year three, deposits made at each year's start have grown for 3, 2 and 1 years. Year-end deposits grow for 2, 1 and 0.",["Start 1","Start 2","Start 3","End 1","End 2","End 3"],[3,2,1,2,1,0],"Years of growth")
    bar("I-065 I-159","A sample of annual returns","The five observations are −6%, 2%, 4%, 4% and 11%. The repeated value is 4%; the extremes are 17 points apart.",list("ABCDE"),[-6,2,4,4,11],"Return (%)")
    bar("I-066 I-161","Distance from the mean","Equal probabilities at 2% and 10% put the mean at 6%. Both outcomes are four percentage points from it.",["Low","Mean","High"],[2,6,10],"Return (%)")
    add("I-067","Zero correlation can hide a pattern","At x = −2, −1, 0, 1, 2 the plotted y values are 4, 1, 0, 1, 4. The quadratic relationship has zero linear correlation.",points([-2,-1,0,1,2],[4,1,0,1,4],"Return A (%)","Return B (%)"))
    bar("I-070 I-071 I-072 I-073","Inventory changes the liquidity picture","An example firm has 30 in quick assets and 90 in inventory against 80 of current liabilities. Current ratio = 120/80; quick ratio = 30/80.",["Quick assets","Inventory","Current liabilities"],[30,90,80],"Amount ($000)")
    bar("I-077","Hold price fixed while EPS doubles","At a $40 price, EPS of $2 means 20 times earnings. At $4 EPS the multiple falls to 10.",["EPS = $2","EPS = $4"],[20,10],"Price / earnings")
    n=np.arange(1,51)
    plot("I-080 II-140","What diversification can reduce","Toy model: independent company shocks have 20% volatility and all holdings share a 12% market shock. Equal weighting diversifies the independent part. The shared risk persists.",n,{"Portfolio":np.sqrt(12**2+20**2/n),"Shared risk":[12]*len(n)},"Equal-weight holdings","Volatility (%)")
    y=np.linspace(.01,.10,91)
    plot("I-081 II-051 II-069","Price a bond at different market yields","A 5-year $1,000 bond pays $50 annually. Discounting the same payments more steeply gives a lower price. At 5% the bond is at par.",100*y,{"Bond":sum(50/(1+y)**i for i in range(1,6))+1000/(1+y)**5,"Par":np.full(len(y),1000)},"Market yield (%)","Price ($)")
    bar("II-047 II-050","A zero has a single payment date","This eight-year zero pays no interim coupons. Its entire redemption occurs in year eight, so its Macaulay duration is eight years.",range(1,9),[0]*7+[1000],"Cash flow ($)")
    bar("II-049 II-246","Macaulay duration weights time by PV","Year one accounts for $50 of $1,000 total present value. Year two accounts for $950. Weighted time is 0.05×1 + 0.95×2 = 1.95 years.",["Year 1","Year 2"],[50,950],"Present value ($)")
    t=np.arange(4)
    plot("II-052 II-244 II-245","A zero approaches redemption value","At a fixed 4% rate, $5,000 discounted over three remaining years increases in price as the redemption date draws nearer.",t,{"Price":5000/1.04**(3-t)},"Years elapsed","Price ($)")
    plot("II-057 II-059 II-254 II-255","Longer zeros respond more to yields","Each curve starts at 100 at a 4% yield. At 5% the 10-year zero loses about 9.13% and the two-year loses 1.90%.",100*y,{"Two-year":100*(1.04/(1+y))**2,"Ten-year":100*(1.04/(1+y))**10},"Yield (%)","Price index (4% yield = 100)")
    x=np.linspace(-1,1,41)
    plot("II-251 II-252","Approximate price change with modified duration","At duration 5.2 a rise of 0.40 percentage points implies approximately −2.08%. On $70,000 the approximate loss is $1,456.",x,{"Approximation":-5.2*x},"Yield change (percentage points)","Price change (%)")
    bar("II-063 II-073 II-266 II-267","Discount payments at their own dates","A two-year $1,000 bond pays $50 in year one and $1,050 in year two. Their present values at 6% sum to $981.67.",["Year 1 PV","Year 2 PV"],[50/1.06,1050/1.06**2],"Present value ($)")
    bar("II-055 II-065 II-249 II-250","Same coupon, different denominators","Annual coupon is $45. Dividing by $1,000 face gives 4.5%; dividing by a $900 purchase price gives 5%.",["Coupon rate","Current yield"],[4.5,5],"Annual rate (%)")
    bar("II-259 II-260","Coupon payments and principal at maturity","Four years of semiannual coupons produce eight payments of $145. The last payment adds the $5,000 face amount.",range(1,9),[145]*7+[5145],"Cash paid ($)")
    x=np.arange(31,52)
    plot("II-067 II-261 II-262 II-263 II-264","Compare the convertible with its shares","Each bond converts to 25 shares. At $42 per share the stock package is worth $1,050. It matches the $1,100 market price at $44.",x,{"25 shares":25*x,"Bond at $1,100":np.full(len(x),1100),"Par":np.full(len(x),1000)},"Common share price ($)","Value ($)")
    bar("II-285","From gross assets to NAV","Securities 22 plus cash 1 less liabilities 3 leaves $20 million. Divide by 2.5 million shares for $8 per share.",["Securities","Cash","Liabilities","Net assets"],[22,1,-3,20],"Amount ($ millions)")
    bar("II-286 II-287","Compare the market price with NAV","NAV holds at $16. A 10% discount gives $14.40; a 5% discount gives $15.20.",["NAV","10% discount","5% discount"],[16,14.4,15.2],"Dollars per share")
    x=np.arange(0,81)
    label="Stock at expiration ($)"
    unit="Profit per share ($)"
    plot("II-151","Long call at expiration","Strike $52, premium $7. The buyer loses at most the premium and breaks even when the stock reaches $59.",x,{"Long call":np.maximum(x-52,0)-7},label,unit)
    plot("II-146 II-291","Long put at expiration","Strike $45 and premium $2. At $38 the profit is $5 per share. At or above $45 the loss is the $2 premium.",x,{"Long put":np.maximum(45-x,0)-2},label,unit)
    plot("II-292 II-293","Short put at expiration","For a $30 strike and $1.80 premium, the best result is +$1.80 a share. At a stock price of zero the loss is $28.20 a share.",x,{"Short put":1.8-np.maximum(30-x,0)},label,unit)
    plot("II-152","Uncovered short call at expiration","For a $40 strike and $2 premium, profit stays at $2 at or below $40. Each additional dollar above $40 takes another dollar from the writer.",x,{"Short call":2-np.maximum(x-40,0)},label,unit)
    plot("II-154 III-310","Covered call at expiration","Stock costs $40. Selling a $45 call for $2 caps profit at $7 and shifts break-even to $38. Stock declines below $38 still produce losses.",x,{"Covered call":x-40+2-np.maximum(x-45,0),"Stock alone":x-40},label,unit)
    plot("III-308","Protective put at expiration","Buying stock at $52 and a $48 put for $2 limits the loss to $6. At $61 the combined position earns $7.",x,{"Stock and put":x-52+np.maximum(48-x,0)-2,"Stock alone":x-52},label,unit)
    plot("II-294 II-295","Daily leverage resets","After +10% then −10%, the index grows from 100 to 99. A daily 2× fund grows from 100 to 120 then falls to 96.",[0,1,2],{"Index":[100,110,99],"Daily 2×":[100,120,96]},"Day","Value (start = 100)")
    plot("II-296","An inverse fund compounds day by day","After −5% and +4% the index ends at 98.8. A daily −1× fund gains 5% then loses 4%, ending at 100.8.",[0,1,2],{"Index":[100,95,98.8],"Daily inverse":[100,105,100.8]},"Day","Value (start = 100)")
    x=np.arange(-12,21)
    plot("II-297","Participation and cap at maturity","For this example only, principal is repaid assuming issuer solvency. The credited return is 70% of positive index gains, capped at 8%.",x,{"Credited return":np.clip(.7*x,0,8)},"Index return (%)","Credited return (%)")
    beta=np.linspace(0,2,41)
    plot("III-039 III-293 III-294","Read the security market line","With a 3% risk-free rate and 6-point market premium, expected return is 3% + beta × 6%. At beta 1.25 it is 10.5%.",beta,{"CAPM":3+6*beta},"Beta","Expected return (%)")
    bar("I-069 I-164","Compare return with the CAPM benchmark","A 2% risk-free rate, 8% market return and 1.2 beta give a 9.2% benchmark. An 11% realized return is 1.8 points higher.",["CAPM","Realized"],[9.2,11],"Return (%)")
    rho=np.linspace(-1,1,101)
    plot("III-043 III-044 III-296","Correlation changes portfolio risk","A half-and-half mix of 10% and 20% volatility has risk 11.18% at zero correlation and 15% at +1. At −1 the equal-weight mix still has 5% risk; canceling both exposures requires different weights.",rho,{"Volatility":np.sqrt(5**2+10**2+2*5*10*rho)},"Correlation","Portfolio volatility (%)")
    w=np.linspace(0,1,101)
    risk=np.sqrt((10*(1-w))**2+(20*w)**2)
    plot("III-042 III-215","Look upward at the same risk","Two hypothetical assets have 10% and 20% volatility, 4% and 10% expected returns, and zero correlation. The upper branch from the minimum-risk point offers the best return at each attainable risk.",risk,{"Two-asset mixtures":4+6*w},"Volatility (%)","Expected return (%)")
    bar("III-048 III-049 III-299 III-300","Compare the actual mix to the target","A $150,000 account holds $96,000 equities against a $90,000 target. Reallocating $6,000 to bonds restores the fixed 60/40 policy.",["Equity now","Target equity","Bonds now","Target bonds"],[96,90,54,60],"Dollars (thousands)")
    bar("III-305 III-306 III-307","Equal investments buy unequal share counts","Each month invests $600. Prices of $30, $20 and $24 buy 20, 30 and 25 shares. Total cost divided by total shares is $24.",["At $30","At $20","At $24"],[20,30,25],"Shares bought")
    plot("III-314","Drawing down a cash reserve","With no return, a $36,000 reserve falls by $2,400 each month. It reaches zero in 15 months.",np.arange(16),{"Reserve":36000-2400*np.arange(16)},"Monthly withdrawals","Balance ($)")
    bar("III-153 III-154 III-335","Walk down the bid book","A seller can fill 200 shares at $18.10. The next 150 sell at $18.00. Average proceeds per share use filled size as the weight.",["Bid $18.10","Bid $18.00"],[200,150],"Available shares")
    bar("III-155 III-156 III-336","Read depth on the offer side","100 shares are offered at $24.10 and 200 at $24.20. Buying all 300 costs $7,250.",["Ask $24.10","Ask $24.20"],[100,200],"Shares offered")
    x=np.linspace(28,52,49)
    plot("III-161 III-337","Closing a short position","For 150 shares sold at $40, lower cover prices raise profit. Deducting $120 of costs leaves $780 at a $34 cover price.",x,{"After costs":150*(40-x)-120},"Buy-to-cover price ($)","Position profit ($)")
    x=np.linspace(28000,50000,101)
    plot("III-165 III-338 III-339","Margin equity shrinks as prices fall","With $24,000 borrowed, the equity fraction is (value − 24,000)/value. It reaches 30% at about $34,286.",x/1000,{"Equity %":100*(x-24000)/x,"Requirement":[30]*len(x)},"Securities value ($ thousands)","Equity (%)")
    plot("III-275 III-345 III-346","Separate external money from returns","The account rises from 100 to 110 before a deposit of 90, then falls from 200 to 190. The two investment returns are +10% and −5%.",[0,1,2,3],{"Value":[100,110,200,190]},"0 start · 1 pre-deposit · 2 post-deposit · 3 end","Account ($ thousands)")
    bar("III-353 III-354","Weight outcomes by probability","Returns −10%, 6% and 18% have probabilities ¼, ½ and ¼. Their contributions sum to 5%.",["Loss state","Middle state","High state"],[-2.5,3,4.5],"Contribution (percentage points)")
    bar("III-355 III-281","Purchasing power grows more slowly than dollars","$100 grows to $107.10. A basket costing $100 now costs $102. Relative purchasing power rises by 107.1/102 − 1 = 5%.",["Start","Ending wealth","Basket cost"],[100,107.1,102],"Dollars")

    bar("I-128","The same basket in two years","The same quantities cost $250 in the first year and $265 in the second.",["First year","Second year"],[250,265],"Basket cost ($)",cue="What inflation rate does this basket imply?")
    bar("I-130","Two ten-year bond yields","The corporate yields 6.35% and the comparable Treasury yields 4.15%.",["Corporate","Treasury"],[6.35,4.15],"Annual yield (%)",cue="What is the ten-year corporate spread in basis points?")
    bar("I-133","Trade flows over one year","Exports are 90 billion dollars; imports are 140 billion.",["Exports","Imports"],[90,140],"Billions of dollars",cue="What are net exports, including the sign?")
    bar("I-135","Three groups in one town","There are 9,200 employed people, 800 unemployed active jobseekers and 2,500 other adults.",["Employed","Seeking work","Outside labor force"],[9200,800,2500],"Adults",cue="Using the groups shown, what is the unemployment rate?")
    bar("I-136 I-137 I-031","Changing the denominator","Initially 9,200 employed plus 800 active jobseekers make a labor force of 10,000 among 12,500 adults. If 200 stop looking, the new rate is 600/9,800.",["Active seekers before","Active seekers after"],[800,600],"People seeking work")
    bar("I-138","International trade over one year","The country imports 420 billion dollars and exports 355 billion.",["Imports","Exports"],[420,355],"Billions of dollars",cue="What is the magnitude of the country's trade deficit?")
    bar("I-139 I-140","Scale purchasing power with the price index","The index rises from 125 to 130, a factor of 1.04. At unchanged purchasing power, $60,000 scales to $62,400.",["Before","After"],[125,130],"Price index")
    bar("I-141 I-142","Follow one dollar of sales down the income statement","Sales of 500 less costs of 320 and operating expenses of 90 leave 90 in operating income. Subtract 10 of interest and 16 of taxes to reach net income of 64.",["Sales","Gross profit","Operating income","Net income"],[500,180,90,64],"Dollars (thousands)")
    bar("I-143 I-144","Which claim does each dollar of assets support?","Assets total 780. Liabilities claim 280, preferred equity 100 and common equity the remaining 400. Total equity includes both equity classes.",["Assets","Liabilities","Preferred","Common"],[780,280,100,400],"Dollars (thousands)")
    bar("I-124 I-125","The same euro invoice at two exchange rates","An €80,000 payable costs $88,000 at $1.10/€ and $92,000 at $1.15/€.",["At 1.10","At 1.15"],[88,92],"Dollar cost (thousands)")
    bar("II-242","A call just after the coupon date","Per bond, par is $1,000, purchase cost was $1,065, and the contractual call quote is 102% of par. No accrued coupon remains.",["Par","Purchase"],[1000,1065],"Dollars",cue="The bond is called at 102% of the illustrated par just after a coupon payment. How much principal does the investor receive?")
    bar("II-243","When a premium bond is called","An investor paid $1,065. Redemption at 102% of $1,000 par returns $1,020. The principal loss is $45.",["Purchase","Redemption"],[1065,1020],"Dollars per bond")
    bar("II-247 II-248","The settlement invoice includes accrued interest","A clean quote of 96.75 on $10,000 face gives $9,675. Add $85 accrued for an invoice of $9,760.",["Clean price","Invoice"],[9675,9760],"Dollars")
    plot("II-272 II-273","A split changes the units of ownership","120 shares at $75 and 180 shares at $50 both represent $9,000. A three-for-two split increases share count without creating value.",[100,120,150,180,200],{"Constant $9,000":9000/np.array([100,120,150,180,200])},"Share count","Price per share ($)")
    bar("II-280 II-281","Who sells the shares?","Two million newly issued shares and one million existing shares sell for $15 each. The issuer receives only proceeds from the new shares.",["Issuer","Existing holders"],[30,15],"Proceeds ($ millions)")
    bar("II-282 II-283","Deduct a front-end load before buying shares","A 4.5% load on $8,000 consumes $360. Only $7,640 buys shares; at $20 each it buys 382 shares.",["Into shares","Load"],[7640,360],"Dollars")
    bar("III-287","A household's monthly cash flows","Take-home income is $7,400; living costs are $4,850, debt service $750, and separate insurance $400.",["Income","Living costs","Debt service","Insurance"],[7400,4850,750,400],"Dollars per month",cue="How much of this household's monthly income remains after the three outflows?")
    bar("III-289 III-290","Household assets and claims","Assets total $500,000 and debts total $252,000. The $360,000 home has a $240,000 mortgage. Household net worth and home equity use different boundaries.",["Home","Cash","Investments","Mortgage","Other debt"],[360,40,100,240,12],"Dollars (thousands)")
    bar("III-291","Look through a fund to its holdings","The $120,000 fund contains $12,000 of employer stock. Add the direct $48,000 position to see $60,000 employer exposure in the $168,000 portfolio.",["Direct","Through fund","Other holdings"],[48,12,108],"Dollars (thousands)")
    bar("III-292","Compare survivor income with spending","60% of $2,500 a month is $1,500, or $18,000 a year. Against $24,000 of spending the survivor has an annual $6,000 gap.",["Annual spending","Survivor pension"],[24,18],"Dollars (thousands)")
    bar("III-342","Two sides of an unchanged stock quote","The bid is $25.10 and the offer is $25.18 for sufficient size. Buy at the offer and sell at the bid.",["Bid","Offer"],[25.10,25.18],"Price ($)",cue="At the displayed quotes, what is the immediate round-trip spread cost on 400 shares, ignoring commissions?")
    bar("IV-356","An advisory contract with two fee tiers","The first $500,000 accrues 1% annually and the next $300,000 accrues 0.6%. Annual fees are $5,000 and $1,800. Quarterly fees total $1,700 at a constant balance.",["First tier","Second tier"],[5000,1800],"Annual fee ($)")
    bar("IV-357","One prepaid contract period","The $1,200 fee covers 90 days, with daily proration. Service stops after 30 days.",["Served","Unserved"],[30,60],"Contract days",cue="Under this contract's daily proration, how much of the $1,200 prepaid fee is unearned?")
    bar("IV-358","Combine separately disclosed compensation","A $900 advisory fee and 2% of $15,000 in trades generate $900 plus $300.",["Advice","Commission"],[900,300],"Compensation ($)")
    bar("IV-359","Allocate mixed use by its documented proportions","This $10,000 service is 65% qualifying research and 35% administrative. The administrative portion is $3,500 under the case assumptions.",["Research","Administrative"],[65,35],"Use (%)")

    # These cues ask the learner to read the graph itself. Text alternatives give observations only.
    prices=np.array([35,45,52,59,66,73])
    plot("II-289","A purchased call at expiration","Strike $52, premium $7. The plotted profit is negative $7 at $52 and positive $7 at $66, rising a dollar per dollar between them.",
         prices,{"Profit":np.maximum(prices-52,0)-7},"Stock at expiration ($)","Profit per share ($)",
         cue="At what stock price does the call buyer break even at expiration?")
    prices=np.array([31,38,43,45,50,55])
    plot("II-290","A purchased put at expiration","The strike is $45, premium $2, and each contract covers 100 shares. At a $38 stock price the line is at +$5 per share.",
         prices,{"Profit":np.maximum(45-prices,0)-2},"Stock at expiration ($)","Profit per share ($)",
         cue="At a $38 stock price, what net profit does one 100-share put contract earn?")
    prices=np.array([30,35,38,40,45,50])
    plot("III-311","A covered call at expiration","Stock cost $40. The call strike is $45 and premium received is $2. Below $45, a $1 rise in the stock adds $1 to the position's per-share profit.",
         prices,{"Profit":prices-40+2-np.maximum(prices-45,0)},"Stock at expiration ($)","Profit per share ($)",
         cue="At which stock price does this covered call break even at expiration?")
    prices=np.array([40,48,52,54,61,66])
    plot("III-309","A stock and protective put at expiration","The stock costs $52, the put strike is $48 and its premium is $2. Above the strike, each extra dollar in stock price adds a dollar of profit.",
         prices,{"Profit":prices-52+np.maximum(48-prices,0)-2},"Stock at expiration ($)","Position profit per share ($)",
         cue="If the stock finishes at $61, what is the protected position's net profit per share?")
    plot("III-041","Where beta is zero","The fitted security market line starts at 3% when beta is zero and reaches 9% when beta is one.",
         [0,.5,1,1.5],{"Expected return":[3,6,9,12]},"Beta","Expected return (%)",
         cue="Which economic rate does the vertical intercept of this security market line represent?")
    plot("III-297","A half-and-half asset mix","The two assets have standard deviations 10% and 20%. Their weights are equal. The line shows how the portfolio's risk changes with their correlation.",
         rho,{"Portfolio":np.sqrt(125+100*rho)},"Correlation","Portfolio volatility (%)",
         cue="When return correlation reaches +1, what is this portfolio's standard deviation?")
    plot("I-058","Where a project's NPV changes sign","An outlay of $100 today pays $110 in one year. The horizontal axis varies the required return; NPV crosses zero at 10%.",
         [0,5,10,15,20],{"NPV":110/(1+np.array([0,5,10,15,20])/100)-100},"Discount rate (%)","NPV ($)",
         cue="What is the name of the discount rate where this project's curve crosses zero?")
    bar("I-160","Five annual returns","The sample values are −6, 2, 4, 4 and 11 percent.",list("ABCDE"),[-6,2,4,4,11],"Annual return (%)",cue="What is the range of the five returns, in percentage points?")
    bar("I-064","One outlier moves the mean","Samples [1,2,3,4,5] and [1,2,3,4,50] both have median 3, but the mean rises from 3 to 12.",["Original mean","New mean","Original median","New median"],[3,12,3,3],"Sample value")

    plot("I-019","An index that tracks the general price level",
         "The index starts at 100, then reaches 106 and 108.12 in successive years.",
         [0,1,2],{"Price level":[100,106,108.12]},"Year","Price index",
         cue="Annual inflation falls from 6% to 2%. What happens to the price level over the second year?")
    plot("I-100","Same Treasury maturities on two dates",
         "Yields at 1, 5 and 10 years change from 3%, 3.5% and 4% to 4%, 4.5% and 5%.",
         [1,5,10],{"Before":[3,3.5,4],"After":[4,4.5,5]},"Years to maturity","Yield (%)",
         cue="What change at each maturity makes this a parallel upward shift?")
    bar("II-060","Principal repayments from a four-bond portfolio",
        "Equal principal amounts come due in years 1, 2, 3 and 4.",
        ["Year 1","Year 2","Year 3","Year 4"],[1000]*4,"Principal repaid ($)",
        cue="Which feature of the bonds is the investor staggering in this ladder?")
    bar("II-009","Two cash flows of a Treasury bill",
        "The buyer pays $970 now and receives $1,000 at maturity, with no interim coupon.",
        ["Purchase","Maturity"],[-970,1000],"Investor cash flow ($)",
        cue="How does the bill deliver a return to this investor at maturity?")
    bar("II-053","Coupons before principal is repaid",
        "Over three years one bond pays $80 annually and the other pays no interim interest. They mature together.",
        ["Coupon bond Y1","Y2","Y3","Zero Y1","Y2","Y3"],[80,80,80,0,0,0],"Interest payment ($)",
        cue="Assuming both bonds are held to maturity, which holder has greater coupon reinvestment risk?")
    bar("II-257","One year from purchase to redemption",
        "The initial outflow is $975. One year later the investor receives $1,000 of principal plus the last $40 coupon.",
        ["Purchase now","Principal in 1 yr","Coupon in 1 yr"],[-975,1000,40],"Investor cash flow ($)",
        cue="Use the purchase outflow and both year-end receipts. What is the bond's one-year yield to maturity?")
    bar("II-288","Terms of one equity call",
        "The stock is $57, the strike is $52 and the quoted call premium is $7 per share.",
        ["Stock","Strike","Call premium"],[57,52,7],"Dollars per share",
        cue="How much of the quoted call premium is time value per share?")
    beta=np.array([0,.4,.8,1.2])
    plot("III-295","Expected returns on the security market line",
         "At betas 0, 0.4, 0.8 and 1.2 the model returns are 3%, 5%, 7% and 9%.",
         beta,{"Model return":3+5*beta},"Beta","Expected return (%)",
         cue="A portfolio lies on the plotted line with an expected return of 7%. What is its implied beta?")
    plot("III-218","Policy weight and trading boundaries",
         "The policy weight is 50%, with boundaries at 45% and 55%. After starting at 50%, the sleeve closes at 56%.",
         [1,2,3,4],{"Actual":[50,52,54,56],"Upper":[55]*4,"Lower":[45]*4},"Month","Portfolio weight (%)",
         cue="A policy trades when the actual weight crosses one of the boundaries. What rebalancing method is this?")
    bar("III-349","Initial value and two period-end amounts",
        "Beginning NAV is $20, ending ex-distribution NAV is $20.80 and the end-of-period cash distribution is $1.20 per share.",
        ["Initial NAV","Ending NAV","Cash received"],[20,20.8,1.2],"Dollars per share",
        cue="Including the cash distribution and ignoring taxes and fees, what one-period total return did the shareholder earn?")
    def market_line(ax):
        x=np.array([0,.5,1,1.5])
        curves(x,{"CAPM":3+5*x},"Beta","Expected return (%)")(ax)
        ax.scatter([1],[10],s=85,marker="D",color="#aa461c",label="Security forecast")
        ax.legend()
    add("III-212","A forecast and the security market line",
        "At beta 1.0, the forecast is 10% and the line passes through 8%.",
        market_line,cue="What does the diamond's position imply about the forecast return relative to the return required for its beta?")
    bar("II-265","Two pieces of a corporate yield quotation",
        "The maturity-matched Treasury yields 385 basis points. The desk requires 180 basis points of additional spread.",
        ["Treasury","Required spread"],[385,180],"Basis points",
        cue="Express the corporate yield meeting this spread target as an annual percentage.")
    x=np.arange(0,11)
    plot("I-099 I-020","Purchasing power of a fixed nominal payment",
         "With annual inflation of 4%, the same $1,000 payment buys about $676 of today's goods in ten years.",
         x,{"Nominal dollars":np.repeat(1000,len(x)),"Today's dollars":1000/1.04**x},"Years","Value of payment ($)")
    plot("II-019","Mortgage principal under two repayment speeds",
         "The slower repayment path leaves more principal outstanding later. The example isolates the timing effect of slower refinancing.",
         [0,1,2,3,4],{"Faster prepayment":[100,62,31,12,0],"Slower prepayment":[100,83,65,43,0]},"Year","Principal outstanding ($000)")
    bar("II-135","When a sales charge leaves the account",
        "Of a $1,000 contribution, a 5% front-end charge takes $50 at purchase, leaving $950 to invest.",
        ["Contribution","Sales charge","Invested"],[1000,50,950],"Amount ($)")
    x=np.arange(25,66)
    plot("III-071","Shareholding with a written call",
         "The shares cost $40. Writing a $50 call for $3 gives $3 of premium but caps the combined expiry profit at $13 per share, ignoring fees.",
         x,{"Shares only":x-40,"Shares + short call":x-40+3-np.maximum(x-50,0)},"Stock price at expiry ($)","Net profit per share ($)")
    add("III-177","Immediate executions at an unchanged quote",
        "An immediate buyer pays $20.05 and an immediate seller receives $19.95. The round-trip cost before fees is ten cents per share.",
        points([19.95,20.05],[1,2],"Execution price ($)","1 = sell at bid, 2 = buy at ask"))
    def dated_flows(ax):
        days=[0,20,365]
        payments=[-1000,-500,1700]
        ax.vlines(days,0,payments,lw=3,color="#135f76")
        ax.scatter(days,payments,color="#135f76")
        ax.axhline(0,color="#52636a",lw=.8)
        ax.set(xticks=[0,90,180,270,365],xlabel="Days since first investment",ylabel="Investor cash flow ($)")
        for x,y in zip(days,payments):
            ax.annotate(f"Day {x}",(x,y),xytext=(5,2),textcoords="offset points",fontsize=9)
        ax.margins(x=.14,y=.18)
    add("III-279","Irregularly dated investor cash flows",
        "A contribution on day 0, another on day 20 and a withdrawal on day 365 are separated by unequal intervals.",
        dated_flows)
