#!/bin/bash

kubectl apply -f secrets/secrets.yml
kubectl delete -f configurations.yml

echo "[INFO]: deploying all the api components"
cd ../api || exit 1

kubectl delete -f usuarios-api/k8s
kubectl delete -f rutas-api/k8s

echo "[INFO]: deploying backend for frontends"
cd ../bff || exit 1

kubectl delete -f web-bff/k8s
kubectl delete -f mobile-bff/k8s
