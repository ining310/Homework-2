liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def getAmountOut(amountIn, reserveIn, reserveOut):
    if (amountIn < 0):
        print("UniswapV2Library: INSUFFICIENT_INPUT_AMOUNT")
        return 0
    if (reserveIn <= 0 or reserveOut <= 0):
        print("UniswapV2Library: INSUFFICIENT_LIQUIDITY")
        return 0
    # print("(997*",amountIn,"*",reserveOut,")/(1000*",reserveIn,"+997*",amountIn,") = ",(997*amountIn*reserveOut)/(1000*reserveIn+997*amountIn),sep="")
    return (997*amountIn*reserveOut)/(1000*reserveIn+997*amountIn)

def getAmountsOut(factory, amountIn, path):
    if (len(path) < 2):
        print("UniswapV2Library: INVALID_PATH")
        return []
    amounts = [amountIn]
    for i,factory in enumerate(path):
        if (i >= len(path)-1): break
        if (path[i]==path[i+1]):
            print("consecutive same token")
            return []
        (reserveIn, reserveOut) = getReserves(factory,path[i],path[i+1])
        amountOut = getAmountOut(amounts[i],reserveIn,reserveOut)
        amounts.append(amountOut)
        update(amountIn,amountOut,factory,path[i],path[i+1])
    return amounts

def getReserves(factory, token0, token1):
    if ((token0,token1) in liquidity):
        (reserve0, reserve1) = liquidity[(token0,token1)]
    else:
        (reserve1, reserve0) = liquidity[(token1,token0)]
    return (reserve0, reserve1) if (factory == token0) else (reserve1, reserve0)

def update(amountIn,amountOut,factory,token0,token1):
    tokenIn = token0 if (factory == token0) else token1
    tokenOut = token1 if (factory == token0) else token0
    if ((tokenIn,tokenOut) in liquidity):
        (_reserveIn, _reserveOut) = liquidity[(tokenIn,tokenOut)]
        liquidity[(tokenIn,tokenOut)] = (_reserveIn+amountIn, _reserveOut-amountOut)
    else:
        (_reserveOut, _reserveIn) = liquidity[(tokenOut,tokenIn)]
        liquidity[(tokenOut,tokenIn)] = (_reserveOut-amountOut,_reserveIn+amountIn)

# path = ['tokenB','tokenA','tokenB','tokenA','tokenB']
# amounts = getAmountsOut('tokenB',5,path)
print(amounts)
tokens = ['tokenA','tokenB','tokenC','tokenD','tokenE']
