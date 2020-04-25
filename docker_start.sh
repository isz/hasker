#!/bin/sh

# docker run --rm -it -p 8000:8000 -v $(pwd):/usr/local/hasker hasker /bin/bash

docker run --rm -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -v hasker_db:/var/lib/postgresql/data postgres