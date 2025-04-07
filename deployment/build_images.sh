#!/bin/bash

source automation.env.sh

if [[ "$1" == "--push-all" ]]
then
  export DOCKER_PATH="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/"
fi

if [[ -n "$1" ]]
then
  source ./secrets/secrets.env.sh
fi


cd ../api || exit 1
ROOT_DIR="$(pwd)"

export APIS



TIMESTAMP="$(date +%Y%m%d%H%M%S)"

if [[ "$1" == "--apis" || "$1" == "--push-all" ]]
then
  echo "========================================================================"
  echo "[INFO]: Building docker images for APIs"
  echo "========================================================================"

  for folder in "${!APIS[@]}"; do
    cd "$ROOT_DIR" || exit 1

    if [[ -f "./$folder/Dockerfile" ]]
    then
      UUID="$(find "./$folder/" -type f -exec sha256sum {} + | sort | sha256sum | cut -c1-6)"
      cd "./$folder/" || exit 1
      VERSION="$(xargs < "version.txt")"

      echo "========================================================================"
      echo "[INFO]: $(pwd) :: building image for ${APIS[$folder]}..."
      echo "========================================================================"
      docker build -t "$DOCKER_PATH${APIS[$folder]}:latest" "$DOCKER_PATH${APIS[$folder]}:$VERSION-$UUID-$TIMESTAMP" -f "Dockerfile" .

      if [[ "$1" == "push" || "$1" == "--push-all" ]]
      then
        docker push "$DOCKER_PATH${APIS[$folder]}:latest" || exit 1
      fi
    else
      echo "========================================================================"
      echo "[INFO]: skipping ${APIS[$folder]} @ ./api/$folder  (no Dockerfile found)."
      echo "========================================================================"
  fi
  done
fi




if [[ "$1" == "--bffs" || "$1" == "--push-all" ]]
then
  cd "$ROOT_DIR" || exit 1
  cd ../bff || exit 1
  ROOT_DIR="$(pwd)"

  echo "========================================================================"
  echo "[INFO]: Building images for BFF"
  echo "========================================================================"

  for folder in "${!BACKENDS_FOR_FRONTEDS[@]}"; do
    cd "$ROOT_DIR" || exit 1

    if [[ -f "./$folder/Dockerfile" ]]
    then
      UUID="$(find "./$folder/" -type f -exec sha256sum {} + | sort | sha256sum | cut -c1-6)"
      cd "./$folder/" || exit 1

      VERSION="$(xargs < "version.txt")"

      echo "========================================================================"
      echo "[INFO]: $(pwd) :: building image for ${BACKENDS_FOR_FRONTEDS[$folder]}..."
      echo "========================================================================"
      docker build -t "$DOCKER_PATH${BACKENDS_FOR_FRONTEDS[$folder]}:latest" "$DOCKER_PATH${APIS[$folder]}:$VERSION-$UUID-$TIMESTAMP" -f "Dockerfile" .

      if [[ "$1" == "push" || "$1" == "--push-all" ]]
      then
        docker push "$DOCKER_PATH${BACKENDS_FOR_FRONTEDS[$folder]}:latest" || exit 1
      fi
    else
      echo "========================================================================"
      echo "[INFO]: skipping ${BACKENDS_FOR_FRONTEDS[$folder]} @ ./bff/$folder  (no Dockerfile found)."
      echo "========================================================================"
  fi
  done
fi


echo "[INFO]: ✅ Docker images built successfully."
