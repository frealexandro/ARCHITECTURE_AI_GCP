
#all: primera funcion para crear la descripcion del pipeline tenuiendo en cuenta que la service account ya esdta logueada en el entorno 
from langchain.chains import SimpleChain
from langchain.prompts import PromptTemplate
from google.oauth2 import service_account
import re
import os

#all: importar la clase CloudStorageManager
from cloud_storage import CloudStorageManager

#all: importar la clase GeminiOperations
from gemini_operations import GeminiOperations

#all: importar la clase PromptTemplate
from templates_prompts import Prompts





#all: Ruta al archivo de clave de la cuenta de servicio
key_path = "/home/frealexandro/proyectos_personales/gemini_pro_competition/keys/key_service_account_analitycs_contactica.json"


#all : cargar la cuenta de servicio en el sistema con os esta se encuentra ya cargada en la variable key_path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path


#* ejemplo de como se puede inicializar el proyecto y la ubicacion con las credenciales de la cuenta de servicio
# vertexai.init(project="datalake-analytics-339922", location="us-central1", credentials=credentials)








def run ():

    #!################################################################
    #!subir la imagen de la arquitectura inicial a un bucket de google cloud storage


    # all: Crear un objeto de la clase CloudStorageManager
    cloud_storage_manager = CloudStorageManager()

    # all: leer el archivo de la primera arquitectura
    path_image = "/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/images_architectures/arquitectura_inicial.png"

    # all: usar el metodo upload_blob para subir un archivo a un bucket
    cloud_storage_manager.upload_blob("gemini_pro", path_image , 'arquitectura_inicial.png' )

    #!################################################################
    #!inicio del proceso de generacion de la descripcion de la arquitectura inicial

    # all: Crear un objeto de la clase GeminiOperations
    gemini_operations = GeminiOperations()

    # all: Crear un objeto de la clase PromptTemplate
    prompt_template = PromptTemplate()

    #all :leer descripcion de la arquitectura de ejemplo 
    with open('/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/examples/general_flow/example_input_description_architecture.txt', 'r') as f:
       exmaple_input_architecture = f.read()

    
    #all: funcion para generar la descripcion de la imagen de la arquitectura inicial con gemini
    output_description_architecture = gemini_operations.generate_description_image (prompt_template.template_primer_prompt_extraer_descripcion ,
                                                                 prompt_template.template_segundo_prompt_extraer_descripcion ,
                                                                 'arquitectura_inicial.png' )
    
    #all :guardar la descripcion de la arquitectura de salida
    with open('/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/final_output/output_description_architecture.txt', 'w') as f:
      f.write(output_description_architecture)

    print("el primer prompt fue generado correctamente")


if __name__ == "__main__":
    run ()