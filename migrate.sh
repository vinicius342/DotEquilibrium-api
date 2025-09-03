#!/bin/bash

# Script para executar migrações do Django
echo "🔄 Executando makemigrations..."
python3 manage.py makemigrations

echo "🔄 Executando migrate..."
python3 manage.py migrate

echo "✅ Migrações concluídas!"
