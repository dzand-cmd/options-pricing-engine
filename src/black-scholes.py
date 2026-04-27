import yfinance as yf
import numpy as np
from scipy.stats import norm

# S is the underlying asset price
# K is the strike price
# T is the time to maturity in years
# r is the risk-free interest rate
# sigma is the volatility 

def black_scholes_price_and_greeks(S, K, T, r, sigma, option_type):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if option_type == 'call':
        price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    elif option_type == 'put':
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

    pdf_d1 = norm.pdf(d1)
    cdf_d1 = norm.cdf(d1)
    cdf_d2 = norm.cdf(d2)

    # Delta
    if option_type == 'call':
        delta = cdf_d1
    else:
        delta = cdf_d1 - 1

    # Gamma
    gamma = pdf_d1 / (S * sigma * np.sqrt(T))

    # Vega
    vega = S * pdf_d1 * np.sqrt(T)

    # Theta
    if option_type == 'call':
        theta = (-S * pdf_d1 * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * cdf_d2)
    elif option_type == 'put':
        theta = (-S * pdf_d1 * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2))

    # Rho
    if option_type == 'call':
        rho = K * T * np.exp(-r * T) * cdf_d2
    elif option_type == 'put':
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    return 'Price:' + str(price) + '\nDelta:' + str(delta) + '\nGamma:' + str(gamma)  + '\nVega:' + str(vega) + '\nTheta:' + str(theta) + '\nRho:' + str(rho)

print(black_scholes_price_and_greeks(100,101.5,0.2,0.07,0.06,option_type = "call"))

ticker = 'NVDA'
data = yf.Ticker(ticker)
S = data.history(period = '1d')['Close'].iloc[-1]
K = S + 3
T = 60/365
r = 0.02
option_type = 'put'
history = data.history(period = '1d')['Close']
returns = history.pct_change().dropna()
sigma = returns.std()*np.sqrt(252)

print(black_scholes_price_and_greeks(S, K, T, r, sigma, option_type))