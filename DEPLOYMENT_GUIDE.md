# Quran Hadith API - Complete Deployment & Testing Guide

## 🚀 **Quick Start on DigitalOcean Droplet**

After SSH into your droplet, run these commands:

```bash
# 1. Clone the repository
git clone https://github.com/imran99744/quran-hadith-app.git
cd quran-hadith-app

# 2. Set up environment variables
cp .env.example .env
nano .env  # Edit with your settings

# 3. Quick start (build + start + seed)
make quick-start
```

## 🗄️ **Manual Database Setup on DigitalOcean**

### **Option 1: Create Managed PostgreSQL Database**

1. **Go to DigitalOcean Control Panel**
   - Navigate to "Databases" → "Create Database"
   - Choose PostgreSQL
   - Select plan (basic plan is fine for starters)
   - Choose same region as your droplet
   - Set database name: `quran-hadith-db`

2. **Get Connection Details**
   - Note down: Host, Port, User, Password, Database name
   - Add your droplet IP to trusted sources

3. **Update .env file**
   ```bash
   DATABASE_URL=postgresql://username:password@host:port/database_name
   POSTGRES_DB=quran_hadith_db
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   DATABASE_HOST=your_db_host
   DATABASE_PORT=25060  # DO uses this port
   ```

### **Option 2: Self-Hosted PostgreSQL on Droplet**

1. **Install PostgreSQL**
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib -y
   ```

2. **Create Database and User**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE quran_hadith_db;
   CREATE USER quran_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE quran_hadith_db TO quran_user;
   \q
   ```

3. **Configure PostgreSQL**
   ```bash
   sudo nano /etc/postgresql/14/main/postgresql.conf
   # Uncomment and set: listen_addresses = 'localhost'
   
   sudo nano /etc/postgresql/14/main/pg_hba.conf
   # Add: local   all             all                                     md5
   
   sudo systemctl restart postgresql
   ```

## 🐳 **Docker Commands**

After cloning repo and setting up .env:

```bash
# Build Docker images
make build

# Start all services
make up

# View logs
make logs

# Stop services
make down

# Access API container shell
make shell

# Access database shell
make shell-db

# Seed database with sample data
make seed-db

# Clean everything
make clean
```

## 🧪 **Testing the Application**

### **1. Health Check**
```bash
make health
# Or: curl http://localhost:8000/health
```

### **2. API Documentation**
- **Swagger UI**: http://your_droplet_ip:8000/docs
- **ReDoc**: http://your_droplet_ip:8000/redoc

### **3. Test API Endpoints**
```bash
make test-api
```

### **4. Manual API Testing**

#### **Authentication**
```bash
# Register admin user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123"
  }'

# Login to get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

#### **Quran Endpoints**
```bash
# Get all surahs
curl http://localhost:8000/api/v1/quran/surahs

# Get specific surah with ayahs
curl http://localhost:8000/api/v1/quran/surahs/1/ayahs

# Search Quran
curl "http://localhost:8000/api/v1/quran/search?q=mercy"

# Get random ayah
curl http://localhost:8000/api/v1/quran/random-ayah
```

#### **Hadith Endpoints**
```bash
# Get all collections
curl http://localhost:8000/api/v1/hadith/collections

# Get hadiths from collection
curl http://localhost:8000/api/v1/hadith/collections/1/hadiths

# Search hadiths
curl "http://localhost:8000/api/v1/hadith/search?q=prayer"

# Get random hadith
curl http://localhost:8000/api/v1/hadith/random-hadith
```

### **5. Run Automated Tests**
```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage
```

## 🔧 **Development Workflow**

### **Daily Development**
```bash
# Start services
make up

# Make changes
# ...

# Restart API to apply changes
docker-compose restart api

# Check logs
make logs
```

### **Code Quality**
```bash
# Lint code
make lint

# Format code
make format
```

### **Database Management**
```bash
# Reset database (dangerous!)
make reset-db

# Backup database
make backup-db

# Seed fresh data
make seed-db
```

## 🌐 **Production Deployment**

### **1. Environment Setup**
```bash
# Production environment variables
export DATABASE_URL=postgresql://user:pass@host:port/db
export SECRET_KEY=your-super-secret-production-key
export DEBUG=False
export ALLOWED_ORIGINS=["https://yourdomain.com"]
```

### **2. SSL Certificate (Optional)**
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

### **3. Production Docker Compose**
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  api:
    build: .
    environment:
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
      DEBUG: ${DEBUG}
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - api
    restart: always

volumes:
  postgres_data:
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Database Connection Failed**
```bash
# Check database logs
make logs | grep db

# Test database connection
make shell-db
# Then try: \lquran_hadith_db
```

#### **API Not Responding**
```bash
# Check API logs
make logs | grep api

# Restart API service
docker-compose restart api

# Check port availability
netstat -tulpn | grep 8000
```

#### **Permission Issues**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

### **Useful Commands**
```bash
# Check service status
make status

# Monitor resource usage
docker stats

# Clean up unused resources
docker system prune -f

# View container details
docker inspect quran-hadith-app_api_1
```

## 📊 **Monitoring**

### **Health Monitoring**
```bash
# Continuous health check
watch -n 30 'curl -s http://localhost:8000/health'
```

### **Log Monitoring**
```bash
# Follow all logs
make logs

# Follow specific service logs
docker-compose logs -f api
docker-compose logs -f db
```

## 🎯 **Success Checklist**

- [ ] Droplet provisioned with Terraform
- [ ] Docker and Docker Compose installed
- [ ] Database created (managed or self-hosted)
- [ ] Repository cloned on droplet
- [ ] Environment variables configured
- [ ] `make quick-start` completed successfully
- [ ] API accessible at http://droplet_ip:8000
- [ ] API docs accessible at http://droplet_ip:8000/docs
- [ ] Health endpoint returning 200
- [ ] Sample data seeded in database
- [ ] Authentication endpoints working
- [ ] Quran endpoints returning data
- [ ] Hadith endpoints returning data
- [ ] All automated tests passing

## 🆘 **Support**

If you encounter issues:

1. **Check logs**: `make logs`
2. **Verify database**: `make shell-db`
3. **Test connectivity**: `make test-api`
4. **Restart services**: `make down && make up`

The application should be fully functional once all steps in the success checklist are completed!
