.PHONY: help install test clean run dry-run dev-install

help:
	@echo "Auto Kubeconfig Generator - Comandos disponibles:"
	@echo ""
	@echo "  make install      - Instalar dependencias"
	@echo "  make dev-install  - Instalar en modo desarrollo"
	@echo "  make run          - Ejecutar el script"
	@echo "  make dry-run      - Ejecutar en modo dry-run"
	@echo "  make test         - Ejecutar tests (si existen)"
	@echo "  make clean        - Limpiar archivos temporales"
	@echo "  make backup       - Hacer backup del kubeconfig actual"
	@echo ""

install:
	@echo "📦 Instalando dependencias..."
	pip install -r requirements.txt

dev-install:
	@echo "📦 Instalando en modo desarrollo..."
	pip install -e .

run:
	@echo "🚀 Ejecutando auto-kubeconfig..."
	python auto_kubeconfig.py

dry-run:
	@echo "🔍 Ejecutando en modo dry-run..."
	python auto_kubeconfig.py --dry-run

test:
	@echo "🧪 Ejecutando tests..."
	python -m pytest tests/ -v

clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/

backup:
	@echo "💾 Creando backup del kubeconfig..."
	@if [ -f ~/.kube/config ]; then \
		cp ~/.kube/config ~/.kube/config.backup_$(shell date +%Y%m%d_%H%M%S); \
		echo "✅ Backup creado"; \
	else \
		echo "⚠️  No existe ~/.kube/config"; \
	fi
