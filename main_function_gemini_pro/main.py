
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

    
    #all:  Definimos los pasos de la cadena de operaciones
    generate_description_image_step = SimpleChain(
    input_variables=["prompt_1", "prompt_2", "name_image"],
    output_variables=["output_description_architecture"],
    chain_function=gemini_operations.generate_description_image_chain
)

    generate_count_steps_step = SimpleChain(
    input_variables=["prompt", "output_description_architecture", "example_input_description_architecture", "example_input_num_steps_architecture"],
    output_variables=["steps_new_flow"],
    chain_function=gemini_operations.generate_count_steps_chain
)

    get_aspects_step = SimpleChain(
    input_variables=["prompt_aspects", "output_description_architecture", "example_input_description_architecture", "example_input_aspects_architecture"],
    output_variables=["other_aspects"],
    chain_function=gemini_operations.get_aspects_chain
)

    extract_step_step = SimpleChain(
    input_variables=["prompt", "output_description_architecture", "num_paso"],
    output_variables=["step"],
    chain_function=gemini_operations.extract_step_chain
)

# Create the final chain
final_chain = SimpleChain(
    steps=[
        generate_description_image_step,
        generate_count_steps_step,
        get_aspects_step,
        extract_step_step
    ]
)

# Run the chain
output_description_architecture = final_chain.run({
    "prompt_1": template_primer_prompt_extraer_descripcion,
    "prompt_2": template_segundo_prompt_extraer_descripcion,
    "name_image": "arquitectura_inicial.png",
    "prompt": template_segundo_prompt,
    "example_input_description_architecture": example_input_description_architecture,
    "example_input_num_steps_architecture": example_input_num_steps_architecture,
    "prompt_aspects": template_tercer_prompt,
    "example_input_aspects_architecture": example_input_aspects_architecture,
    "num_paso": 1  # This will need to be looped as per your logic
})

print(output_description_architecture)

    

    


if __name__ == "__main__":
    run ()