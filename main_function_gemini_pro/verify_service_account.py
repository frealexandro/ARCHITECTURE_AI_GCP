import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import bigquery

# def check_full_access_service_account(credentials_file, project_id, services):
#     #! Autenticarse con la cuenta de servicio
#     credentials = service_account.Credentials.from_service_account_file(credentials_file)
    
#     results = {}
#     for service in services:
#         try:
#             #! Construir el cliente de la API del servicio
#             service_client = build(service, 'v1', credentials=credentials)
            
#             # Definir los métodos de prueba para cada servicio
#             if service == 'compute':
#                 service_client.zones().list(project=project_id).execute()
#             elif service == 'storage':
#                 service_client.buckets().list(project=project_id).execute()
#             elif service == 'bigquery':
#                 client = bigquery.Client(credentials=credentials, project=project_id)
#                 client.query("SELECT 1").result()
#             elif service == 'pubsub':
#                 service_client.projects().topics().list(project=f'projects/{project_id}').execute()
#             else:
#                 results[service] = 'Service not supported'
#                 continue
            
#             results[service] = 'Full access'
#         except HttpError as e:
#             if e.resp.status in [403, 404]:
#                 results[service] = 'No access'
#             else:
#                 results[service] = f'Error: {e}'
#         except Exception as e:
#             results[service] = f'Error: {e}'
    
#     return results



def list_service_account_permissions(credentials_file, service_account_email,project_id):
    
    # Autenticarse con la cuenta de servicio
    credentials = service_account.Credentials.from_service_account_file(credentials_file)

    try:
        # Construir el cliente de la API de IAM
        iam_service = build('iam', 'v1', credentials=credentials)
        
        # Obtener los roles asignados a la cuenta de servicio
        request = iam_service.projects().serviceAccounts().getIamPolicy(
            resource=f'projects/{project_id}/serviceAccounts/{service_account_email}'
        )
        response = request.execute()
        
        print(response)
        # Extraer los roles de la política de IAM
        #roles = [binding['role'] for binding in response['bindings'] if 'members' in binding and f'serviceAccount:{service_account_email}' in binding['members']]
        
        # Construir el cliente de la API de Cloud Resource Manager
        #crm_service = build('cloudresourcemanager', 'v1', credentials=credentials)
        
        # Obtener los permisos para cada rol
        # permissions = {}
        # for role in roles:
        #     role_name = role.split('/')[-1]
        #     request = crm_service.roles().get(name=role)
        #     response = request.execute()
        #     permissions[role_name] = response['includedPermissions']
        
        return response

    except HttpError as e:
        return f'Error: {e}'
    except Exception as e:
        return f'Error: {e}'





def run ():
    #! path del archivo de credenciales
    credentials_file = '/home/frealexandro/proyectos_personales/gemini_pro_competition/keys/key_service_account_analitycs_contactica.json'


    #! find the id of the proyect of the service account
    with open(credentials_file) as f:
        credentials_info = json.load(f)
        service_account_email  = credentials_info['client_email']

    #! find the id of the proyect of the service account
    with open(credentials_file) as f:
        credentials_info = json.load(f)
        project_id  = credentials_info['project_id']

    #services = ['compute', 'storage', 'bigquery', 'pubsub']  # Agrega los servicios que deseas verificar
    
    #access_results = check_full_access_service_account(credentials_file, project_id, services)


    permissions = list_service_account_permissions(credentials_file, service_account_email,project_id)

    print(json.dumps(permissions, indent=2))
    


if __name__ == "__main__":
    run()