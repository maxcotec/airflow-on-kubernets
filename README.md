# Airflow on Kubernetes
Run Airflow on Kubernetes. This repository contains scripts to;
1) run a multi-node kubernets cluster on local machine using KinD
2) prepare Dockerfile for your airflow dags 
3) minimal helm chart required to run airflow on kubernetes using Kubernetes Executor

Watch video tutorial here
https://youtu.be/RqSYh3UI_Is

## Prerequisites 
Prior knowledge on Airflow as well as Kubernetes is a must. 

Airflow tutorials: https://www.youtube.com/playlist?list=PLzKRcZrsJN_xcKKyKn18K7sWu5TTtdywh

Articles: 
1. https://maxcotec.com/apache-airflow-architecture
2. https://maxcotec.com/blog/apache-airflow-2-docker-beginners-guide/

## Requirements 

kind: https://kind.sigs.k8s.io/docs/user/quick-start/#installation 

kubectl: https://kubernetes.io/docs/tasks/tools

k9s: https://k9scli.io/topics/install

docker: https://docs.docker.com/get-docker

###  Tools version used in this tutorial: 
kind: v0.14.0

k9s: 0.25.18

kubectl: Client Version: version.Info{Major:"1", Minor:"23", GitVersion:"v1.23.4", GitCommit:"e6c093d87ea4cbb530a7b2ae91e54c0842d8308a", GitTreeState:"clean", BuildDate:"2022-02-16T12:30:48Z", GoVersion:"go1.17.6", Compiler:"gc", Platform:"darwin/arm64"}

Docker desktop: 4.10.1

## Run Instructions

1. create kubernets cluster. Run bash script `create_cluster_with_registry.sh` from directory kind_cluster/
2. write your own dag and place it inside `airflow-dags/dags` directory. Then build docker file `docker build . -t airflow_dags:0.1.0`
3. tag the image with local docker registry host `docker tag airflow_dags:0.1.0 localhost:5001/airflow_dags:0.1.0`
4. push the airflow image to local docker registry `docker push localhost:5001/airflow_dags:0.1.0`
5. deploy helm chart `helm upgrade --install airflow . --values values.yaml --set airflow.dags_image.repository=localhost/airflow_dags --set airflow.dags_image.tags=0.1.0`