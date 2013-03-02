from debb import daemon

if __name__ == "__main__":
    client = daemon.Client("/tmp/debb-notifyd")
#    client.notify("hello world")
    client.stop()