from Client import Client
from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('MyLogger')

logger.info("Opening Client")
client = Client('openai-server', 'CartPole-v0')
client.Init()

logger.info("---------------- DEBUG SLOW ----------------")
res = client.DebugSlow()
logger.info("---------------- DEBUG FAST ----------------")
res = client.DebugFast()

# while True:
#     logger.info(f"Sending Debug #1 @          {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
#     res = client.DebugSlow()
#     logger.info(f"Sending Debug #2 @          {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
#     res = client.DebugSlow()
#     logger.info(f"Sending Debug #3 @          {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
#     res = client.DebugSlow()
    
    # logger.info(f"Finished Sending Debug @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")