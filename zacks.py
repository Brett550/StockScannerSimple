import subprocess
import json
from unittest import result

class ZacksClient:
    def __init__(self):
        pass

    def get_zacks_data(self, ticker):

        result = subprocess.run(
            ["node", "zacks-bridge/index.js", ticker],
            capture_output=True,
            text=True
        )

        print("return code:", result.returncode)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            raise Exception(f"Error fetching Zacks data: {result.stderr}")
        
        return json.loads(result.stdout)