#!/usr/bin/env bash

HTTP_PORT=8080 HTTP_DEBUG=True \
  SQL_HOST=database/sql.db \
  python migrate.py "$1"
