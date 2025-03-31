#!/bin/bash

source apis.env.sh

chmod +x build_images.sh

bash build_images.sh

echo "[INFO]: now running the test cases $APIS"

for folder in "${!APIS[@]}"; do
  if [ -d "../api/$folder/test" ]; then
    echo "Running tests for ${APIS[$folder]}..."
    docker run --rm -e PYTHONPATH=/app/src "${APIS[$folder]}:latest" \
      bash -c "pipenv run pytest --cov-config=pytest.ini --cov=src --cov-report=term-missing" || exit 1

      echo "salio anterior con $?"
  fi
done

echo "[INFO]: ✅ All tests completed."
