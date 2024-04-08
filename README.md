# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution
Profitable path = tokenB -> tokenA -> tokenD -> toeknC -> tokenB <br />
(B, A) -> (A, D) -> (D, C) -> (C, B) <br />
(5, 5.655321988655322) -> (5.655321988655322, 2.4587813170979333) -> (2.4587813170979333, 5.0889272933015155) -> (5.0889272933015155, 20.129888944077443) <br />
Final reward (your tokenB balance) = 20.129888944077443 <br />
There is the other path which reward > 20:  tokenB -> tokenA -> tokenE -> tokenD -> toeknC -> tokenB

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution
Slippage in AMM could be addressed in the case when we swap A token for B token, the expected B token before swap might not equal the actual B token after swap, which is due to the fluctuation of liquidity, size of trade , and the speed of the chain (larger trade or slower speed may exacerbate the slippage). <br />

Uniswap V2 offer a slippage tolerance, which is a lower bound of the actual B token (received). If B is lower than this threshold, and then the transaction will be reverted to avoid further loss. <br />
There are functions in periphery, with a setting of "amountOutMin", e.g. function swapExactTokensForTokens. If the final swap is lower than the amountOutMin, the transaction will revert: 
```
require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
```
```
function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external virtual override ensure(deadline) returns (uint[] memory amounts) {
        amounts = UniswapV2Library.getAmountsOut(factory, amountIn, path);
        require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
        TransferHelper.safeTransferFrom(
            path[0], msg.sender, UniswapV2Library.pairFor(factory, path[0], path[1]), amounts[0]
        );
        _swap(amounts, path, to);
    }
```

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution
The minimum liquidity resembles a threshold(10**3), and the first MINIMUM_LIQUIDITY tokens will be permanently lock to solve the "first minter problem", which happens when the first minter owns 100% of the LP pool and conducts inflation attack (inflate the share price as much as 1001 times on the first deposit). To ensure no-one owns the entire supply of LP tokens and can easily manipulate the price, <code>liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY); _mint(address(0), MINIMUM_LIQUIDITY);</code> calculate the liquidity above the threshold and lock the first MINIMUM_LIQUIDITY tokens. <br />
Refernece: <br />
https://www.rareskills.io/post/uniswap-v2-mint-and-burn <br />
https://github.com/sherlock-audit/2023-12-dodo-gsp-judging/issues/55


## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution
```liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);```takes min on the 2 tokens, and the best situation is the 2 ratio is the same, which imlies that the LPs tend to increase the supply of 2 tokens without changing the ratio of 2 tokens (keep pool balanced). There is an example (from RareSkills) to illustrate the reason for using min not max. <br />

Initial A:B = 100:100, supply of LP tokens = 1 <br />
Someone supply 1 additional tokenA (at a cost of $100) and raise the pool value to $300 <br />
By taking max, he owns 1/2 of the supply of the LP tokens and control $150, but he only deposited $100. This is stealing from other LP providers.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution
A searcher profits from buying low and selling high with the characteristics of AMM and price slippage, regardless the victim user buys at a higher price. The scenario could be a victim user swap a lot A for B, and a searcher knows the price and front-runs the victim to buy B (before victim's transaction). As token B is getting less, the price of B and slippage is higher for victim, and a searcher could sell B at a higher price. <br />
When initiating a swap, we can encrypt transaction details(e.g zk-SNARKs, a zero-knowledge-proof technique), but the corresponding gas is much higher. So another possible way is to lower the swap amount so that attackers might not be interested in attacking the transaction. <br />

Refernece: <br />
ppt of TA <br />
https://medium.com/coinmonks/defi-sandwich-attack-explain-776f6f43b2fd
