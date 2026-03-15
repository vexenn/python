How to Run the Prototype
Environment Setup: Create a .env file in the root folder and add your key:
OPENAI_API_KEY=your_sk_key_here

Install Dependencies:
pip install -r requirements.txt

Launch the Server:
python app.py

Test with a "Black Swan" Scenario:
Open your terminal or Postman and send a POST request:

Bash
curl -X POST http://127.0.0.1:5000/check-risk \
-H "Content-Type: application/json" \
-d '{
    "metrics": "BTC dropped 5% in 10 mins, RSI is 20",
    "news": "Reports of a major liquidity crisis at a top-tier exchange."
}'