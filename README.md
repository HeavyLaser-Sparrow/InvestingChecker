
# 📈 Enhanced Trade Analysis Tool

This Python script provides an advanced stock analysis system by combining technical and fundamental analysis. 
It uses the **Financial Modeling Prep API** to retrieve stock data and assists in making informed trading decisions: 
**Buy**, **Sell**, or **Hold**.

---

## 🚀 Features

- 🔄 **Live Stock Data**: Retrieves real-time stock prices, market cap, daily highs/lows, and moving averages.
- 📊 **Fundamental Analysis**: Computes a fundamental score based on revenue growth and profit margin.
- 🧮 **Technical Analysis**: Evaluates technical indicators such as moving averages and daily price ranges.
- 🎯 **Trade Expectancy**: Calculates potential trade expectancy to estimate profitability.
- 🎛️ **Composite Scoring**: Combines technical and fundamental indicators into a composite chance of winning.
- 📝 **Trade Recommendation**: Provides actionable insights—Buy, Hold, or Sell—based on analysis.

---

## ⚙️ Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Install Dependencies:**
   ```bash
   pip install requests
   ```

---

## 💡 Usage

1. **Update API Key:**  
   Replace the placeholder API key (`PUT API KEY HERE`) in the script with your [Financial Modeling Prep API](https://financialmodelingprep.com/developer/docs/) key.
   There are multiple placeholders for API key

3. **Run the Script:**
   ```bash
   python <script_name>.py
   ```

4. **Follow the Prompts:**  
   - Enter the stock ticker symbol (e.g., AAPL, MSFT).  
   - Input your target price and stop-loss price when prompted.

---

## 📝 Example Output

```
=== Enhanced Trade Analysis Tool ===
Enter the stock ticker symbol: AAPL

Current price for AAPL: $175.00
Market Cap: $2,500,000,000,000
Day High: $177.00, Day Low: $172.00
50-Day Moving Average: $173.00
200-Day Moving Average: $160.00

--- Trade Analysis ---
Ticker:                      AAPL
Current Price:               $175.00
Target Price:                $185.00
Stop-Loss:                   $170.00
Technical Chance:            71.4%
Fundamental Score:           80.0%
Composite Chance:            74.2%
Calculated Expectancy:       5.20
Technical Recommendation:    Buy
Final Decision:              Buy
```

---

## ⚖️ How It Works

### 1. **Technical Chance of Winning**  
   - Calculated based on distances between the current price, target price, and stop-loss levels.

### 2. **Fundamental Score**  
   - Derived from revenue growth and profit margin based on the last two income statements.

### 3. **Composite Chance of Winning**  
   - Weighted average combining technical and fundamental metrics (`70%` technical, `30%` fundamental by default).

### 4. **Trade Expectancy**  
   - Predicts expected profitability using the chance of winning and price targets.

### 5. **Final Decision**  
   - **Buy**: High composite chance and positive expectancy.  
   - **Sell**: Low composite chance or negative expectancy.  
   - **Hold**: Neutral metrics.

---

## 🔒 Disclaimer

> **This tool is for educational purposes only. It does not constitute financial advice. Investing in stocks involves risks, including the potential loss of principal. Always do your own research before making financial decisions.**

---

## 💬 Contributing

Contributions, suggestions, and improvements are welcome! Feel free to submit a pull request or open an issue.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
