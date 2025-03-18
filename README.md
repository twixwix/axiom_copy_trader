# Axiom Copy Trader

Axiom Copy Trader is a simple Python bot that enables copy trading of wallets using the Axiom.trade WebSocket. It listens for buy/sell signals and automatically trades Solana memecoins/tokens accordingly.

## Disclaimer

- This project is **not affiliated with Axiom.trade**, and they do not endorse or support it in any way.
- This is **not an official product** of Axiom.trade.
- The bot has **not been extensively tested**, and I **do not take responsibility for any losses** incurred while using it.
- **I do not recommend putting money on it. Use it at your own risk.**
- The Raydium **BUY** transaction is disabled by default because it has not been tested yet. See below for enabling it.

If you wish to create an account on Axiom.trade, you can use my referral link:
[Sign up on Axiom.trade](https://axiom.trade/@calvet)

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/calvet/axiom-copy-trader.git
   cd axiom-copy-trader
   ```

2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file with the following format:
   ```ini
   RPC_URL_PUMP_FUN=https://api.mainnet-beta.solana.com
   RPC_URL_RAYDIUM=https://api.mainnet-beta.solana.com
   WALLET_PUBLIC_KEY=your_public_key_here
   WALLET_PRIVATE_KEY=your_private_key_here
   TRACK_WALLETS=G3g1CKqKWSVEVURZDNMazDBv7YAhMNTjhJBVRTiKZygk
   SOL_IN=0.01
   MAX_SOL_SPEND=0.1
   MAX_SLIPPAGE=35
   ALLOW_REBUY=false
   MAX_BUY_ATTEMPTS=1
   DEBUG=false
   ```

   - `TRACK_WALLETS` can include multiple wallets, separated by `|` (e.g., `wallet1|wallet2|wallet3`).
   - `SOL_IN` is the fixed amount of SOL to use for each buy order.
   - `ALLOW_REBUY` defines whether the bot is allowed to rebuy the same token.
   - `MAX_BUY_ATTEMPTS` is the maximum number of times the bot will retry a failed buy transaction before giving up.

4. Obtain your authentication token:
   You can obtain the authentication token by opening the Axiom.trade website in Google Chrome, going to the **Network** tab in Developer Tools (F12 or Ctrl+Shift+I), and finding the first request that returns the token.

5. Add your authentication token to `cookie.txt`:
   ```
   auth-refresh-token=your_refresh_token_here; auth-access-token=your_access_token_here;
   ```

## Enabling Raydium Buy Transactions (Experimental)

By default, buy transactions for tokens on Raydium are **disabled** because they have **not been tested deeply**. If you want to enable it, uncomment the following line in the code at **line 433**:

```python
# 'buy': lambda: sell_token('ra', token_name, token_address, max_slippage),
```

## Usage

Run the bot with:
```sh
python main.py
```

## Credits

This project was made possible thanks to:
- [AL-THE-BOT-FATHER/pump_fun_py](https://github.com/AL-THE-BOT-FATHER/pump_fun_py)
- [AL-THE-BOT-FATHER/raydium_py](https://github.com/AL-THE-BOT-FATHER/raydium_py)

These libraries provide the necessary contract functionality for Pump.fun and Raydium.

## Donations

If you find this project useful and want to support future development, feel free to donate to my Solana wallet:
```
4ugZWiyAYH7auVajf3axVykxTLsc13cx9oHCzETUjc21
```

Any contribution is greatly appreciated!

