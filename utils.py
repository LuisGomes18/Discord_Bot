import mysql.connector


def buscar_token(cursor):
    try:
        query_token = "SELECT token FROM `server_testes_bot` WHERE nome_bot = 'Server Testes Bot Official'"
        cursor.execute(query_token)
        token_sem_modificacoes = cursor.fetchone()
        if token_sem_modificacoes:
            token = token_sem_modificacoes[0]
            return token
        else:
            print("No token found in the database.")
            exit(1)
    except mysql.connector.Error as error:
        print('Buscar Token')
        print("Erro ao acessar o banco de dados:", error)
        exit(1)


def carregar_prefixo(cursor):
    try:
        query_prefixo = "SELECT prefixo FROM server_testes_bot WHERE id = 1"
        cursor.execute(query_prefixo)
        prefixo = cursor.fetchone()
        if prefixo:
            return prefixo[0]
        else:
            return None
    except mysql.connector.Error as error:
        print('Erro ao carregar o prefixo')
        print("Erro ao acessar o banco de dados:", error)
        exit(1)


def carregar_boas_vindas(cursor):
    try:
        query_boas_vindas = ("SELECT id_boas_vindas FROM server_testes_bot WHERE nome_bot = 'Server Testes Bot "
                             "Official'")
        cursor.execute(query_boas_vindas)
        boas_vindas = cursor.fetchone()
        if boas_vindas:
            return boas_vindas[0]
        else:
            return None
    except mysql.connector.Error as error:
        print('Erro ao carregar as boas vindas')
        print("Erro ao acessar o banco de dados:", error)
        exit(1)


def carregar_despedidas(cursor):
    try:
        query_despedidas = "SELECT id_despedidas FROM server_testes_bot WHERE nome_bot = 'Server Testes Bot Official'"
        cursor.execute(query_despedidas)
        despedidas = cursor.fetchone()
        if despedidas:
            return despedidas[0]
        else:
            return None
    except mysql.connector.Error as error:
        print('Erro ao carregar as despedidas')
        print("Erro ao acessar o banco de dados:", error)
        exit(1)


def guardar_id_boas_vindas(mydb, cursor, id_boas_vindas):
    try:
        query_guardar_boas_vindas = ("UPDATE server_testes_bot SET id_boas_vindas = %s WHERE nome_bot = 'Server "
                                     "Testes Bot Official'")
        cursor.execute(query_guardar_boas_vindas, (id_boas_vindas,))
        mydb.commit()
    except mysql.connector.Error as error:
        print('Erro ao guardar o ID de boas vindas')
        print("Erro ao acessar o banco de dados:", error)
        exit(1)


def guardar_id_despedidas(mydb, cursor, id_despedidas):
    try:
        query_guardar_despedidas = ("UPDATE server_testes_bot SET id_despedidas = %s WHERE nome_bot = 'Server Testes"
                                    "Bot Official'")
        cursor.execute(query_guardar_despedidas, (id_despedidas,))
        mydb.commit()
    except mysql.connector.Error as error:
        print('Erro ao guardar o ID de despedidas')
        print("Erro ao acessar o banco de dados:", error)
        exit(1)


def carregar_api_key(cursor):
    try:
        query_api_key = "SELECT key_tempo FROM server_testes_bot WHERE nome_bot = 'Server Testes Bot Official'"
        cursor.execute(query_api_key)
        api_key = cursor.fetchone()
        if api_key:
            return api_key[0]
        else:
            return None
    except mysql.connector.Error as error:
        print('Erro ao carregar a chave da API')
        print("Erro ao acessar o banco de dados:", error)
        exit(1)


def guardar_api_key(mydb, cursor, api):
    try:
        query_guardar_api_key = ("UPDATE server_testes_bot SET key_tempo = %s WHERE nome_bot = 'Server Testes Bot "
                                 "Official'")
        cursor.execute(query_guardar_api_key, (api,))
        mydb.commit()
    except mysql.connector.Error as error:
        print('Erro ao guardar a chave da API')
        print("Erro ao acessar o banco de dados:", error)
        exit(1)
