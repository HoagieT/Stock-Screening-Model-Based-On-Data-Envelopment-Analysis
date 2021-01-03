# Stock-Screening-Model-Based-On-Data-Envelopment-Analysis
A stock screening model based on Data Envelopment Analysis (DEA). The model intends to screen out the stocks whose financial statements appear to warrant a higher market cap, which makes the stock a potential value investing target.

In value investing, the first step is to look for potentially undervalued stocks. I borrowed an analytical algorithm from operational research, the Data Envelopment Analysis (DEA), to help me find companies whose valuation comps are not warranted by their financial statements. DEA is a method that enables us to compare and rank records based on their features without making any prior assumptions about the importance or weights of the features. Each record/stock has M inputs that measure the financial performances, and N outputs that measure the company’s valuation.

E_{i}=\frac{\sum_{r=1}^{N}u_{r,i}y_{r,i}}{\sum_{s=1}^{M}v_{s,i}x_{r,i}}

where, E is the efficiency of stock i, u and v are the weights of each output and input of the stock. Then the problem of finding the best weights for a particular stock i can be formulated as follows:

maximize \quad h=\frac{\sum_{r=1}^{N}u_{r,i}y_{r,i}}{\sum_{s=1}^{M}v_{s,i}x_{r,i}} \\ subject \, to \quad \frac{\sum_{r=1}^{N}u_{r,i}y_{r,j}}{\sum_{s=1}^{M}v_{s,i}x_{r,j}}\le1\,for\,every\,record\,j \\ and \, u_{r,i}, v_{s,i} \ge 0

The above optimization problem can be solved with Linear Dynamic Programming. The h in the first equation is called efficiency. A low efficiency indicates that the company might be undervalued. To apply this algorithm to assist value investing, I used each company’s financial statistics as inputs and valuation comps as outputs:

Inputs: Beta, operating margin, profit margin, revenue per share, return on assets, return on equity, EPS, revenue growth, leverage ratio

Outputs: Trailing P/E, forward P/E, EV/Sales, EV/EBIT, P/BV, PEG, P/sales

We can run this algorithm to all the stocks. The stocks with the lowest efficiency have the best chance of being undervalued, i.e., their financial statistics tell a different story from their valuation. What the algorithm gave me was a lead to a story that had to be developed. I would take a more in-depth look into the most undervalued stocks and analyse their fundamentals to decide if they are cheap for a valid reason.
