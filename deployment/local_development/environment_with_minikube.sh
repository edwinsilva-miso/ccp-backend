#!/bin/bash

for arg in "$@"
do
  case "$arg" in
    --force)
      FORCE=true
      ;;
    --prod)
      PROD=prod
      ;;
    *)
      echo "unknown parameter: $arg"
      exit 1
      ;;
  esac
done

if [[ -z "$PROD" ]]
then
  if ! minikube status
  then
    minikube start
    minikube addons enable ingress
  fi
else
  source ../secrets/secrets.env.sh
  DOCKER_PATH="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/"
fi

kubectl apply -f ../configurations.yml
kubectl apply -f ../secrets/secrets.yml


function build_image() {
  SRC_PATH="$1"
  COMPONENT="$2"
  DEPLOYMENT="$3"

  SHA256="$(find "$SRC_PATH" \
    -type d -name '.idea' -prune -o \
    -type f ! -name 'checksum.txt' -print \
    -type f ! -name 'Pipfile.lock' -print \
    | sort \
    | xargs sha256sum \
    | sort \
    | sha256sum \
    | awk '{print $1}'
  )"
  EXISTING_SHA256="$( [ -f "$SRC_PATH/checksum.txt" ] && xargs < "$SRC_PATH/checksum.txt" || echo "" )"

  echo "computed_checksum::\`$SHA256\` --- existing_checksum::\`$EXISTING_SHA256\`"

  if [[ "$SHA256" != "$EXISTING_SHA256" ]] || [[ -n "$FORCE" ]]
  then
    echo "[INFO]: there are new changes detected inside the folder \`$COMPONENT\` for $DEPLOYMENT"

    echo "$SHA256" > "$SRC_PATH/checksum.txt"

    TIMESTAMP="$(date +%Y%m%d%H%M%S)"
    UUID="$(find "$SRC_PATH" -type f -exec sha256sum {} + | sort | sha256sum | cut -c1-6)"
    VERSION="$(xargs < "$SRC_PATH/version.txt")"

    docker build -t "$DOCKER_PATH$DEPLOYMENT:latest" -f "$SRC_PATH/Dockerfile" "$SRC_PATH"
    docker tag "$DOCKER_PATH$DEPLOYMENT:latest" "$DOCKER_PATH$DEPLOYMENT:$VERSION-$UUID-$TIMESTAMP"

    if [[ -z "$PROD" ]]
    then
      minikube image load "$DEPLOYMENT:latest"
      minikube image load "$DEPLOYMENT:$VERSION-$UUID-$TIMESTAMP"
    else
      docker push "$DOCKER_PATH$DEPLOYMENT:latest"
      docker push "$DOCKER_PATH$DEPLOYMENT:$VERSION-$UUID-$TIMESTAMP"
    fi

    sleep 2

    if ! kubectl get deployment "$DEPLOYMENT" -n default &> /dev/null
    then
      if [[ -z "$PROD" ]]
      then
        kubectl apply -f "$SRC_PATH/k8s/minikube"
      else
        kubectl apply -f "$SRC_PATH/k8s/cloud"
      fi
      sleep 5
    fi

    kubectl set image deployment/"$DEPLOYMENT" "$DEPLOYMENT=$DOCKER_PATH$DEPLOYMENT:$VERSION-$UUID-$TIMESTAMP"

  else
    echo "[INFO]: no changes in the folder \`$COMPONENT\` for $DEPLOYMENT"
  fi
}

set -e

echo "[INFO]: ✅ deleting all unused existing images"

source ../automation.env.sh || exit 1

export APIS
export BACKENDS_FOR_FRONTEDS

# gather the information about the software backplane-components that
# need new images to be created and deployed (if they have new changes)
COMPONENTS_JSON="$(cat "$(pwd)"/software_components.json)"
CURRENT_DIR="$(pwd)"

# fetch all BFFs
BFF_ARRAY="$(echo "$COMPONENTS_JSON" | jq -r '.bffs[]')"
for bff in $BFF_ARRAY
do
  echo "[INFO]: bff \`$bff\`"

  build_image "../../bff/$bff" "$bff" "${BACKENDS_FOR_FRONTEDS[$bff]}"
done


# fetch all APIs
APIS_ARRAY="$(echo "$COMPONENTS_JSON" | jq -r '.apis[]')"
for api in $APIS_ARRAY
do
  echo "[INFO]: api \`$api\`"

  build_image "../../api/$api" "$api" "${APIS[$api]}"
done


# fetch all backplane-components
cd ../backplane-components || exit 1

BACKPLANE_ARRAY="$(echo "$COMPONENTS_JSON" | jq -r '."backplane-components"[]')"
for component in $BACKPLANE_ARRAY
do
  echo "[INFO]: backplane component \`$component\`"
done
