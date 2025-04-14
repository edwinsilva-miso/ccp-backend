#!/bin/bash

for arg in "$@"
do
  case "$arg" in
    --apis)
      GEN_APIS=true
      ;;
    --bffs)
      GEN_BFFS=true
      ;;
    --push-all)
      PUSH_ALL=true
      ;;
    --push-all-from-local)
      PUSH_ALL_LOCAL=true
      ;;
    --minikube)
      MINIKUBE=true
      ;;
    --specific=*)
      SPECIFIC="${arg#*=}"
      ;;
    *)
      echo "unknown parameter: $arg"
      exit 1
      ;;
  esac
done

if [[ -n "$MINIKUBE" ]]
then
  echo "[INFO]: ✅ deleting all unused existing images"
  minikube ssh -- docker rmi -f $(docker images -q)
  minikube ssh -- docker image prune -af
fi



source automation.env.sh

if [[ -n "$PUSH_ALL" ]]
then
  export DOCKER_PATH="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/"
fi

if [[ -n "$PUSH_ALL_LOCAL" ]]
then
  echo "[INFO]: loading secrets in local"
  source ./secrets/secrets.env.sh
  export DOCKER_PATH="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/"
  PUSH_ALL=true
fi


cd ../api || exit 1
ROOT_DIR="$(pwd)"

export APIS



TIMESTAMP="$(date +%Y%m%d%H%M%S)"

if [[ -n "$GEN_APIS" || -n "$PUSH_ALL" ]]
then
  echo "========================================================================"
  echo "[INFO]: Building docker images for APIs"
  echo "========================================================================"

  for folder in "${!APIS[@]}"; do
    cd "$ROOT_DIR" || exit 1

    if [[ -n "$SPECIFIC" && "$SPECIFIC" != "${APIS[$folder]}" ]]
    then
      continue
    fi

    if [[ -f "./$folder/Dockerfile" ]]
    then
      UUID="$(find "./$folder/" -type f -exec sha256sum {} + | sort | sha256sum | cut -c1-6)"
      cd "./$folder/" || exit 1
      VERSION="$(xargs < "version.txt")"

      echo "========================================================================"
      echo "[INFO]: $(pwd) :: building image for ${APIS[$folder]}..."
      echo "========================================================================"
      docker build -t "$DOCKER_PATH${APIS[$folder]}:latest" -f "Dockerfile" .

      if [[ -n "$MINIKUBE" ]]
      then
        echo "========================================================================"
        echo "[INFO]: loading image into minikube"
        echo "========================================================================"
        minikube image load "$DOCKER_PATH${APIS[$folder]}:latest"
      fi

      if [[ -n "$DOCKER_PATH" ]]
      then
        docker tag "$DOCKER_PATH${APIS[$folder]}:latest" "$DOCKER_PATH${APIS[$folder]}:$VERSION-$UUID-$TIMESTAMP"
      fi

      if [[ -n "$PUSH_ALL" ]]
      then
        docker push "$DOCKER_PATH${APIS[$folder]}:latest" || exit 1
        docker push "$DOCKER_PATH${APIS[$folder]}:$VERSION-$UUID-$TIMESTAMP" || exit 1
      fi
    else
      echo "========================================================================"
      echo "[INFO]: skipping ${APIS[$folder]} @ ./api/$folder  (no Dockerfile found)."
      echo "========================================================================"
  fi
  done
fi




if [[ -n "$GEN_BFFS" || -n "$PUSH_ALL" ]]
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
      docker build -t "$DOCKER_PATH${BACKENDS_FOR_FRONTEDS[$folder]}:latest" -f "Dockerfile" .

      if [[ -n "$MINIKUBE" ]]
      then
        echo "========================================================================"
        echo "[INFO]: loading image into minikube"
        echo "========================================================================"
        minikube image load "$DOCKER_PATH${BACKENDS_FOR_FRONTEDS[$folder]}:latest"
      fi

      if [[ -n "$DOCKER_PATH" ]]
      then
        docker tag "$DOCKER_PATH${BACKENDS_FOR_FRONTEDS[$folder]}:latest" "$DOCKER_PATH${BACKENDS_FOR_FRONTEDS[$folder]}:$VERSION-$UUID-$TIMESTAMP"
        docker push "$DOCKER_PATH${BACKENDS_FOR_FRONTEDS[$folder]}:$VERSION-$UUID-$TIMESTAMP" || exit 1
      fi

      if [[ -n "$PUSH_ALL" ]]
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

if [[ -n "$MINIKUBE" ]]
then
  echo "[INFO]: ✅ inspecting what images are inside minikube"
  minikube ssh -- docker images
fi
