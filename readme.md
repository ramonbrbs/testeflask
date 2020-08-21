#Teste Shipay
***
## Teste 1

* Aplicação FLASK configurada com Docker e MongoDB
* Testes feitos com Unittest (rodar como *python -m unittest discover*)

### Utilização
A aplicação valida se existe o cnpj cadastrado para confirmar as transações. Por isso é necessário rodar o seed antes
 de submeter requisições para que elas sejam aceitas:
```
export FLASK_APP=main.py
flask seed
``` 

Isto irá criar o estabelecimento com as seguintes informações:
````json
{
    "nome": "Nosso Restaurante de Todo Dia LTDA",
    "cnpj": "45.283.163/0001-67",
    "dono": "Fabio I.",
    "telefone": "11909000300"
}
````

As requisições são respondidas através do padrão definido _/v1/transacao_


## Teste 2

* Repartir o código diminuindo a responsabilidade de cada uma das partes do código
* Utilizar um padrão de serviços (*services*) para desacoplar operações como construção de planilhas
* Utilizar um padrão de repositórios (*repositories*) para desacoplar a persistência de dados
* Utilizar um arquivo de configuração (como config.py) para manter variáveis globais utilizadas.