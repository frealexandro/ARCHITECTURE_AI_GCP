
#all: primera funcion para crear la descripcion del pipeline tenuiendo en cuenta que la service account ya esdta logueada en el entorno 

from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerativeModel,Part
import re
import os
from cloud_storage import CloudStorageManager



#all: Ruta al archivo de clave de la cuenta de servicio
key_path = "/home/frealexandro/proyectos_personales/gemini_pro_competition/keys/key_service_account_analitycs_contactica.json"


#all : cargar la cuenta de servicio en el sistema con os esta se encuentra ya cargada en la variable key_path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path


#* ejemplo de como se puede inicializar el proyecto y la ubicacion con las credenciales de la cuenta de servicio
# vertexai.init(project="datalake-analytics-339922", location="us-central1", credentials=credentials)





def run ():

    #!################################################################
    #!inicio del primer prompt para la descripcion de la arquitectura
    
    # all: Crear un objeto de la clase CloudStorageManager
    cloud_storage_manager = CloudStorageManager()

    # all: leer el archivo de la primera arquitectura
    path_image = "gemini_pro_competition/images/arquitectura_inicial.png"

    # all: usar el metodo upload_blob para subir un archivo a un bucket
    cloud_storage_manager.upload_blob("gemini_pro", path_image , 'arquitectura_inicial.png' )

    


if __name__ == "__main__":
    run ()