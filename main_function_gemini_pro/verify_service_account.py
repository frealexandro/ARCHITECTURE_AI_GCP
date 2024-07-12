import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import bigquery



class ServiceAccessChecker:

    def __init__(self, credentials_file, project_id):
        self.credentials_file = credentials_file
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file)

    def check_full_access_service_account(self , services):

        #* Autenticarse con la cuenta de servicio
        #*credentials = service_account.Credentials.from_service_account_file(self.credentials)
        
        results = {}
        for service in services:
            try:
                if service == 'compute' or service == 'storage' or service == 'pubsub' or service == 'cloudfunctions':
                
                    #! Construir el cliente de la API del servicio
                    service_client = build(service, 'v1', credentials=self.credentials)
                    
                    # Definir los métodos de prueba para cada servicio
                    if service == 'compute':
                        service_client.zones().list(project=self.project_id).execute()
                    elif service == 'storage':
                        service_client.buckets().list(project=self.project_id).execute()
                    elif service == 'pubsub':
                        service_client.projects().topics().list(project=f'projects/{self.project_id}').execute()
                    elif service == 'cloudfunctions':
                        service_client.projects().locations().functions().list(parent=f'projects/{self.project_id}/locations/-').execute()


                elif service == 'bigquery':
                    client = bigquery.Client(credentials=self.credentials, project=self.project_id)
                    client.query("SELECT 1").result()
                    results[service] = 'Full access'

                else:
                    results[service] = 'Service not supported'
                    continue
                
                results[service] = 'Full access'
            except HttpError as e:
                if e.resp.status in [403, 404]:
                    results[service] = 'No access'
                else:
                    results[service] = f'Error: {e}'
            except Exception as e:
                results[service] = f'Error: {e}'
        
        return results




# def run ():
#     #! path del archivo de credenciales
#     credentials_file = '/home/frealexandro/proyectos_personales/gemini_pro_competition/keys/key_service_account_analitycs_contactica.json'

#     #* code is not necesary for this case 
#     # # find the id of the proyect of the service account
#     # with open(credentials_file) as f:
#     #     credentials_info = json.load(f)
#     #     service_account_email  = credentials_info['client_email']

#     #! find the id of the proyect of the service account
#     with open(credentials_file) as f:
#         credentials_info = json.load(f)
#         project_id  = credentials_info['project_id']

#     services = ['compute', 'storage', 'bigquery', 'pubsub','cloudfunctions']  #! Agrega los servicios que deseas verificar por ahora solo se soportan estos
    
#     access_results = check_full_access_service_account(credentials_file, project_id, services)

#     print(access_results)

# if __name__ == "__main__":
#     run()