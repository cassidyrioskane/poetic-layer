
---

## `Makefile`

```makefile
.PHONY: up down build test

up:
\tdocker-compose up --build

down:
\tdocker-compose down -v

build:
\tdocker-compose build

test:
\tpytest -v
