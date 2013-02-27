import ipc
import uuid
import sys

def start(url):
    print url

if __name__ == "__main__":
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = "/tmp/debb-notifyd-" + uuid.uuid4().get_hex()
    start(url)