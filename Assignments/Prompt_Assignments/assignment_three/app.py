import json
import random
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from risk_engine import ARRE_Engine

app = Flask(__name__)
# Using cors_allowed_origins="*" to prevent connection issues during local dev
socketio = SocketIO(app, cors_allowed_origins="*")
engine = ARRE_Engine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-risk', methods=['POST'])
def check_risk():
    data = request.json
    market_metrics = data.get('metrics', 'No data provided')
    news = data.get('news', 'Neutral')

    # Trigger AI Reasoning via D.A.V.E. Logic
    result = engine.evaluate_execution_safety(market_metrics, news)
    
    # Push update to the Dashboard via WebSockets
    socketio.emit('risk_update', {'analysis': result})
    
    return jsonify({"status": "broadcasted", "analysis": json.loads(result)})

@app.route('/simulate', methods=['POST'])
def simulate():
    """
    Simulates a variety of market conditions to test the AI's response logic.
    """
    scenarios = [
        {
            "metrics": "VIX at 15, BTC +2.5% in 4h, Low Volume", 
            "news": "Major institutional bank announces Bitcoin custody services."
        },
        {
            "metrics": "VIX at 42, ETH -12%, Spreads widening on major pairs", 
            "news": "Flash crash on localized Asian exchanges; stablecoin de-pegging rumors."
        },
        {
            "metrics": "S&P 500 flat, Tech sector showing mild RSI divergence", 
            "news": "Standard CPI data released; market expecting no change in interest rates."
        },
        {
            "metrics": "Massive liquidation volume detected at $65k support", 
            "news": "Whale wallet movement of 50,000 BTC to exchanges."
        }
    ]
    
    selected = random.choice(scenarios)
    
    # Process the selected scenario through the AI Risk Engine
    result = engine.evaluate_execution_safety(selected['metrics'], selected['news'])
    
    # Broadcast to the dashboard
    socketio.emit('risk_update', {'analysis': result})
    
    return jsonify({
        "status": "simulation_complete",
        "scenario_used": selected
    })

if __name__ == '__main__':
    # Using socketio.run instead of app.run to support WebSocket connections
    socketio.run(app, debug=True, port=5000)