#!/bin/bash

source apis.env.sh

cd ../api || exit 1

ROOT_DIR="$(pwd)"

export APIS

echo "[INFO]: building docker images"

for folder in "${!APIS[@]}"; do
  cd "$ROOT_DIR" || exit 1

  if [ -f "./$folder/Dockerfile" ]; then
    cd "./$folder/" || exit 1

    echo "[INFO]: $(pwd) :: building image for ${APIS[$folder]}..."
    docker build -t "${APIS[$folder]}:latest" -f "Dockerfile" .

    if [[ "$1" == "push" ]]
    then
      docker push "${APIS[$folder]}:latest"
    fi
  else
    echo "[INFO]: skipping ${APIS[$folder]} @ ./api/$folder  (no Dockerfile found)."
fi
done

echo "[INFO]: ✅ Docker images built successfully."
