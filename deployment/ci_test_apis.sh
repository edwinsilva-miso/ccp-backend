#!/bin/bash

export PROJECT_ID
export REGION
export REPOSITORY

source automation.env.sh

chmod +x build_images.sh

bash build_images.sh --apis

echo "[INFO]: now running the test cases $APIS"

for folder in "${!APIS[@]}"; do
  if [ -d "../api/$folder/test" ]; then
    echo "Running tests for ${APIS[$folder]}..."
    if ! docker run --rm -e PYTHONPATH=/app/src "${APIS[$folder]}:latest" \
      bash -c "pipenv run pytest --cov-config=pytest.ini --cov=src --cov-report=term-missing"
    then
      echo '[ERROR]: comamnd docker run --rm -e PYTHONPATH=/app/src "<image>:latest" bash -c "pipenv run pytest --cov-config=pytest.ini --cov=src --cov-report=term-missing" | has failed'
      echo "[INFO]: fix test cases for [[$folder]]"
      exit 1
    fi
  fi
done

echo "[INFO]: ✅ All tests completed."
