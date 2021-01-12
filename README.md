# match-app


## 以下、awsの管理画面に書いてあるプッシュコマンド
### aws-cli login
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin xxxxxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com

### aws-cli tag
docker tag match-app_toukare:latest xxxxxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/[reponame]:latest

### aws-cli push
docker push xxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/[reponame]:latest
