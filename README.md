# Currency converter test task

## To run the project in docker:

1. clone this project by **git clone git@github.com:burbaljaka/currency_converter.git**
2. execute: docker-compuse up -build
3. execute: docker exec -it currency_converter-app-1 alembic upgrade head

Call **/base_rates_upload/** endpoint to upload sample data to the database

Open http://localhost:8099/docs# to navigate through all available endpoints
