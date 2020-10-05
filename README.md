# prometheus_monitoring
Monitoring examples using Prometheus python client libraries

## Installation and Setup Using EC2 instance

## Make sure you use an Ubuntu 16.2 image for your ec2 box

Make sure the security group has ports 80, 22, 9090, 9100, 3000 open.

## Initial Ubuntu 16.04 Server Setup

After ssh into your instance: 

```
adduser sonu
```

Enter the username you wish and set up a password. 
Give your user root privelages.


```
usermod -ag sudo sonu
```

## Install Nginx

```
$ sudo apt-get update
$ sudo apt-get install nginx
```

After installing check your web server.

```
$ systemctl status nginx
```

The server should be active and running. Confirm this by going to your ec2 instance's public ip. You should see a 'Welcome to nginx!' message.

## Setting up Prometheus

# Step 1

Create two new users to isolate the ownership of Prometheus' core files and directories.

```
$ sudo useradd --no-create-home --shell /bin/false prometheus
$ sudo useradd --no-create-home --shell /bin/false node_exporter
```

Create the directories to store Prometheus' files and data.

```
$ sudo mkdir /etc/prometheus
$ sudo mkdir /var/lib/prometheus
```

```
$ sudo chown prometheus:prometheus /etc/prometheus
$ sudo chown prometheus:prometheus /var/lib/prometheus
```

```
$ cd ~
$ curl -LO https://github.com/prometheus/prometheus/releases/download/v2.0.0/prometheus-2.0.0.linux-amd64.tar.gz 
```

```
$ sha256sum prometheus-2.0.0.linux-amd64.tar.gz
```

```
$ tar xvf prometheus-2.0.0.linux-amd64.tar.gz
```

```
$ sudo cp prometheus-2.0.0.linux-amd64/prometheus /usr/local/bin/
$ sudo cp prometheus-2.0.0.linux-amd64/promtool /usr/local/bin/
```

```
$ sudo chown prometheus:prometheus /usr/local/bin/prometheus
$ sudo chown prometheus:prometheus /usr/local/bin/promtool
```

```
$ sudo cp -r prometheus-2.0.0.linux-amd64/consoles /etc/prometheus
$ sudo cp -r prometheus-2.0.0.linux-amd64/console_libraries /etc/prometheus
```

```
$ sudo chown -R prometheus:prometheus /etc/prometheus/consoles
$ sudo chown -R prometheus:prometheus /etc/prometheus/console_libraries
```

```
$ rm -rf prometheus-2.0.0.linux-amd64.tar.gz prometheus-2.0.0.linux-amd64
```

```
$ sudo nano /etc/prometheus/prometheus.yml
```

```
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9090']
```

```
$ sudo chown prometheus:prometheus /etc/prometheus/prometheus.yml
```

```
$ sudo -u prometheus /usr/local/bin/prometheus \
$   --config.file /etc/prometheus/prometheus.yml \
$   --storage.tsdb.path /var/lib/prometheus/ \
$   --web.console.templates=/etc/prometheus/consoles \
$   --web.console.libraries=/etc/prometheus/console_libraries
```

```
$ sudo nano /etc/systemd/system/prometheus.service
```

```
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```

```
$ sudo systemctl daemon-reload
```

```
$ sudo systemctl start prometheus
```

```
$ sudo systemctl status prometheus
```

```
$ sudo systemctl enable prometheus
```

```
$ cd ~
$ curl -LO https://github.com/prometheus/node_exporter/releases/download/v0.15.1/node_exporter-0.15.1.linux-amd64.tar.gz
```

```
$ sha256sum node_exporter-0.15.1.linux-amd64.tar.gz
```

```
$ tar xvf node_exporter-0.15.1.linux-amd64.tar.gz
```

```
$ sudo cp node_exporter-0.15.1.linux-amd64/node_exporter /usr/local/bin
$ sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
```

```
$ rm -rf node_exporter-0.15.1.linux-amd64.tar.gz node_exporter-0.15.1.linux-amd64
```

```
$ sudo nano /etc/systemd/system/node_exporter.service 
```

```
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

```
$ sudo systemctl daemon-reload
```

```
$ sudo systemctl start node_exporter
```

```
$ sudo systemctl status node_exporter
```

```
$ sudo systemctl enable node_exporter
```

```
$ sudo nano /etc/prometheus/prometheus.yml
```

```
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'node_exporter'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9100']
```

```
$ sudo systemctl restart prometheus
```

```
$ sudo systemctl status prometheus
```

```
$ sudo apt-get install apache2-utils
```

```
$ sudo htpasswd -c /etc/nginx/.htpasswd sonu
```

```
$ sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/prometheus
```

```
$ sudo nano /etc/nginx/sites-available/prometheus
```

```
...
    location / {
        auth_basic "Prometheus server authentication";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:9090;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
...
```

```
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo ln -s /etc/nginx/sites-available/prometheus /etc/nginx/sites-enabled/
```

```
$ sudo nginx -t
```

```
$ sudo systemctl reload nginx
```

```
$ sudo systemctl status nginx
```

```
$ wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.0.4_amd64.deb
$ sudo apt-get install -y adduser libfontconfig
$ sudo dpkg -i grafana_5.0.4_amd64.deb
```

```
$ sudo systemctl daemon-reload && sudo systemctl enable grafana-server && sudo systemctl start grafana-server
```
