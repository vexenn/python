import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ARRE_Engine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def evaluate_execution_safety(self, market_data, news_sentiment):
        """
        Uses D.A.V.E. Logic:
        D: Data Validation (Is the data clean?)
        A: Analysis of Volatility (Is spread widening?)
        V: Verification of Trends (Is this a fake-out?)
        E: Execution Safety (Is the risk-reward ratio > 2.0?)
        """
        prompt = f"""
        ACT AS: Senior Financial Risk Controller.
        CONTEXT: Algorithmic Trading Environment.
        INPUT DATA: {market_data}
        NEWS SENTIMENT: {news_sentiment}

        TASK: Apply D.A.V.E. Logic to determine if we should allow trade execution.
        
        OUTPUT FORMAT: JSON ONLY
        {{
            "decision": "EXECUTE" | "HALT" | "REDUCE_SIZE",
            "risk_multiplier": 0.0 to 1.0,
            "dave_summary": "Short explanation of logic",
            "regime": "Trending" | "Ranging" | "Volatile"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a deterministic risk engine. No prose, only JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            return response.choices[0].message.content
        except Exception as e:
            return f'{{"decision": "HALT", "error": "{str(e)}"}}'