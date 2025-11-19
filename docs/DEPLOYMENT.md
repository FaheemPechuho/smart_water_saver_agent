# Deployment Guide

This guide covers various deployment options for the Smart Water Saver Agent.

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t smart-water-saver-agent .

# Run the container
docker run -d \
  --name smart-water-agent \
  -p 8000:8000 \
  --env-file .env \
  smart-water-saver-agent
```

### Using Docker Compose

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## ☁️ Cloud Deployment

### Fly.io

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and Initialize**
   ```bash
   fly auth login
   fly launch
   ```

3. **Set Environment Variables**
   ```bash
   fly secrets set OPENAI_API_KEY=your_key_here
   fly secrets set WEATHER_API_KEY=your_key_here
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

### Heroku

1. **Create Heroku App**
   ```bash
   heroku create smart-water-saver-agent
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your_key_here
   heroku config:set WEATHER_API_KEY=your_key_here
   ```

3. **Create Procfile**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### AWS EC2

1. **Launch EC2 Instance** (Ubuntu 22.04)

2. **SSH and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3.11 python3-pip python3-venv -y
   
   # Clone repository
   git clone https://github.com/your-repo/smart-water-saver-agent.git
   cd smart-water-saver-agent
   
   # Setup virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Configure environment
   nano .env  # Add your API keys
   ```

3. **Setup Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/water-agent.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Smart Water Saver Agent
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/smart-water-saver-agent
   Environment="PATH=/home/ubuntu/smart-water-saver-agent/venv/bin"
   ExecStart=/home/ubuntu/smart-water-saver-agent/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable water-agent
   sudo systemctl start water-agent
   ```

4. **Setup Nginx Reverse Proxy** (Optional)
   ```bash
   sudo apt install nginx -y
   sudo nano /etc/nginx/sites-available/water-agent
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   
   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/water-agent /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name SmartWaterAgent --location eastus

# Create container instance
az container create \
  --resource-group SmartWaterAgent \
  --name smart-water-agent \
  --image your-dockerhub-username/smart-water-saver-agent \
  --dns-name-label smart-water-agent \
  --ports 8000 \
  --environment-variables \
    OPENAI_API_KEY=your_key \
    WEATHER_API_KEY=your_key
```

## 🔒 Production Checklist

- [ ] Set strong environment variables
- [ ] Enable HTTPS/SSL (use Let's Encrypt)
- [ ] Configure CORS for specific origins
- [ ] Set up monitoring and logging
- [ ] Implement rate limiting
- [ ] Set up backup for database (if using)
- [ ] Configure health check monitoring
- [ ] Set up CI/CD pipeline
- [ ] Document API endpoints
- [ ] Test error handling
- [ ] Set up alerting

## 📊 Monitoring

### Health Check

Monitor the `/health` endpoint:

```bash
curl https://your-domain.com/health
```

### Logs

```bash
# Docker
docker logs -f smart-water-agent

# Systemd
sudo journalctl -u water-agent -f
```

## 🔄 Updates

```bash
# Pull latest code
git pull origin main

# Rebuild and restart (Docker)
docker-compose down
docker-compose up -d --build

# Restart (Systemd)
sudo systemctl restart water-agent
```

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# or
netstat -tulpn | grep 8000

# Kill the process
kill -9 <PID>
```

### Permission Denied
```bash
# Fix file permissions
chmod +x run.sh

# Fix directory permissions
sudo chown -R $USER:$USER .
```

### Out of Memory
- Increase container/instance memory
- Use smaller OpenAI model (gpt-3.5-turbo)
- Implement request queuing

## 📞 Support

For issues or questions, refer to the main README.md or contact the development team.

