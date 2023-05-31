# Projeto tecnico Desenvolvimento

## Projeto do teste


![Teste Case](./doc/diagrama_teste.png)

### Detalhes do teste

Criar uma API de emissão de apólice, a API vai receber um payload (payload_1 ou  payload_2) e de acordo com o produto deve direcionar para o worker que o processa.
Criar um Worker de validação para o produto 111 e outro para o produto 222.

Regras de negocio:
O produto 111 tem dados que são required como endereco do imovel, dados do inquilino, beneficiario.
O produto 222 tem dados que são required como placa do carro, chassis, modelo.
Ao final do processamento precisamos ter salvo no banco de dados as parcelas que o segurado deve pagar.


Payload_1
```JSON
{
    "produto": 111,
    "item":{
        "endereço": {
            "rua": "rua x",
            "numero": 123
        },
        "inquilino":{
            "nome": "jose",
            "CPF": 12345678912
        },
        "beneficiario":{
            "nome": "Imobiliaria X",
            "CNPJ": 12345678912345
        }
    },
    "valores":{
        "precoTotal": 1200.00,
        "parcelas": 6
    }
}
```

Payload_2
```JSON
{
    "produto": 111,
    "item":{
        "placa": "ABC1234",
        "chassis": 123213,
        "modelo": "PORCHE"
    },
    "valores":{
        "precoTotal": 3000.00,
        "parcelas": 12
    }
}
```

# Details of the project
The test is using
 - Flask
 - Marshmallow (for the payload validation)
 - SQLAlchemy (for database modeling and storing data)
 - Pytest to run the tests
 - Docker to build/run the containers (better to use docker-compose with it)
 - Redis for the queue and workers

# To run the project
Just run docker-compose up and the webapp will be up and running with the redis server which provides our queues and workers that consume our queues.

Here are some examples of POSTS based on the explanation of the test:

# Car Payload
```
curl --location 'http://localhost:5000/payload' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=00tvxuk7E8mJs6Lnuh5b7qSU0W9qhYAt' \
--data '{
    "produto": "999",
    "item":{
        "placa": "ABC1234",
        "chassis": 3323232,
        "modelo": "CIVIC"
    },
    "valores":{
        "precoTotal": 3000.00,
        "parcelas": 12
    }
}'
```

# House Payload
```
curl --location 'http://localhost:5000/payload' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=00tvxuk7E8mJs6Lnuh5b7qSU0W9qhYAt' \
--data '{
    "produto": 222,
    "item":{
        "endereço": {
            "rua": "rua x",
            "numero": 123
        },
        "inquilino":{
            "nome": "jose",
            "CPF": "12345678912"
        },
        "beneficiario":{
            "nome": "Imobiliaria X",
            "CNPJ": "12345678912345"
        }
    },
    "valores":{
        "precoTotal": 9999.00,
        "parcelas": 6
    }
}'
```

# To run the tests
Only basic tests were written so, to run them you just write pytest at the terminal, taking in consideration that you must have a virtualenv setup with all dependencies installed.
