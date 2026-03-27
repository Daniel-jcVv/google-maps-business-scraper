#!/bin/bash
# Script de limpieza para mantener el proyecto organizado

echo "🧹 Limpiando archivos temporales y caché..."

# Eliminar cachés de Python
find . -type d -name "__pycache__" -prune -exec rm -rf {} \; 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# Eliminar archivos de cobertura
rm -f .coverage 2>/dev/null
rm -rf htmlcov/ 2>/dev/null

# Eliminar caché de pytest
rm -rf .pytest_cache/ 2>/dev/null

# Preservar carpetas importantes (.agent y .context)
echo "✅ Carpetas .agent/ y .context/ preservadas"

echo "✨ Limpieza completada"
