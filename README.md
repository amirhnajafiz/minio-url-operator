# Minio URL Operator

![](https://img.shields.io/badge/Language-Python-blue)
![](https://img.shields.io/badge/Storage-Minio-lightgrey)

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

## View

Visit ```localhost```.

![](https://github.com/amirhnajafiz/minio-url-operator/blob/master/assets/Screen%20Shot%201402-04-12%20at%2016.20.33.png)
