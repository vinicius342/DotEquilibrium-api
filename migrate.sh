#!/bin/bash

# Script para executar migrações do Django
echo "🔄 Executando makemigrations..."
python manage.py makemigrations

echo "🔄 Executando migrate..."
python manage.py migrate

echo "✅ Migrações concluídas!"
