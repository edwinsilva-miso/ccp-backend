#!/bin/bash

source automation.env.sh

if [[ -n "$1" ]]
then
  source ./secrets/secrets.env.sh
fi

cd ../api || exit 1
ROOT_DIR="$(pwd)"

export APIS

echo "[INFO]: Building docker images for APIs"

if [[ -n "$1" ]] && [[ "$1" == "--apis" ]] || [[ "$1" == "--push-all" ]]
then
  for folder in "${!APIS[@]}"; do
    cd "$ROOT_DIR" || exit 1

    if [[ -f "./$folder/Dockerfile" ]]
    then
      cd "./$folder/" || exit 1

      echo "[INFO]: $(pwd) :: building image for ${APIS[$folder]}..."
      docker build -t "$IMAGES_REPOSITORY${APIS[$folder]}:latest" -f "Dockerfile" .

      if [[ "$1" == "push" ]] || [[ "$1" == "--push-all" ]]
      then
        docker push "$IMAGES_REPOSITORY${APIS[$folder]}:latest"
      fi
    else
      echo "[INFO]: skipping ${APIS[$folder]} @ ./api/$folder  (no Dockerfile found)."
  fi
  done
fi

if [[ -n "$1" ]] && [[ "$1" == "--bffs" ]] || [[ "$1" == "--push-all" ]]
then
  cd "$ROOT_DIR" || exit 1
  cd ../bff || exit 1
  ROOT_DIR="$(pwd)"

  echo "[INFO]: Building images for BFF"

  for folder in "${!BACKENDS_FOR_FRONTEDS[@]}"; do
    cd "$ROOT_DIR" || exit 1

    if [[ -f "./$folder/Dockerfile" ]]
    then
      cd "./$folder/" || exit 1

      echo "[INFO]: $(pwd) :: building image for ${BACKENDS_FOR_FRONTEDS[$folder]}..."
      docker build -t "$IMAGES_REPOSITORY${BACKENDS_FOR_FRONTEDS[$folder]}:latest" -f "Dockerfile" .

      if [[ "$1" == "push" ]] || [[ "$1" == "--push-all" ]]
      then
        docker push "$IMAGES_REPOSITORY${BACKENDS_FOR_FRONTEDS[$folder]}:latest"
      fi
    else
      echo "[INFO]: skipping ${BACKENDS_FOR_FRONTEDS[$folder]} @ ./bff/$folder  (no Dockerfile found)."
  fi
  done
fi

echo "[INFO]: ✅ Docker images built successfully."
