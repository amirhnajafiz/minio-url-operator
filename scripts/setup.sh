#!/usr/bin/env bash

# AKIAIOSFODNN7EXAMPLE
# wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

HTTP_PORT=8080 HTTP_DEBUG=True \
  MINIO_HOST=localhost:9000 MINIO_ACCESS=CDcJUoJ1RyF6lT8k2Jpk \
  MINIO_SECRET=oqZnjItFQSnOURApT1Y42UxGSG9nRDgZWPI0OGGV \
  MINIO_SECURE=False \
  SQL_HOST=database/sql.db \
  python3 script.py
