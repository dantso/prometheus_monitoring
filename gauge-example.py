from prometheus_client import start_http_server, Summary
from prometheus_client import Gauge

def main():
    g = Gauge('bcr-gauge-example', 'Testing how Prometheus Gauge works')   
    start_http_server(8000)
    g.set(1)
    
      
if __name__ == "__main__":
    main()
