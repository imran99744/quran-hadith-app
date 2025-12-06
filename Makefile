# Quran Hadith API Makefile
.PHONY: help build up down logs shell test seed-db clean lint format

# Default target
help:
	@echo "Quran Hadith API - Available Commands:"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  make build      - Build Docker images"
	@echo "  make up        - Start all services (db + api)"
	@echo "  make down      - Stop all services"
	@echo "  make logs       - Show service logs"
	@echo "  make shell      - Access API container shell"
	@echo "  make shell-db   - Access database shell"
	@echo "  make clean      - Remove containers, images, volumes"
	@echo ""
	@echo "🗄️ Database Commands:"
	@echo "  make seed-db   - Seed database with sample data"
	@echo "  make reset-db   - Reset database (dangerous!)"
	@echo ""
	@echo "🧪 Testing Commands:"
	@echo "  make test      - Run API tests"
	@echo "  make test-coverage - Run tests with coverage"
	@echo ""
	@echo "🔧 Development Commands:"
	@echo "  make lint      - Run code linting"
	@echo "  make format    - Format code"
	@echo "  make install   - Install dependencies"
	@echo ""
	@echo "🌐 API Testing:"
	@echo "  make test-api  - Test API endpoints"
	@echo "  make health    - Check API health"
	@echo ""
	@echo "🚀 Production:"
	@echo "  make prod-deploy - Deploy with managed database"
	@echo "  make prod-logs   - View production logs"
	@echo "  make prod-down   - Stop production services"

# Build Docker images
build:
	@echo "🔨 Building Docker images..."
	docker compose build

# Start all services
up:
	@echo "🚀 Starting all services..."
	docker compose up -d
	@echo "✅ Services started. Use 'make logs' to view logs."
	@echo "🌐 API will be available at: http://localhost:8000"
	@echo "📚 API docs at: http://localhost:8000/docs"

# Stop all services
down:
	@echo "🛑 Stopping all services..."
	docker compose down
	@echo "✅ Services stopped."

# Show logs
logs:
	docker compose logs -f

# Access API container shell
shell:
	docker compose exec api bash

# Access database shell
shell-db:
	docker compose exec db psql -U quran_user -d quran_hadith_db

# Clean everything
clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker compose down -v --rmi all --remove-orphans
	docker system prune -f
	@echo "✅ Cleanup completed."

# Seed database
seed-db:
	@echo "🌱 Seeding database with sample data..."
	docker compose exec api python -m app.db.seed
	@echo "✅ Database seeded successfully!"

# Reset database (dangerous)
reset-db:
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? (yes/no): " confirm && [ "$$confirm" = "yes" ]
	@if [ "$$confirm" = "yes" ]; then \
		docker compose down -v; \
		docker compose up -d db; \
		sleep 10; \
		make seed-db; \
		echo "✅ Database reset completed."; \
	else \
		echo "❌ Database reset cancelled."; \
	fi

# Run tests
test:
	@echo "🧪 Running API tests..."
	docker compose exec api pytest -v

# Run tests with coverage
test-coverage:
	@echo "🧪 Running tests with coverage..."
	docker compose exec api pytest --cov=app --cov-report=html --cov-report=term

# Lint code
lint:
	@echo "🔍 Linting code..."
	docker compose exec api flake8 app/ tests/
	docker compose exec api black --check app/ tests/

# Format code
format:
	@echo "🎨 Formatting code..."
	docker compose exec api black app/ tests/
	docker compose exec api isort app/ tests/

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	docker compose exec api pip install -r requirements.txt

# Test API endpoints
test-api:
	@echo "🌐 Testing API endpoints..."
	@echo "Testing health endpoint..."
	curl -f http://localhost:8000/health || (echo "❌ Health check failed" && exit 1)
	@echo "✅ Health check passed"
	@echo ""
	@echo "Testing API docs..."
	curl -f http://localhost:8000/docs || (echo "❌ Docs check failed" && exit 1)
	@echo "✅ API docs accessible"
	@echo ""
	@echo "Testing Quran endpoint..."
	curl -f http://localhost:8000/api/v1/quran/surahs || (echo "❌ Quran endpoint failed" && exit 1)
	@echo "✅ Quran endpoint working"
	@echo ""
	@echo "Testing Hadith endpoint..."
	curl -f http://localhost:8000/api/v1/hadith/collections || (echo "❌ Hadith endpoint failed" && exit 1)
	@echo "✅ Hadith endpoint working"
	@echo ""
	@echo "🎉 All API tests passed!"

# Check API health
health:
	@echo "🏥 Checking API health..."
	curl -s http://localhost:8000/health | jq . || echo "API Health Response"

# Quick start (build + up + seed)
quick-start: build up seed-db
	@echo ""
	@echo "🚀 Quick start completed!"
	@echo "🌐 API: http://localhost:8000"
	@echo "📚 Docs: http://localhost:8000/docs"
	@echo "👤 Admin login: admin / admin123"

# Development setup
dev-setup: install
	@echo "🔧 Development environment setup completed!"
	@echo "Run 'make up' to start services."

# Production deployment with managed database
prod-deploy:
	@echo "🚀 Deploying to production with managed database..."
	docker compose -f docker-compose.prod.yml down
	docker compose -f docker-compose.prod.yml build
	docker compose -f docker-compose.prod.yml up -d
	@echo "✅ Production deployment completed!"
	@echo "🌐 API: http://localhost:8000"
	@echo "📚 Docs: http://localhost:8000/docs"

# Production logs
prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

# Production down
prod-down:
	@echo "🛑 Stopping production services..."
	docker compose -f docker-compose.prod.yml down
	@echo "✅ Production services stopped."

# Production shell
prod-shell:
	docker compose -f docker-compose.prod.yml exec api bash

# Production seed database
prod-seed-db:
	@echo "🌱 Seeding production database..."
	docker compose -f docker-compose.prod.yml exec api python -m app.db.seed
	@echo "✅ Production database seeded successfully!"

# Backup database
backup-db:
	@echo "💾 Creating database backup..."
	docker compose exec db pg_dump -U quran_user quran_hadith_db > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup completed."

# Show service status
status:
	@echo "📊 Service Status:"
	docker compose ps
