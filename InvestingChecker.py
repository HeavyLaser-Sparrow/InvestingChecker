import requests

def get_current_price(ticker, api_key="API KEY HERE"):
    """
    Fetch the current stock price and key technical metrics using the Financial Modeling Prep API.
    """
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors.
        data = response.json()
        if not data:
            print(f"No data returned for ticker {ticker}.")
            return None
        stock_data = data[0]
        current_price = float(stock_data.get("price"))
        market_cap = stock_data.get("marketCap")
        day_high = stock_data.get("dayHigh")
        day_low = stock_data.get("dayLow")
        price_avg50 = stock_data.get("priceAvg50")
        price_avg200 = stock_data.get("priceAvg200")
        return current_price, market_cap, day_high, day_low, price_avg50, price_avg200
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def get_fundamental_score(ticker, api_key="API KEY HERE"):
    """
    Fetch the latest two income statements from Financial Modeling Prep and compute a simple
    fundamental score based on revenue growth and profit margin.

    Uses the endpoint:
    https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=2&apikey={api_key}

    The score is normalized between 0 (poor fundamentals) and 1 (strong fundamentals).
    """
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=2&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data or len(data) < 2:
            print(f"Not enough income statement data available for {ticker}. Using neutral score (0.5).")
            return 0.5  # Neutral score if not enough data
        latest = data[0]
        previous = data[1]
        revenue_latest = latest.get("revenue")
        revenue_previous = previous.get("revenue")
        net_income_latest = latest.get("netIncome")

        if not revenue_latest or not revenue_previous or revenue_previous == 0 or net_income_latest is None:
            return 0.5

        # Calculate revenue growth rate
        revenue_growth = (revenue_latest - revenue_previous) / revenue_previous

        # Calculate profit margin for the latest period
        profit_margin = net_income_latest / revenue_latest if revenue_latest else 0

        # Normalize each metric between 0 and 1.
        normalized_profit_margin = max(0, min(1, profit_margin))
        normalized_revenue_growth = max(0, min(1, revenue_growth))

        # The fundamental score is the average of the two normalized metrics.
        fundamental_score = (normalized_profit_margin + normalized_revenue_growth) / 2

        print(f"Fundamental Score for {ticker}: {fundamental_score:.2f} "
              f"(Profit Margin: {profit_margin:.2f}, Revenue Growth: {revenue_growth:.2f})")
        return fundamental_score
    except Exception as e:
        print(f"Error fetching fundamental data for {ticker}: {e}")
        return 0.5

def calculate_technical_chance_of_winning(current_price, target_price, stop_loss):
    """
    Calculate the base chance of winning based solely on price distances.
    """
    stop_loss_distance = abs(current_price - stop_loss)
    target_distance = abs(target_price - current_price)
    if stop_loss_distance + target_distance == 0:
        return 0.5
    return stop_loss_distance / (stop_loss_distance + target_distance)

def calculate_composite_chance_of_winning(current_price, target_price, stop_loss, fundamental_score, w_tech=0.7, w_fund=0.3):
    """
    Combine the technical chance (based on price distances) with the fundamental score.
    We use a weighted average where w_tech and w_fund represent the weights
    for the technical and fundamental components respectively.
    """
    technical_chance = calculate_technical_chance_of_winning(current_price, target_price, stop_loss)
    composite_chance = w_tech * technical_chance + w_fund * fundamental_score
    return composite_chance

def calculate_expectancy(current_price, target_price, stop_loss, chance_of_winning):
    """
    Calculate the trade expectancy.
    Formula: expectancy = (chance_of_winning * (target_price - current_price)) -
                             ((1 - chance_of_winning) * (current_price - stop_loss))
    """
    return chance_of_winning * (target_price - current_price) - (1 - chance_of_winning) * (current_price - stop_loss)

def final_decision(composite_chance, expectancy, chance_threshold=0.55, expectancy_threshold=0):
    """
    Make a final buy/sell/hold decision based on the composite chance and expectancy.

    - If composite chance is strong (above chance_threshold) and expectancy is positive,
      then the trade is considered favorable: "Buy".
    - If composite chance is weak (below chance_threshold) or expectancy is negative,
      then the trade is considered unfavorable: "Sell".
    - Otherwise, the recommendation is to "Hold".

    You can adjust the thresholds to suit your risk tolerance and backtesting results.
    """
    if composite_chance >= chance_threshold and expectancy > expectancy_threshold:
        return "Buy"
    elif composite_chance < chance_threshold and expectancy < expectancy_threshold:
        return "Sell"
    else:
        return "Hold"

def evaluate_stock_for_trade(current_price, market_cap, day_high, day_low, price_avg50, price_avg200):
    """
    Evaluate whether to buy, hold, or sell based on technical indicators.
    This function prints some technical signals based on moving averages and daily ranges.
    """
    recommendation = "Hold"  # Default recommendation

    # Market Cap Analysis
    if market_cap < 1000000000:
        recommendation = "Sell"
        print(f"Market Cap: ${market_cap} (Small cap: consider selling)")

    # Moving Averages Analysis
    if current_price > price_avg50:
        print(f"Price is above the 50-day moving average ({price_avg50}). Bullish signal - up.")
    else:
        recommendation = "Sell"
        print(f"Price is below the 50-day moving average ({price_avg50}). Bearish signal - down.")

    if current_price > price_avg200:
        print(f"Price is above the 200-day moving average ({price_avg200}). Long-term bullish trend - up.")
    else:
        recommendation = "Sell"
        print(f"Price is below the 200-day moving average ({price_avg200}). Long-term bearish trend - down.")

    # Daily Range Analysis
    if (day_high - day_low) != 0:
        price_to_day_low_ratio = (current_price - day_low) / (day_high - day_low)
    else:
        price_to_day_low_ratio = 0.5
    if price_to_day_low_ratio < 0.3:
        print("Price is close to day's low. Potential buy signal.")
        recommendation = "Buy"
    elif price_to_day_low_ratio > 0.7:
        print("Price is close to day's high. Potential sell signal.")
        recommendation = "Sell"

    return recommendation

def main():
    print("=== Enhanced Trade Analysis Tool ===")
    ticker = input("Enter the stock ticker symbol: ").upper().strip()
    api_key = ""  # Replace with your API key if needed

    # Fetch technical data
    data = get_current_price(ticker, api_key)
    if data is None:
        print("Could not retrieve the financial data. Exiting.")
        return
    current_price, market_cap, day_high, day_low, price_avg50, price_avg200 = data
    print(f"\nCurrent price for {ticker}: ${current_price:.2f}")
    print(f"Market Cap: ${market_cap}")
    print(f"Day High: ${day_high}, Day Low: ${day_low}")
    print(f"50-Day Moving Average: ${price_avg50}")
    print(f"200-Day Moving Average: ${price_avg200}")

    # Fetch fundamental data and calculate a fundamental score.
    fundamental_score = get_fundamental_score(ticker, api_key)

    try:
        target_price = float(input(f"\nEnter your target price for {ticker}: "))
        stop_loss = float(input(f"Enter your stop-loss price for {ticker}: "))
    except ValueError:
        print("Invalid input for target price or stop-loss. Exiting.")
        return

    # Calculate the composite chance of winning and trade expectancy.
    composite_chance = calculate_composite_chance_of_winning(current_price, target_price, stop_loss, fundamental_score)
    expectancy = calculate_expectancy(current_price, target_price, stop_loss, composite_chance)

    # We can use both technical indicators and our composite calculations.
    tech_based_recommendation = evaluate_stock_for_trade(current_price, market_cap, day_high, day_low, price_avg50, price_avg200)
    final_recommendation = final_decision(composite_chance, expectancy)

    print("\n--- Trade Analysis ---")
    print(f"Ticker:                      {ticker}")
    print(f"Current Price:               ${current_price:.2f}")
    print(f"Target Price:                ${target_price:.2f}")
    print(f"Stop-Loss:                   ${stop_loss:.2f}")
    print(f"Technical Chance:            {calculate_technical_chance_of_winning(current_price, target_price, stop_loss)*100:.1f}%")
    print(f"Fundamental Score:           {fundamental_score*100:.1f}%")
    print(f"Composite Chance:            {composite_chance*100:.1f}%")
    print(f"Calculated Expectancy:       {expectancy:.2f}")
    print(f"Technical Recommendation:    {tech_based_recommendation}")
    print(f"Final Decision:              {final_recommendation}")

if __name__ == '__main__':
    main()
