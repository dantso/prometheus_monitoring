from prometheus_client import start_http_server, Summary
from prometheus_client import Gauge
import time

def main():
    g = Gauge('bcr_gauge_example', 'Testing how Prometheus Gauge works')   
    start_http_server(8000)
    while True:
      g.inc(3)
      time.sleep(5)
      g.dec(2)

    
      
if __name__ == "__main__":
    main()
