# Trandfer-Encrypted

Transfer-Encrypted is a solution to transfer encrypted json file to xml format

## Installation

Use  [docker-compose](https://docs.docker.com/compose/compose-file/) to run Transfer-Encrypted

Command has to be executed in same directory of docker-compose file
```bash
docker-compose build
docker-compose up
```

## Usage

Any json file inputed in folder dataJson will be transformed to XML, encrypted, transfer to folder dataXml and decrypted

## Limitations
It has to put one file per time
Empty files are note converted neither transfered

