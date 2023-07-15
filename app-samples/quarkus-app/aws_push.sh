 "Echo build it"
quarkus build
docker -f src/main/docker/Dockerfile.jvm -t $ECR_PATH:$APP_NAME:latest .
docker push $ECR_PATH:$APP_NAME:latest