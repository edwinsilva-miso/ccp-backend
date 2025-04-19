#!/bin/bash

kubectl apply -f secrets-configuration.yml
kubectl apply -f configurations.yml

echo "[INFO]: deploying all the api components"
cd ../api || exit 1

kubectl apply -f usuarios-api/k8s
kubectl apply -f rutas-api/k8s

echo "[INFO]: deploying backend for frontends"
cd ../bff || exit 1

kubectl apply -f web-bff/k8s
kubectl apply -f mobile-bff/k8s
