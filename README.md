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
   git clone https://github.com/calvet/axiom_copy_trader.git
   cd axiom_copy_trader
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
   TRACK_WALLETS=4ugZWiyAYH7auVajf3axVykxTLsc13cx9oHCzETUjc21
   SOL_IN=0.01
   MAX_SOL_SPEND=0.1
   MAX_SLIPPAGE=35
   ALLOW_REBUY=false
   MAX_BUY_ATTEMPTS=1
   DEBUG=false
   
   # Discord Bot Konfiguration
   DISCORD_TOKEN=your_discord_bot_token_here
   DISCORD_CHANNEL_ID=your_channel_id_here
   ```

### Environment Variables Explanation

- **RPC_URL_PUMP_FUN**: The RPC URL used for transactions on Pump.fun.
- **RPC_URL_RAYDIUM**: The RPC URL used for transactions on Raydium.
- **WALLET_PUBLIC_KEY**: Your Solana wallet public key.
- **WALLET_PRIVATE_KEY**: Your private key in **Base58 format** (can be extracted from Phantom Wallet - [Guide](https://help.phantom.com/hc/en-us/articles/28355165637011-Exporting-Your-Private-Key)).
- **TRACK_WALLETS**: Wallets to track for copy trading. Multiple wallets can be separated using `|` (e.g., `wallet1|wallet2|wallet3`).
- **SOL_IN**: The fixed amount of SOL to use for each buy order.
- **MAX_SOL_SPEND**: The maximum amount of SOL that can be spent while the bot is running. If set to `0`, there is no limit.
- **MAX_SLIPPAGE**: The maximum slippage allowed for transactions before they fail.
- **ALLOW_REBUY**: Defines whether the bot is allowed to rebuy the same token (`true` or `false`).
- **MAX_BUY_ATTEMPTS**: The maximum number of times the bot will retry a failed buy transaction before giving up.
- **DEBUG**: If set to `true`, it enables detailed logs, including packet logs from WebSockets, for debugging purposes.
- **DISCORD_TOKEN**: Your Discord Bot Token (see Discord Bot Setup section).
- **DISCORD_CHANNEL_ID**: The ID of the Discord channel where notifications will be sent.

4. Obtain your authentication token:
   You can obtain the authentication token by opening the Axiom.trade website in Google Chrome, going to the **Network** tab in Developer Tools (F12 or Ctrl+Shift+I), and finding the first request that returns the token.

5. Add your authentication token to `cookie.txt`:
   ```
   auth-refresh-token=your_refresh_token_here; auth-access-token=your_access_token_here;
   ```

## Discord Bot Setup

1. Create a Discord Bot:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" tab and click "Add Bot"
   - Under the bot settings, enable "Message Content Intent"
   - Copy the bot token and add it to your `.env` file as `DISCORD_TOKEN`

2. Invite the Bot to Your Server:
   - Go to the "OAuth2" tab in the Developer Portal
   - Select "bot" under "Scopes"
   - Select the permissions you want to give the bot (at minimum: "Send Messages", "Read Message History")
   - Copy the generated URL and open it in your browser to invite the bot to your server

3. Get the Channel ID:
   - Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
   - Right-click on the channel where you want to receive notifications and select "Copy ID"
   - Add this ID to your `.env` file as `DISCORD_CHANNEL_ID`

## Enabling Raydium Buy Transactions (Experimental)

By default, buy transactions for tokens on Raydium are **disabled** because they have **not been tested deeply**. If you want to enable it, uncomment the following line in the code at **line 433**:

```python
# 'buy': lambda: sell_token('ra', token_name, token_address, max_slippage),
```

## Usage

### Local Development

Run the bot with:
```sh
python main.py
```

### Running as a Service on Linux VPS

1. Transfer all project files to your VPS.

2. Make the installation script executable:
   ```sh
   chmod +x install_service.sh
   ```

3. Run the installation script as root:
   ```sh
   sudo ./install_service.sh
   ```

4. The script will:
   - Configure the service with your current user and directory
   - Install the service to start automatically on boot
   - Start the service immediately

5. Useful service management commands:
   ```sh
   # Check service status
   sudo systemctl status axiom_trade_bot.service
   
   # Stop the service
   sudo systemctl stop axiom_trade_bot.service
   
   # Start the service
   sudo systemctl start axiom_trade_bot.service
   
   # Restart the service
   sudo systemctl restart axiom_trade_bot.service
   
   # View logs
   sudo journalctl -u axiom_trade_bot.service
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

