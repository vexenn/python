import asyncio
import json
import os
import time
import hmac
import hashlib
import requests
import websockets
from urllib.parse import urlencode
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, Side, OrderType
from py_clob_client.constants import POLYGON

load_dotenv()

# --- CONFIGURATION ---
SYMBOLS = {
    "BTC": {"binance": "btcusdt", "poly_tag": "Bitcoin"},
    "ETH": {"binance": "ethusdt", "poly_tag": "Ethereum"}
}

# RISK SETTINGS
MAX_SLIPPAGE = 0.01  
MIN_PROFIT_MARGIN = 0.04 
TRADE_SIZE = 50.0 

class SniperPolyBot:
    def __init__(self):
        self.host = "https://clob.polymarket.com"
        self.key = os.getenv("PRIVATE_KEY")
        self.funder = os.getenv("FUNDER_ADDRESS")
        self.client = None
        self.creds = None
        self.binance_prices = {s: 0.0 for s in SYMBOLS}
        self.active_markets = {} 

    async def setup_auth(self):
        """Unlocks L2 Sniper Mode."""
        print("🔐 Unlocking Sniper Mode...")
        temp_client = ClobClient(self.host, POLYGON, self.key, funder=self.funder)
        self.creds = temp_client.create_or_derive_api_key()
        self.client = ClobClient(self.host, POLYGON, self.key, self.creds, signature_type=1, funder=self.funder)
        print("✅ Sniper & Monitor Ready.")

    def send_telegram(self, message):
        """Emergency notifications to your phone."""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        try:
            requests.get(url)
        except:
            print("❌ Telegram Failed.")

    def execute_binance_hedge(self, symbol, amount_usd):
        """Opens a Short position on Binance to protect your capital."""
        base_url = "https://fapi.binance.com"
        endpoint = "/fapi/v1/order"
        qty = round(amount_usd / self.binance_prices[symbol], 3)
        
        params = {
            "symbol": f"{symbol}USDT",
            "side": "SELL",
            "type": "MARKET",
            "quantity": qty,
            "timestamp": int(time.time() * 1000)
        }
        
        query_string = urlencode(params)
        signature = hmac.new(os.getenv("BINANCE_SECRET_KEY").encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        
        try:
            res = requests.post(f"{base_url}{endpoint}?{query_string}&signature={signature}", 
                                headers={"X-MBX-APIKEY": os.getenv("BINANCE_API_KEY")})
            print(f"🛡️ HEDGE: Shorted {symbol}. Status: {res.status_code}")
        except Exception as e:
            print(f"🚨 HEDGE FAILED: {e}")

    async def monitor_liquidation_risk(self):
        """Background thread: Monitors Binance positions for danger."""
        while True:
            try:
                base_url = "https://fapi.binance.com/fapi/v3/positionRisk" # Using v3 for performance
                params = {"timestamp": int(time.time() * 1000)}
                query_string = urlencode(params)
                signature = hmac.new(os.getenv("BINANCE_SECRET_KEY").encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
                
                res = requests.get(f"{base_url}?{query_string}&signature={signature}", 
                                   headers={"X-MBX-APIKEY": os.getenv("BINANCE_API_KEY")}).json()

                for pos in res:
                    liq_price = float(pos['liquidationPrice'])
                    mark_price = float(pos['markPrice'])
                    
                    if liq_price > 0:
                        risk_distance = abs(liq_price - mark_price) / mark_price
                        if risk_distance < 0.02: # 2% Threshold
                            self.send_telegram(f"⚠️ LIQUIDATION RISK: {pos['symbol']} is {risk_distance*100:.2f}% from death!")
                            
            except Exception as e:
                print(f"❌ Monitor Error: {e}")
            await asyncio.sleep(10)

    async def refresh_markets(self):
        """Discovers liquid Polymarket price targets."""
        while True:
            try:
                data = requests.get("https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=50").json()
                for market in data:
                    for sym, info in SYMBOLS.items():
                        if info['poly_tag'] in market['question'] and "Price" in market['question']:
                            strike = float(market['question'].split('$')[1].split(' ')[0].replace(',', ''))
                            self.active_markets[sym] = {"id": market['clobTokenIds'][0], "strike": strike}
                print(f"🎯 Targets: {list(self.active_markets.keys())}")
            except: pass
            await asyncio.sleep(30)

    async def binance_ws_stream(self):
        """Millisecond price feed."""
        streams = "/".join([f"{v['binance']}@ticker" for v in SYMBOLS.values()])
        async with websockets.connect(f"wss://stream.binance.com:9443/ws/{streams}") as ws:
            while True:
                msg = json.loads(await ws.recv())
                symbol = msg['s'].replace('USDT', '')
                self.binance_prices[symbol] = float(msg['c'])
                asyncio.create_task(self.check_sniper_logic(symbol))

    async def check_sniper_logic(self, symbol):
        if symbol not in self.active_markets: return
        spot = self.binance_prices[symbol]
        strike = self.active_markets[symbol]['strike']
        
        if (spot - strike) / strike > 0.002: # +0.2% Signal
            await self.execute_sniper_trade(self.active_markets[symbol]['id'], 0.75, symbol)

    async def execute_sniper_trade(self, token_id, limit_price, symbol):
        """Execution: Poly Order -> Binance Hedge -> Telegram Alert."""
        try:
            book = self.client.get_order_book(token_id)
            if not book.asks: return
            
            effective_price = float(book.asks[0].price)
            if effective_price > limit_price: return

            # Profit Calculation with Fees
            fee_rate = 0.035 if 0.40 < effective_price < 0.60 else 0.01
            if (0.95 - (effective_price * (1 + fee_rate))) > MIN_PROFIT_MARGIN:
                # 1. Fire Polymarket
                order = OrderArgs(token_id=token_id, price=effective_price, 
                                  size=TRADE_SIZE/effective_price, side=Side.BUY)
                poly_res = self.client.create_and_post_order(order, OrderType.FOK)
                
                # 2. Hedge & Alert
                self.execute_binance_hedge(symbol, TRADE_SIZE)
                self.send_telegram(f"💰 PROFIT LOCKED: Bought {symbol} Poly / Shorted {symbol} Binance.")
                await asyncio.sleep(5) 

        except Exception as e:
            print(f"⚠️ Sniper Jammed: {e}")

    async def run(self):
        """The Main Engine."""
        await self.setup_auth()
        await asyncio.gather(
            self.refresh_markets(), 
            self.binance_ws_stream(),
            self.monitor_liquidation_risk() 
        )

if __name__ == "__main__":
    bot = SniperPolyBot()
    asyncio.run(bot.run())