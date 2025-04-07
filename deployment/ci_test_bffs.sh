#!/bin/bash

export PROJECT_ID
export REGION
export REPOSITORY

source automation.env.sh

chmod +x build_images.sh

bash build_images.sh --bffs

echo "[INFO]: now running the test cases $BACKENDS_FOR_FRONTEDS"

for folder in "${!BACKENDS_FOR_FRONTEDS[@]}"; do
  if [ -d "../bff/$folder/test" ]; then
    echo "Running tests for ${BACKENDS_FOR_FRONTEDS[$folder]}..."
    docker run --rm -e PYTHONPATH=/app/src "${BACKENDS_FOR_FRONTEDS[$folder]}:latest" \
      bash -c "pipenv run pytest --cov-config=pytest.ini --cov=src --cov-report=term-missing" || exit 1
  fi
done

echo "[INFO]: ✅ All tests completed."
