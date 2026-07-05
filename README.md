Options Pricing Engine


Author:** Dzandu Selorm (dzand-cmd)  
**Project Type:** Quantitative Research  
**Language:** Python  
**Status:** Complete 

---

## Overview

This project implements an options pricing engine based on the Black-Scholes framework, extended into a modular system for pricing derivatives and analyzing option sensitivities (Greeks). It models option prices as a function of underlying asset price, volatility, time to maturity, and risk-free rate.

The objective is to understand derivative pricing mechanics and how volatility and time decay affect option valuation.


## Project Structure

options-pricing-engine/
│
├── src/
│   ├── options_pricing_engine.py   # Core Black-Scholes pricing logic
│
├── README.md                       # Project documentation


## Core Features

- Black-Scholes option pricing model
- Call and put option valuation
- Computation of Greeks: Delta, Gamma, Vega, Theta
- Sensitivity analysis with respect to volatility and time
- Visualization of option price behavior


## Methodology

The model is based on the Black-Scholes assumptions:
- Log-normal asset price dynamics
- Constant volatility
- Constant risk-free rate
- No arbitrage conditions

Key outputs:
- Fair value of European call and put options
- Sensitivity of option price to market parameters


## How to run

git clone https://github.com/dzand-cmd/options-pricing-engine.git
cd options-pricing-engine
python options-pricing-engine.py 


