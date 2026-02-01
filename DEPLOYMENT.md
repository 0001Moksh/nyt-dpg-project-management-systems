# DPG PMS - Deployment Guide

Complete guide for deploying the DPG Project Management System to production.

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Frontend Deployment](#frontend-deployment)
3. [Backend Deployment](#backend-deployment)
4. [Database Backup & Migration](#database-backup--migration)
5. [Post-Deployment Verification](#post-deployment-verification)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Rollback Procedures](#rollback-procedures)

---

## Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing: `npm run test` (frontend), `pytest` (backend)
- [ ] No console errors in development
- [ ] TypeScript compilation successful: `npm run type-check`
- [ ] Code linting passed: `npm run lint`
- [ ] All security vulnerabilities resolved: `npm audit`, `pip audit`

### Environment Setup
- [ ] Production `.env` file configured with real values
- [ ] All secrets in environment variables (not in code)
- [ ] Database URL points to production PostgreSQL
- [ ] SMTP credentials verified
- [ ] Groq API key configured
- [ ] CORS origins set correctly
- [ ] JWT_SECRET_KEY is strong (32+ characters)

### Database
- [ ] Database backups automated
- [ ] Migrations tested in staging
- [ ] Database user permissions configured
- [ ] Connection pooling optimized

### Performance
- [ ] Frontend build optimized: `npm run build`
- [ ] Database indexes created
- [ ] CDN configured for static assets
- [ ] Compression enabled

### Security
- [ ] HTTPS/SSL configured
- [ ] CORS properly restricted
- [ ] Rate limiting enabled
- [ ] SQL injection protections verified
- [ ] XSS protections verified
- [ ] CSRF tokens enabled

---

## Frontend Deployment

### Option 1: Vercel (Recommended for Next.js)

#### Prerequisites
- Vercel account: https://vercel.com
- GitHub repository connected

#### Steps

1. **Connect GitHub Repository**
   ```bash
   # Push code to GitHub
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com
   - Click "New Project"
   - Select your GitHub repository
   - Vercel automatically detects Next.js

3. **Configure Environment Variables**
   ```
   NEXT_PUBLIC_API_BASE_URL=https://api.dpg-itm.edu.in
   NEXT_PUBLIC_APP_NAME=DPG Project Management System
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel builds and deploys automatically
   - Production URL: `https://dpg-pms.vercel.app`

5. **Custom Domain (Optional)**
   - Go to Project Settings → Domains
   - Add custom domain: `dpg.dpg-itm.edu.in`
   - Update DNS records at domain registrar

#### Environment Variables for Production
```
NEXT_PUBLIC_API_BASE_URL=https://api.dpg-itm.edu.in
NEXT_PUBLIC_APP_NAME=DPG Project Management System
NEXT_PUBLIC_COLLEGE_NAME=DPG ITM College
```

### Option 2: AWS Amplify

1. **Build Frontend**
   ```bash
   npm run build
   ```

2. **Create AWS Amplify App**
   ```bash
   npm install -g @aws-amplify/cli
   amplify init
   amplify publish
   ```

3. **Configure Custom Domain**
   - AWS Amplify Console → Domain Management
   - Add custom domain

### Option 3: Docker + Cloud Run

1. **Create Dockerfile**
   ```dockerfile
   FROM node:18-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production
   COPY . .
   RUN npm run build
   EXPOSE 3000
   CMD ["npm", "start"]
   ```

2. **Build and Push Image**
   ```bash
   docker build -t gcr.io/PROJECT_ID/dpg-pms-frontend .
   docker push gcr.io/PROJECT_ID/dpg-pms-frontend
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy dpg-pms-frontend \
     --image gcr.io/PROJECT_ID/dpg-pms-frontend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars NEXT_PUBLIC_API_BASE_URL=https://api.dpg-itm.edu.in
   ```

---

## Backend Deployment

### Option 1: Azure App Service (Current Deployment)

#### Prerequisites
- Azure subscription
- Azure CLI installed
- Backend code ready

#### Steps

1. **Create Resource Group**
   ```bash
   az group create \
     --name dpg-pms-rg \
     --location eastus
   ```

2. **Create App Service Plan**
   ```bash
   az appservice plan create \
     --name dpg-pms-plan \
     --resource-group dpg-pms-rg \
     --sku B1 \
     --is-linux
   ```

3. **Create Web App**
   ```bash
   az webapp create \
     --resource-group dpg-pms-rg \
     --plan dpg-pms-plan \
     --name dpg-pms-backend \
     --runtime "PYTHON|3.11"
   ```

4. **Create PostgreSQL Database**
   ```bash
   az postgres flexible-server create \
     --resource-group dpg-pms-rg \
     --name dpg-pms-db \
     --admin-user dpg_admin \
     --admin-password YourSecurePassword123! \
     --location eastus \
     --sku-name Standard_B1ms
   ```

5. **Configure App Settings**
   ```bash
   az webapp config appsettings set \
     --resource-group dpg-pms-rg \
     --name dpg-pms-backend \
     --settings \
       DATABASE_URL="postgresql://dpg_admin:password@dpg-pms-db.postgres.database.azure.com:5432/dpg_pms" \
       FASTAPI_DEBUG=false \
       SMTP_HOST=smtp.gmail.com \
       SMTP_USER=your-email@gmail.com \
       SMTP_PASSWORD=your-app-password \
       JWT_SECRET_KEY=your-super-secret-key \
       GROQ_API_KEY=your-groq-api-key \
       CORS_ORIGINS="https://dpg-pms.vercel.app"
   ```

6. **Deploy Code**
   ```bash
   # From backend directory
   az webapp deployment source config-zip \
     --resource-group dpg-pms-rg \
     --name dpg-pms-backend \
     --src-path backend.zip
   ```

   Or use Git:
   ```bash
   az webapp deployment user set --user-name your-username --password your-password
   git remote add azure https://your-username@dpg-pms-backend.scm.azurewebsites.net:443/dpg-pms-backend.git
   git push azure main
   ```

7. **Run Migrations**
   ```bash
   az webapp ssh --resource-group dpg-pms-rg --name dpg-pms-backend
   # Inside SSH session:
   alembic upgrade head
   ```

#### Access Points
- **API**: https://dpg-pms-backend.azurewebsites.net
- **Docs**: https://dpg-pms-backend.azurewebsites.net/docs

### Option 2: Docker on Azure Container Instances

1. **Build Docker Image**
   ```bash
   docker build -t dpg-pms-backend:latest .
   ```

2. **Push to Azure Container Registry**
   ```bash
   az acr create --resource-group dpg-pms-rg --name dpgpmsacr --sku Basic
   az acr build --registry dpgpmsacr --image dpg-pms-backend:latest .
   ```

3. **Deploy Container**
   ```bash
   az container create \
     --resource-group dpg-pms-rg \
     --name dpg-pms-backend \
     --image dpgpmsacr.azurecr.io/dpg-pms-backend:latest \
     --cpu 1 \
     --memory 1 \
     --registry-login-server dpgpmsacr.azurecr.io \
     --registry-username <username> \
     --registry-password <password> \
     --environment-variables \
       DATABASE_URL="postgresql://..." \
       SMTP_HOST="smtp.gmail.com" \
       GROQ_API_KEY="your-key" \
     --ports 8000 \
     --protocol TCP
   ```

### Option 3: Google Cloud Run

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD exec gunicorn --bind :$PORT --workers 4 --timeout 0 app.main:app
   ```

2. **Build and Push**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/dpg-pms-backend
   ```

3. **Deploy**
   ```bash
   gcloud run deploy dpg-pms-backend \
     --image gcr.io/PROJECT_ID/dpg-pms-backend \
     --platform managed \
     --region us-central1 \
     --memory 2Gi \
     --cpu 2 \
     --set-env-vars DATABASE_URL="...",SMTP_HOST="smtp.gmail.com"
   ```

---

## Database Backup & Migration

### Pre-Deployment Backup

```bash
# Backup production database before deployment
pg_dump \
  -h localhost \
  -U dpg_user \
  -d dpg_pms \
  --format=custom \
  --file=backup_$(date +%Y%m%d_%H%M%S).dump
```

### Automated Backups

#### Azure Backup
1. Go to Azure Portal → PostgreSQL Server
2. Click "Backup and restore"
3. Enable automatic backups (daily)

#### AWS RDS Backups
```bash
# Create automated backup
aws rds create-db-snapshot \
  --db-instance-identifier dpg-pms-db \
  --db-snapshot-identifier dpg-pms-backup-$(date +%Y%m%d)
```

### Database Migration

1. **Run Migrations**
   ```bash
   # SSH into deployed backend
   alembic upgrade head
   ```

2. **Verify Migration**
   ```bash
   # Connect to database and verify tables
   psql -h dpg-pms-db.postgres.database.azure.com \
        -U dpg_admin \
        -d dpg_pms \
        -c "\dt"
   ```

### Restore from Backup

```bash
# Restore from backup file
pg_restore \
  -h localhost \
  -U dpg_user \
  -d dpg_pms \
  -v backup_20240115_143022.dump
```

---

## Post-Deployment Verification

### 1. Frontend Checks

```bash
# Test frontend is running
curl -s https://dpg-pms.vercel.app | head -20

# Check API communication
# Open browser and test login flow
# Verify no console errors
```

### 2. Backend Checks

```bash
# Test API is running
curl https://api.dpg-itm.edu.in/health

# Test API documentation
curl https://api.dpg-itm.edu.in/docs

# Test authentication endpoint
curl -X POST https://api.dpg-itm.edu.in/api/v1/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"test@dpg-itm.edu.in"}'
```

### 3. Database Checks

```bash
# Connect to production database
psql -h dpg-pms-db.postgres.database.azure.com \
     -U dpg_admin \
     -d dpg_pms

# Verify tables exist
\dt

# Check user count
SELECT COUNT(*) FROM users;

# Exit
\q
```

### 4. Email Verification

Test SMTP by sending a test email:

```python
import asyncio
from app.services.email_service import email_service

async def test_email():
    result = await email_service.send_otp_email(
        "admin@dpg-itm.edu.in",
        "123456",
        "Admin"
    )
    print(f"Email sent: {result}")

asyncio.run(test_email())
```

### 5. SSL/HTTPS Verification

```bash
# Check SSL certificate
openssl s_client -connect api.dpg-itm.edu.in:443

# Verify certificate validity
curl -v https://api.dpg-itm.edu.in/health
```

### 6. Load Testing (Optional)

```bash
# Install Apache Bench
# macOS: brew install httpd

# Test frontend
ab -n 1000 -c 10 https://dpg-pms.vercel.app/

# Test API
ab -n 100 -c 5 https://api.dpg-itm.edu.in/health
```

---

## Monitoring & Maintenance

### Azure Monitoring

1. **Enable Application Insights**
   ```bash
   az monitor app-insights component create \
     --app dpg-pms-insights \
     --location eastus \
     --resource-group dpg-pms-rg \
     --application-type web
   ```

2. **View Metrics**
   - Azure Portal → App Service → Metrics
   - Monitor CPU, Memory, HTTP requests

### Logging

1. **Backend Logging**
   ```python
   # Logs are sent to:
   # - Console (development)
   # - /var/log/dpg-pms/app.log (production)
   # - Azure Application Insights (if configured)
   ```

2. **Access Logs**
   ```bash
   # Azure CLI
   az webapp log tail --resource-group dpg-pms-rg --name dpg-pms-backend
   ```

### Performance Optimization

1. **Enable Caching**
   - Frontend: Vercel CDN (automatic)
   - Backend: Redis/Memcached (if needed)

2. **Database Optimization**
   ```sql
   -- Create indexes on frequently queried fields
   CREATE INDEX idx_users_email ON users(email);
   CREATE INDEX idx_submissions_team_id ON submissions(team_id);
   CREATE INDEX idx_submissions_created_at ON submissions(created_at);
   ```

3. **API Optimization**
   - Implement pagination
   - Use query optimization
   - Cache responses

---

## Rollback Procedures

### Frontend Rollback (Vercel)

1. **Via Git**
   ```bash
   git revert <commit-hash>
   git push origin main
   # Vercel automatically redeploys
   ```

2. **Via Vercel Dashboard**
   - Go to Deployments
   - Click on previous successful deployment
   - Click "Promote to Production"

### Backend Rollback (Azure)

1. **Via Git**
   ```bash
   git revert <commit-hash>
   git push azure main
   # Azure automatically redeploys
   ```

2. **Via Azure Portal**
   - Go to App Service → Deployment slots
   - Swap staging and production

3. **Database Rollback**
   ```bash
   # Downgrade database schema
   alembic downgrade -1
   
   # Or restore from backup
   pg_restore -d dpg_pms backup_file.dump
   ```

---

## Security Hardening

### Update Dependencies

```bash
# Frontend
npm update
npm audit fix

# Backend
pip install --upgrade pip
pip list --outdated
```

### Rotate Secrets

1. **Update JWT Secret**
   - Generate new JWT_SECRET_KEY
   - Update all deployed instances
   - Old tokens will invalidate

2. **Update SMTP Password**
   - Update Gmail App Password (or SMTP provider)
   - Update environment variable
   - Redeploy

3. **Update API Keys**
   - Regenerate Groq API key if needed
   - Update environment variables

### Enable WAF (Web Application Firewall)

```bash
# Azure Web Application Firewall
az webapp waf-config set \
  --resource-group dpg-pms-rg \
  --name dpg-pms-backend \
  --enabled true \
  --mode Prevention
```

---

## Troubleshooting Deployment

### Issue: 503 Service Unavailable

**Solution:**
```bash
# Check if backend is running
curl https://api.dpg-itm.edu.in/health

# Check logs
az webapp log tail --resource-group dpg-pms-rg --name dpg-pms-backend

# Restart app service
az webapp restart --resource-group dpg-pms-rg --name dpg-pms-backend
```

### Issue: Database Connection Error

**Solution:**
```bash
# Verify database is running
az postgres flexible-server show \
  --resource-group dpg-pms-rg \
  --name dpg-pms-db

# Check firewall rules
az postgres flexible-server firewall-rule list \
  --resource-group dpg-pms-rg \
  --name dpg-pms-db

# Allow app service IP
az postgres flexible-server firewall-rule create \
  --resource-group dpg-pms-rg \
  --name dpg-pms-db \
  --rule-name allow-app-service \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255
```

### Issue: CORS Errors

**Solution:**
```bash
# Update CORS origins in backend
az webapp config appsettings set \
  --resource-group dpg-pms-rg \
  --name dpg-pms-backend \
  --settings CORS_ORIGINS="https://dpg-pms.vercel.app,https://your-domain.com"
```

---

## Post-Deployment Support

- **Frontend Issues**: Check Vercel dashboard
- **Backend Issues**: Check Azure Portal / Application Insights
- **Database Issues**: Connect via pgAdmin or Azure portal
- **Email Issues**: Check Gmail/SMTP provider logs

---

## Deployment Checklist Summary

- [ ] Code committed to main branch
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database backups created
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Azure
- [ ] Database migrations run
- [ ] SSL certificates valid
- [ ] API endpoints tested
- [ ] Email notifications verified
- [ ] Monitoring enabled
- [ ] Rollback plan documented

---

**Deployment completed successfully! 🚀**

For ongoing support, refer to the monitoring and maintenance sections.
