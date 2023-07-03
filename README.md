# Minio URL Operator

![](https://img.shields.io/badge/Language-Python-blue)
![](https://img.shields.io/badge/Storage-Minio-lightgrey)

URL operator for Minio shared objects links. Since Minio object storage provides
urls for sharing objects with a maximum 7 days limit, you can use this operator
in order to have live urls for every object that you want.
With this operator, you can create a persistent url for your objects in Minio.

## Start

```shell
sudo HTTP_PORT=80 HTTP_DEBUG=0 MINIO_HOST=localhost:9000 \
 MINIO_SECURE=0 MINIO_ACCESS=9iWKawYzq68iNMN7MsiU \
 MINIO_SECRET=zWwZlmTX56Hr8NYBOpN4ga2zV8oO2ECIjjPHPF20 \
 HTTP_HOST=localhost HTTP_PRIVATE=1 \
 python3 main.py
```