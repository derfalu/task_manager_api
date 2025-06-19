# Имя файла: Makefile

.PHONY: help run down migrate upgrade init-env celery beat logs test lint rebuild

# Справка
help:
	@echo "🛠  Команды проекта:"
	@echo "  make init-env           — Проверка и создание .env при необходимости"
	@echo "  make start                — Запуск приложения через Docker Compose"
	@echo "  make stop               — Остановка и удаление контейнеров"
	@echo "  make migrate            — Применить миграции Alembic"
	@echo "  make upgrade name=...   — Создать новую миграцию"
	@echo "  make celery             — Запуск Celery-воркера"
	@echo "  make beat               — Запуск Celery Beat"
	@echo "  make logs               — Просмотр логов"
	@echo "  make rebuild            — Пересобрать все контейнеры с нуля"

# Проверка наличия .env
init-env:
	@if [ ! -f .env ]; then \
		echo "📄 .env не найден. Копируем из .env.example..."; \
		cp .env.example .env; \
	else \
		echo "✅ .env уже существует."; \
	fi

# Запуск приложения (Docker Compose)
start: init-env
	docker-compose up --build -d

# Полная остановка и удаление контейнеров, томов, сети
stop:
	docker-compose down -v --remove-orphans

# Применить миграции Alembic
migrate:
	docker-compose exec web alembic upgrade head

# Создать новую миграцию: make upgrade name=название
upgrade:
	docker-compose exec web alembic revision --autogenerate -m "$(name)"

# Запуск Celery воркера
celery:
	docker-compose exec celery_worker celery -A app.core.celery.celery_worker.celery_app worker --loglevel=info

# Запуск Celery Beat планировщика
beat:
	docker-compose exec celery_beat celery -A app.core.celery.celery_worker.celery_app beat --loglevel=info

# Просмотр логов
logs:
	docker-compose logs -f

# Полная пересборка контейнеров
rebuild:
	docker-compose down -v --remove-orphans
	docker-compose build --no-cache
	docker-compose up -d
