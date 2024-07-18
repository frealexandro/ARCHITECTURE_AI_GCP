import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel,Part



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

                elif service == 'gemini':
                    
                    vertexai.init(project=self.project_id , location="us-central1")
                    model = GenerativeModel("gemini-1.5-pro-001")
                    response = model.generate_content("Hello, Gemini!")
                    if response.text:
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


