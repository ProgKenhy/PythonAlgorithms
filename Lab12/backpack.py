def book_shop(n: int, max_price: int, prices: list, pages: list) -> int:
    dp = [0] * (max_price + 1)

    for i in range(n):
        for w in range(max_price, prices[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - prices[i]] + pages[i])

    return dp[max_price]


n, x = map(int, input().split())
prices = list(map(int, input().split()))
pages = list(map(int, input().split()))

print(book_shop(n, x, prices, pages))
