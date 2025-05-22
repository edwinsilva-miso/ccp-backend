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
    docker run --rm -e PYTHONPATH=/app/src "${APIS[$folder]}:latest" \
      bash -c "pipenv run pytest --cov-config=pytest.ini --cov=src --cov-report=term-missing"
  fi
done

echo "[INFO]: ✅ All tests completed."
