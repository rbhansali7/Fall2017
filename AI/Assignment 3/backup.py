def findMaxProfit(m,n,grid,dp):

    infinity = 1000
    buyValue = +infinity
    profit = -infinity

    #if F is inaccessible return
    if grid[m][n]<0:
        return (buyValue,profit)

    dp[1][1] = (buyValue, profit)

    #Initialize the values of topmost row and leftmost column
    for i in range(2,n+1):
        #Shop
        if grid[1][i]>0:
            # it is not possible to make a larger profit by selling at this position
            if grid[1][i]< buyValue:
                buyValue = grid[1][i]
            #a profit can be made at this position. So check if its larger than the current maximum profit and update
            else:
                if(grid[1][i]-buyValue>profit):
                    profit = grid[1][i]-buyValue


            #fill dp[0][i] cell with the updated buyValue and profit values
            dp[1][i] = (buyValue, profit)

        #Empty
        elif grid[1][i]==0:
            #the buyValue and profit value will be the same as the previous row cell
            dp[1][i] = dp[1][i-1]
        #Inaccessible
        elif grid[1][i]<0:
            #all remaining row cells are inaccessible so set (buyValue,profit) = (+infinity,-infinity) and break
            for j in range(i,n+1):
                dp[1][j]=(+infinity,-infinity)
            break

    buyValue = +infinity
    profit = -infinity
    for i in range(2, m+1):
        # Shop
        if grid[i][1] > 0:
            # it is not possible to make a larger profit by selling at this position
            if grid[i][1] < buyValue:
                buyValue = grid[i][1]
            # a profit can be made at this position. So check if its larger than the current maximum profit and update
            else:
                if (grid[i][1] - buyValue > profit):
                    profit = grid[i][1] - buyValue

            # fill dp[0][i] cell with the updated buyValue and profit values
            dp[i][1] = (buyValue, profit)

        # Empty
        elif grid[i][1] == 0:
            # the buyValue and profit value will be the same as previous column cell
            dp[i][1] = dp[i-1][1]
        # Inaccessible
        elif grid[i][1] < 0:
            # all remaining row cells are inaccessible so set (buyValue,profit) = (+infinity,-infinity) and break
            for j in range(i, m+1):
                dp[j][1] = (+infinity, -infinity)
            break

    #Now run the main loop
    for i in range(2,m+1):
        for j in range(2,n+1):
            #extract the (buyValue,profit) of left and top cells
            lval, lprofit = dp[i][j - 1]
            tval, tprofit = dp[i - 1][j]
            # Shop
            # the profit will be a maximum of the profit values to the left cell, top cell,
            # or the profit generated at that point and the buyValue will be updated to the minimum of left cell, top cell
            # and grid[i][j] value
            if grid[i][j]>0:
                buyValue = min(lval,tval,grid[i][j])
                profit = max(lprofit,tprofit,grid[i][j]-lval,grid[i][j]-tval)
                dp[i][j]=(buyValue,profit)
            #Empty
            elif grid[i][j]==0:
                dp[i][j] = (min(lval,tval),max(lprofit,tprofit))
            #Inaccessible
            elif grid[i][j]<0:
                dp[i][j] = (+infinity,-infinity)

    #backtrack
    i=m
    j=n
    path=""
    while i>=1 and j>=1:

        #top cell is inaccessible
        if grid[i-1][j]<0:
            path+="E"
            j=j-1
            continue
        #left cell is inaccessible
        if grid[i][j-1]<0:
            path+="S"
            i=i-1
            continue

        lval, lprofit = dp[i][j - 1]
        tval, tprofit = dp[i - 1][j]
        #empty
        if grid[i][j]==0:
            bVal,profit = dp[i][j]
            if profit==lprofit:
                path+="E"
                j=j-1
                continue
            if profit==tprofit:
                path+="S"
                i=i-1
                continue
        #shop
        if grid[i][j]>0:
            bVal,profit=dp[i][j]
            if profit ==lprofit or profit==grid[i][j]-lval:
                path+="E"
                j=j-1
                continue
            if profit==tprofit or profit==grid[i][j]-tval:
                path+="S"
                i=i-1
                continue

    path=path[:-1]
    print path[::-1]

    return dp[m][n]


if __name__=="__main__":
    m=8
    n=8
    grid = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,0,0,0,20,0,0,-1,45],[-1,0,0,9,0,32,0,0,0],[-1,23,0,0,0,-1,0,20,0]
        ,[-1,0,-1,8,0,0,-1,0,0],[-1,0,12,0,0,0,10,0,0],[-1,0,20,-1,0,0,0,0,-1],[-1,0,0,0,0,-1,15,-1,0],[-1,1,0,21,-1,0,0,5,0]]

    dp=[]
    for i in range(0,m+1):
        tmp=[]
        for j in range(0,n+1):
            tmp.append((0,0))
        dp.append(tmp)


    buyValue,profit = findMaxProfit(m,n,grid,dp)
    print profit












