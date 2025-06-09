#!/bin/bash

# Mostrar qué base de datos está usando
echo "DATABASE_URL = $DATABASE_URL"

# Realizar migraciones automáticamente
flask db upgrade

# Iniciar la aplicación en el puerto que define Railway (usualmente $PORT)
flask run --host=0.0.0.0 --port=${PORT:-5000}