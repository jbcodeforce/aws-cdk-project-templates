 "Echo build it"
quarkus build
docker -f ../Dockerfile -t $ECR_PATH:$APP_NAME:latest .
docker push $ECR_PATH:$APP_NAME:latest