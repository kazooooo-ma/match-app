# match-app

## docker build
- in dev
```
  docker-compose build
```
- run py
```
  docker-compose -f docker-compose.yml -f docker-compose-prd.yml build
```
## docker up
- in dev
```
  docker-compose up -d
  ```
- run py
  ```
  docker-compose -f docker-compose.yml -f docker-compose-prd.yml up -d
```
