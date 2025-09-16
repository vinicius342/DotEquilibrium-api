#!/bin/bash

source ./venv/bin/activate

echo "🚀 Iniciando o servidor Django em background..."
python3 manage.py runserver &
DJANGO_PID=$!

echo "✅ Servidor Django iniciado (PID: $DJANGO_PID)!"

cd dotequilibrium-frontend/

echo "🚀 Iniciando o servidor React..."
npm run dev &
REACT_PID=$!

echo "✅ Ambos os servidores estão rodando!"
echo "Django: http://127.0.0.1:8000"
echo "React: http://localhost:5173"
echo ""
echo "Para parar os servidores, pressione Ctrl+C"

# Aguarda qualquer um dos processos terminar
wait