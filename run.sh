if [ ! -f .env ]; then
  cp .env.sample .env
  echo "✅ .env создан из .env.sample. Пожалуйста, проверьте переменные."
fi