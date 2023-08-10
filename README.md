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
docker pull amirhossein21/muo:v0.2
```

### environment variables

|         Name         |    Type    | Example              | Description             |
|:--------------------:|:----------:|----------------------|-------------------------|
|   ```HTTP_PORT```    | ```int```  | ```8080```           | HTTP port of MUO API    |
|   ```HTTP_DEBUG```   | ```bool``` | ```true```           | Debug flag for logging  |
|   ```HTTP_HOST```    | ```str```  | ```127.0.0.1```      | Container host name     |
|  ```HTTP_PRIVATE```  | ```bool``` | ```false```          | Private host or not     |
|   ```MYSQL_HOST```   | ```str```  | ```127.0.0.1```      | MySQL cluster host      |
|   ```MYSQL_PORT```   | ```int```  | ```3306```           | MySQL cluster port      |
|   ```MYSQL_USER```   | ```str```  | ```root```           | MySQL user              |
| ```MYSQL_PASSWORD``` | ```str```  | ```pa$$word```       | MySQL pass              |
|    ```MYSQL_DB```    | ```str```  | ```minio-db```       | MySQL database          |
| ```MYSQL_MIGRATE```  | ```bool``` | ```false```          | Database migration      |
|   ```MINIO_HOST```   | ```str```  | ```localhost:9000``` | Minio cluster host      |
|  ```MINIO_SECURE```  | ```bool``` | ```false```          | Secure Minio connection |
|  ```MINIO_ACCESS```  | ```str```  | -                    | Minio access token      |
|  ```MINIO_SECRET```  | ```str```  | -                    | Minio secret token      |


### start

```shell
docker run -d -it \
 -e HTTP_PORT=80 -e HTTP_DEBUG=0 -e MINIO_HOST=localhost:9000 \
 -e MINIO_SECURE=0 -e MINIO_ACCESS=9iWKawYzq68iNMN7MsiU \
 -e MINIO_SECRET=zWwZlmTX56Hr8NYBOpN4ga2zV8oO2ECIjjPHPF20 \
 -e HTTP_HOST=localhost -e HTTP_PRIVATE=1 \
 amirhossein21/muo:v0.2
```

## View

Visit ```localhost```.

![](https://github.com/amirhnajafiz/minio-url-operator/blob/master/assets/Screen%20Shot%201402-04-12%20at%2016.20.33.png)

## API

In order to use the operator APIs, you can read the ```swagger``` documents in [docs](./api/swagger.yaml).
