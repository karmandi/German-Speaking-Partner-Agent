# Deployment Guide

This guide covers deploying the German Speaking Partner Agent to production.

## 🚀 Quick Deployment Options

### Option 1: Docker Compose (Recommended for Beginners)

**Prerequisites:**
- Docker and Docker Compose installed
- OpenAI API key

**Steps:**

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/German-Speaking-Partner-Agent.git
cd German-Speaking-Partner-Agent

# 2. Create .env file
cp backend/.env.example backend/.env
# Edit backend/.env with your OpenAI API key

# 3. Build and run
docker-compose up --build

# 4. Access application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# Health check: http://localhost:8000/health
```

### Option 2: Heroku Deployment

**Prerequisites:**
- Heroku CLI installed
- GitHub repository
- OpenAI API key

**Steps:**

```bash
# 1. Login to Heroku
heroku login

# 2. Create new app
heroku create your-app-name

# 3. Set environment variables
heroku config:set OPENAI_API_KEY=your_api_key
heroku config:set LANGUAGE_LEVEL=A2

# 4. Add buildpacks
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs

# 5. Deploy
git push heroku main
```

### Option 3: AWS EC2 Deployment

**Prerequisites:**
- AWS account
- EC2 instance (t3.micro or larger)
- SSH access to instance

**Steps:**

```bash
# 1. SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 2. Install dependencies
sudo yum update -y
sudo yum install python3 nodejs git -y
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. Clone and setup
git clone https://github.com/yourusername/German-Speaking-Partner-Agent.git
cd German-Speaking-Partner-Agent
cp backend/.env.example backend/.env
# Edit .env with API keys

# 4. Run with Docker Compose
docker-compose up -d

# 5. Configure Nginx (optional, for production)
# Follow Nginx reverse proxy setup below
```

### Option 4: Vercel + Railway (Frontend + Backend Separation)

**Backend on Railway:**

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login and create project
railway login
railway init

# 3. Add service
railway add

# 4. Set environment variables
railway variables set OPENAI_API_KEY=your_key

# 5. Deploy
railway up
```

## 🔒 Production Checklist

- [ ] Update `allowed_origins` in backend for production domain
- [ ] Set environment variables securely
- [ ] Enable HTTPS/SSL certificate
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Setup error tracking (Sentry)
- [ ] Enable rate limiting
- [ ] Review security headers
- [ ] Setup automated backups
- [ ] Configure CDN for static files

## 📊 Monitoring

### Application Health

```bash
# Check health endpoint
curl https://your-app.com/health
```

### Log Monitoring

```bash
# Docker Compose logs
docker-compose logs -f backend

# Heroku logs
heroku logs --tail

# AWS CloudWatch
aws logs tail /aws/ec2/your-instance
```

### Performance Monitoring

- Setup New Relic or DataDog
- Monitor API response times
- Track error rates
- Monitor resource usage

## 🔐 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use secret management services
   - Rotate API keys regularly

2. **HTTPS**
   - Use Let's Encrypt for free SSL
   - Enable HSTS headers
   - Redirect HTTP to HTTPS

3. **Rate Limiting**
   ```python
   # Add to FastAPI
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

4. **CORS Configuration**
   - Whitelist specific domains
   - Avoid `allow_origins=["*"]` in production

5. **Dependency Updates**
   - Regularly update dependencies
   - Use `pip audit` for security vulnerabilities
   - Use `npm audit` for frontend

## 🧪 Pre-Deployment Testing

```bash
# Backend tests
cd backend
python -m pytest --cov=app

# Frontend build test
cd frontend
npm run build

# Integration test
npm run test:integration
```

## 📈 Scaling Considerations

- **Database**: Add persistent storage for conversation history
- **Caching**: Implement Redis for API responses
- **Load Balancing**: Use Nginx or HAProxy for traffic distribution
- **Queue Processing**: Use Celery for async tasks
- **CDN**: CloudFront or Cloudflare for static assets

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Verify API key
echo $OPENAI_API_KEY

# Test API
curl http://localhost:8000/health
```

### Frontend can't reach backend
```bash
# Check CORS settings
# Verify backend is running
# Check firewall rules
# Verify API_BASE URL in frontend config
```

### High latency
- Check OpenAI API status
- Review CloudWatch metrics
- Setup closer service regions
- Enable caching

---

For more deployment options and advanced configurations, see the README.md
