import redis
from datetime import datetime
import pytz  # pip install pytz if not installed

# Redis connection details
REDIS_HOST = 'fp-freshid-sandbox.redis.apps-us-east-1'
REDIS_PORT = 11151
REDIS_PASSWORD = 'v20D37zdP4@Ep'
REDIS_DB = 0

# Connect to Redis
r = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True
)

# Subscribe to keyevent notifications
pubsub = r.pubsub()
pubsub.psubscribe('__keyevent@0__:expired', '__keyevent@0__:del')

print("Listening for key expiration or deletion events...")

# Function to get IST timestamp
def get_ist_time():
    utc_now = datetime.utcnow()
    ist = pytz.timezone('Asia/Kolkata')
    return utc_now.replace(tzinfo=pytz.utc).astimezone(ist).isoformat()

# Listen to events
for message in pubsub.listen():
    if message['type'] == 'pmessage':
        event_type = message['channel']
        key = message['data']

        if key.startswith('spring:session:sessions:'):
            print(f"[{get_ist_time()} IST] [{event_type}] Key affected: {key}")