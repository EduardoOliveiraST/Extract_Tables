from get_audiences import auth_api, remove_aud
import sqlite3
import pandas as pd
import os
import time
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR')

def registrar_audiencia(nome_arquivo, audience_name):
    agora = datetime.now()
    data_audiencia = agora.strftime("%A, %d de %B de %Y %H:%M:%S")
    try:
        # Tenta abrir o arquivo para leitura e escrita
        with open(nome_arquivo, 'r+') as arquivo:
            # Lê o conteúdo atual
            conteudo = arquivo.read()

            # Verifica se a audiência já foi registrada
            if audience_name in conteudo:
                print(f'A audiência {audience_name} já foi registrada.')
                return True
            else:
                # Move o ponteiro para o início do arquivo para permitir a escrita
                arquivo.seek(0)

                # Escreve o conteúdo existente e a nova linha com a audiência
                arquivo.write(conteudo + f'{audience_name} - {data_audiencia}\n')

                print(f'Audiência {audience_name} registrada com sucesso.')

    except FileNotFoundError:
        # Se o arquivo não existir, cria um novo e escreve a linha com a audiência
        with open(nome_arquivo, 'w') as arquivo:
            print(f'Audiência {audience_name} registrada com sucesso.')
            arquivo.write(f'{audience_name} - {data_audiencia}\n')


nome_arquivo = 'registro_audiencias.txt'

out_path = 'C:/Users/EduardoOliveira/Scripts/raw_data/'
databases_path = 'C:/Users/EduardoOliveira/Scripts/Api_Edu/Upload_Audience/ext/databases/'


cont = 0
execution = True
response_json = auth_api()

if response_json['Created_Audiences']:
    for audiencia in response_json['Created_Audiences']:
        cont += 1
        audience_created = registrar_audiencia(nome_arquivo, audiencia['audience_name'])
        time.sleep(2)
        if not audience_created:
            try:
                if os.path.exists(f'{databases_path}{audiencia["db_name"]}.db'):
                    with sqlite3.connect(f'{databases_path}{audiencia["db_name"]}.db') as conn:
                        cursor = conn.cursor()
                        query = f"SELECT * FROM {audiencia['table_name']}"
                        cursor.execute(query)
                        existing_entry = cursor.fetchall()
                        if existing_entry:
                            df = pd.read_sql(query, conn)
                            df.to_csv(out_path + audiencia["audience_name"] + ".csv", header=True, sep=',', encoding='utf-8')
                            remove_aud(audiencia["audience_id"])
                else:
                    print('Database inexistente', audiencia["db_name"])
                    
            except Exception as e:
                if 'no such table' in e.args[0]:
                    remove_aud(audiencia["audience_id"])
                    print('Tabela inexistente')
else:
    print('Não há audiência a ser processada.')

print("Execução concluída.")