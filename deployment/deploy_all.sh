#!/bin/bash

kubectl apply -f secrets/secrets.yml
kubectl apply -f configurations.yml

kubectl apply -f backplane-components/rabbitmq/k8s

echo "[INFO]: deploying all the api components"
cd ../api || exit 1

kubectl apply -f usuarios-api/k8s/cloud
kubectl rollout restart deployment users-api

kubectl apply -f rutas-api/k8s/cloud
kubectl rollout restart deployment routes-api

kubectl apply -f clientes-api/k8s/cloud
kubectl rollout restart deployment customers-api

kubectl apply -f pedidos-api/k8s/cloud
kubectl rollout restart deployment orders-api

kubectl apply -f productos-api/k8s/cloud
kubectl rollout restart deployment products-api

kubectl apply -f fabricantes-api/k8s/cloud
kubectl rollout restart deployment manufacturers-api

echo "[INFO]: deploying backend for frontends"
cd ../bff || exit 1

kubectl apply -f web-bff/k8s/cloud
kubectl rollout restart deployment web-bff

kubectl apply -f mobile-bff/k8s/cloud
kubectl rollout restart deployment mobile-bff
