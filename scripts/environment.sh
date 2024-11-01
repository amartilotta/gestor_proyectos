#!/bin/sh

#? Set the working directory to the root of the project
cd "$(dirname "$(readlink -f "$0")")/.."

#? Copy the .env file to use inside the container
echo "Actualizando variables de entorno..."


if ! cp example.env .env; then
  echo "    → Error ❌"
  exit 1
fi

chmod +rwx .env
echo "    → Éxito ✅"
