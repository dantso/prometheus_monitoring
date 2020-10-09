# Prometheus and Grafana



## Installation and Setup Using EC2 instance

## Make sure you use an Ubuntu 16.2 image for your ec2 box

Make sure the security group has ports 80, 22, 9090, 9100, 3000 open.

## Initial Ubuntu 16.04 Server Setup

After ssh into your instance: 

```
$ adduser sonu
```

Enter the username you wish and set up a password. 
Give your user root privelages.

```
$ usermod -ag sudo sonu
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

Set the user and group ownership on the new directories to the prometheus user.

```
$ sudo chown prometheus:prometheus /etc/prometheus
$ sudo chown prometheus:prometheus /var/lib/prometheus
```

# Step 2 - Download Prometheus

Download the latest version of prometheus: https://prometheus.io/download/

```
$ cd ~
$ curl -LO https://github.com/prometheus/prometheus/releases/download/v2.21.0/prometheus-2.21.0.linux-amd64.tar.gz 
```

Use the sha256sum command to generate a checksum and compare it to the checksum on the prometheus website to ensure correct download.

```
$ sha256sum prometheus-2.21.0.linux-amd64.tar.gz
```

Tar the download

```
$ tar xvf prometheus-2.21.0.linux-amd64.tar.gz
```

Copy the binaries to the proper directories

```
$ sudo cp prometheus-2.21.0.linux-amd64/prometheus /usr/local/bin/
$ sudo cp prometheus-2.21.0.linux-amd64/promtool /usr/local/bin/
```

Set the user and group ownership on the binaries to the prometheus user created before.

```
$ sudo chown prometheus:prometheus /usr/local/bin/prometheus
$ sudo chown prometheus:prometheus /usr/local/bin/promtool
```

Copy the consoles and console_libraries directories to /etc/prometheus.

```
$ sudo cp -r prometheus-2.21.0.linux-amd64/consoles /etc/prometheus
$ sudo cp -r prometheus-2.21.0.linux-amd64/console_libraries /etc/prometheus
```

Set the user and group ownership on the directories to the prometheus user.

```
$ sudo chown -R prometheus:prometheus /etc/prometheus/consoles
$ sudo chown -R prometheus:prometheus /etc/prometheus/console_libraries
```

Remove files that are no longer needed

```
$ rm -rf prometheus-2.21.0.linux-amd64.tar.gz prometheus-2.21.0.linux-amd64
```

# Step 3 - Prometheus Configuration

Create a config file to run prometheus.

```
$ sudo nano /etc/prometheus/prometheus.yml
```

Copy the contents to the config file.

```
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9090']
```

Set the user and group ownership on the configuration file to the prometheus user.

```
$ sudo chown prometheus:prometheus /etc/prometheus/prometheus.yml
```

# Step 4 - Running Prometheus

Start up Prometheus as the prometheus user, providing the path to both the configuration file and the data directory.

```
$ sudo -u prometheus /usr/local/bin/prometheus \
$   --config.file /etc/prometheus/prometheus.yml \
$   --storage.tsdb.path /var/lib/prometheus/ \
$   --web.console.templates=/etc/prometheus/consoles \
$   --web.console.libraries=/etc/prometheus/console_libraries
```

Create a new service file.

```
$ sudo nano /etc/systemd/system/prometheus.service
```

Copy contents to service file.

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

Reload systemd.

```
$ sudo systemctl daemon-reload
```

Start Prometheus.

```
$ sudo systemctl start prometheus
```

Check the service status.

```
$ sudo systemctl status prometheus
```

Wnable service to start on boot

```
$ sudo systemctl enable prometheus
```

# Step 5 - Node Exporter Download

Download the latest version of node_exporter: https://prometheus.io/download/

```
$ cd ~
$ curl -LO https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz
```

Use the sha256sum command to generate a checksum and compare it to the checksum on the prometheus website to ensure correct download.


```
$ sha256sum node_exporter-1.0.1.linux-amd64.tar.gz
```

tar the download.

```
$ tar xvf node_exporter-1.0.1.linux-amd64.tar.gz
```

Copy files to correct directory and change ownership to node_exporter user created earlier.

```
$ sudo cp node_exporter-1.0.1.linux-amd64/node_exporter /usr/local/bin
$ sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
```

Remove files which are no longer needed.

```
$ rm -rf node_exporter-1.0.1.linux-amd64.tar.gz node_exporter-1.0.1.linux-amd64
```

# Step 6 - Run Node Exporter

Create a service file for node_exporter.

```
$ sudo nano /etc/systemd/system/node_exporter.service 
```

Copy the content into the service file.

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

Reload systemd.

```
$ sudo systemctl daemon-reload
```

Start node_exporter.

```
$ sudo systemctl start node_exporter
```

Check the status.

```
$ sudo systemctl status node_exporter
```

Enable node_exporter to start on boot.

```
$ sudo systemctl enable node_exporter
```

# Step 7 - Configuring Node Exporter to Work With Prometheus

Open the config file once more and add to it.

```
$ sudo nano /etc/prometheus/prometheus.yml
```

Your config file should look like this.

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

Restart prometheus.

```
$ sudo systemctl restart prometheus
```

Check the status.

```
$ sudo systemctl status prometheus
```

# Step 8 - Making Prometheus Secure

Install this apache library.

```
$ sudo apt-get install apache2-utils
```

Set up a password with the user you want.

```
$ sudo htpasswd -c /etc/nginx/.htpasswd sonu
```

Copy the existing default files in case you need to revert.

```
$ sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/prometheus
```

Open the new configuration file and replace the location block.

```
$ sudo nano /etc/nginx/sites-available/prometheus
```

Replace the location block to this.

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

Deactive the default nginx config file and activate the new one.

```
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo ln -s /etc/nginx/sites-available/prometheus /etc/nginx/sites-enabled/
```

Check for any errors.

```
$ sudo nginx -t
```

Restart nginx.

```
$ sudo systemctl reload nginx
```

Check the status.

```
$ sudo systemctl status nginx
```

# Step 9 - Testing Prometeheus

Enter the public ip online and you should see the prometheus dashboard.


# Step 10 - Downloading and Setting Up Grafana

Download the lastest version of Grafana: https://grafana.com/grafana/download

```
$ sudo apt-get install -y adduser libfontconfig
$ wget https://dl.grafana.com/oss/release/grafana_7.2.0_amd64.deb
$ sudo dpkg -i grafana_7.2.0_amd64.deb
```

Set up and start the Grafana server.

```
$ sudo systemctl daemon-reload && sudo systemctl enable grafana-server && sudo systemctl start grafana-server
```

Enter the public ip with port 3000 online to check the grafana dashboard. Add a new data souce and select prometheus as the data source. Set the prometheus server url as the public ip url with port 9090. Click add to test the connection and save the new data source.
