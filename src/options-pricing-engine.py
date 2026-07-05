import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import yfinance as yf

def black_scholes(S, K, T, r, sigma, option_type="call"):
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        raise ValueError("Invalid inputs")

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2))
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)

    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2))
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)

    return {"price": float(price),
          "delta": float(delta), 
          "gamma": float(gamma),
          "vega": float(vega),
          "theta": float(theta / 365),
          "rho": float(rho)
    }
    
    

def binomial_tree(S, K, T, r, sigma, n=200, option_type="call", american=False):
    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    prices = np.zeros(n + 1)

    for i in range(n + 1):
        ST = S * (u ** (n - i)) * (d ** i)
        if option_type == "call":
            prices[i] = max(ST - K, 0)
        else:
            prices[i] = max(K - ST, 0)

    for step in range(n - 1, -1, -1):
        for i in range(step + 1):
            ST = S * (u ** (step - i)) * (d ** i)
            hold = np.exp(-r * dt) * (p * prices[i] + (1 - p) * prices[i + 1])
            if american:
                if option_type == "call":
                    exercise = max(ST - K, 0)
                else:
                    exercise = max(K - ST, 0)
                prices[i] = max(hold, exercise)
            else:
                prices[i] = hold
    return prices[0]


def monte_carlo(S, K, T, r, sigma, option_type="call", paths=100000):
    Z = np.random.standard_normal(paths)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == "call":
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)
    return np.exp(-r * T) * np.mean(payoff)


def implied_volatility(market_price, S, K, T, r, option_type):
    def objective(vol):
        return black_scholes(S, K, T, r, vol, option_type)["price"] - market_price

    return brentq(objective, 1e-6, 5)


def put_call_parity(call, put, S, K, r, T):
    return (call - put) - (S - K * np.exp(-r * T))


def portfolio_greeks(positions):
    return {
        "delta": sum(p["qty"] * p["delta"] for p in positions),
        "gamma": sum(p["qty"] * p["gamma"] for p in positions),
        "vega": sum(p["qty"] * p["vega"] for p in positions)
    }


def get_data(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="1y") 
    S = hist["Close"].iloc[-1]
    returns = hist["Close"].pct_change().dropna()
    sigma = returns.std() * np.sqrt(252)
    return S, sigma


ticker = "NVDA"
S, sigma = get_data(ticker)
K = S + 5
T = 60 / 365
r = 0.02

print("Black-Scholes:", black_scholes(S, K, T, r, sigma, "call"))
print("Binomial:", binomial_tree(S, K, T, r, sigma, n=300))
print("Monte Carlo:", monte_carlo(S, K, T, r, sigma))
