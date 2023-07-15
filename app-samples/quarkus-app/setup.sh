
echo "Get AWS information"

export ACCOUNT_ID=$(aws sts  get-caller-identity --query Account --output text)
export REGION=$(aws configure get region)
export ECR_PATH=$ACCOUNT_ID".dkr.ecr."$REGION".amazonaws.com"
export APP_NAME=demo-customer-api

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ECR_PATH
aws ecr create-repository --repository-name demo-customer-api

if [[ -z "$(quarkus version)" ]]
then
    echo "install Quarkus CLI"
    curl -Ls https://sh.jbang.dev | bash -s - trust add https://repo1.maven.org/maven2/io/quarkus/quarkus-cli/
    curl -Ls https://sh.jbang.dev | bash -s - app install --fresh --force quarkus@quarkusio
else
    quarkus version
fi

if [[ -d $APP_NAME ]]
then
    echo $APP_NAME already exist
    cd $APP_NAME
else
    echo "Create the app: "$APP_NAME
    quarkus create app com.acme:$APP_NAME:1.0
    cd $APP_NAME
    quarkus ext add smallrye-health
fi


open http://localhost:8080
quarkus dev


