# Minio URL Operator

![](https://img.shields.io/badge/Language-Python-blue)
![](https://img.shields.io/badge/Storage-Minio-lightgrey)
![GitHub release (with filter)](https://img.shields.io/github/v/release/amirhnajafiz/minio-url-operator)


URL operator for Minio shared objects links. Since Minio object storage provides
urls for sharing objects with a maximum 7 days limit, you can use this operator
in order to have live urls for every object that you want.
With this operator, you can create a persistent url for your objects in Minio.

## Start

You can use ```docker``` image of MUP in order to setup the operator on ```Docker``` or ```Kubernetes```.

### image

```shell
docker pull amirhossein21/muo:macos.v0.1
```

### environment variables

|        Name        |   Type    | Values               | Usage                               |
|:------------------:|:---------:|----------------------|-------------------------------------|
|  ```HTTP_PORT```   | ```int``` | -                    | HTTP port of MUO API                |
|  ```HTTP_DEBUG```  | ```int``` | ```0,1```            | Debug flag for logging (0 is True)  |
|  ```MINIO_HOST```  | ```str``` | ```localhost:9000``` | Minio cluster host                  |
| ```MINIO_SECURE``` | ```int``` | ```0,1```            | Secure Minio connection (0 is True) |
| ```MINIO_ACCESS``` | ```str``` | -                    | Minio access token                  |
| ```MINIO_SECRET``` | ```str``` | -                    | Minio secret token                  |
|  ```HTTP_HOST```   | ```str``` | -                    | Container host name                 |
| ```HTTP_PRIVATE``` | ```int``` | ```0,1```            | Private host or not (1 is False)    |


### start

```shell
docker run -d -it \
 -e HTTP_PORT=80 -e HTTP_DEBUG=0 -e MINIO_HOST=localhost:9000 \
 -e MINIO_SECURE=0 -e MINIO_ACCESS=9iWKawYzq68iNMN7MsiU \
 -e MINIO_SECRET=zWwZlmTX56Hr8NYBOpN4ga2zV8oO2ECIjjPHPF20 \
 -e HTTP_HOST=localhost -e HTTP_PRIVATE=1 \
 -v muo-volume:/app/database/sql.db \
 amirhossein21/muo:macos.v0.1
```

#### sql.db

Since the application is using ```SQLite3``` for storing objects data, make sure to run
the migrate script before starting the container. You can create a volume for ```database/sql.db```
in order to save the storage.

## View

Visit ```localhost```.

![](https://github.com/amirhnajafiz/minio-url-operator/blob/master/assets/Screen%20Shot%201402-04-12%20at%2016.20.33.png)

## API

In order to use the operator APIs, you can read the ```swagger``` documents in [docs](./docs/swagger.yaml).
