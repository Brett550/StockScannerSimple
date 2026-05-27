import subprocess
import json

class ZacksClient:
    def __init__(self):
        pass

    def get_zacks_data(self, tickers):

        result = subprocess.run(
            ["node", "zacks-bridge/index.js", json.dumps(tickers)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"Error fetching Zacks data: {result.stderr}")
        
        return json.loads(result.stdout)