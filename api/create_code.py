
#all: first function to create the pipeline description considering that the service account is already logged in the environment

from google.oauth2 import service_account
import re
import os

#all: import the CloudStorageManager class
from cloud_storage import CloudStorageManager

#all: import the GeminiOperations class
from gemini_operations import GeminiOperations

#all: import the PromptTemplate class
from templates_prompts import Prompts
from cloud_storage import CloudStorageManager
from gemini_operations import GeminiOperations





#all: Path to the service account key file
key_path = "/home/frealexandro/proyectos_personales/gemini_pro_competition/keys/key_service_account_analitycs_contactica.json"


#all: Load the service account into the system using os, as it is already loaded in the variable key_path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path


#* ejemplo de como se puede inicializar el proyecto y la ubicacion con las credenciales de la cuenta de servicio
#* vertexai.init(project="datalake-analytics-339922", location="us-central1", credentials=credentials)








def run ():

    #!################################################################
    #! Upload the image of the initial architecture to a Google Cloud Storage bucket


    # all: Create an object of the CloudStorageManager class
    cloud_storage_manager = CloudStorageManager()

    # all: read the first image of the architecture
    path_image = "/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/images_architectures/arquitectura_inicial.png"



    
    # all: use the upload_blob method to upload a file to a bucket
    cloud_storage_manager.upload_blob("gemini_pro", path_image , 'arquitectura_inicial.png' )

    #!################################################################
    #!inicio del proceso de generacion de la descripcion de la arquitectura inicial

    # all: create language model variable
    model = "gemini-1.5-pro-001"


    
    # all: Create an object of the GeminiOperations class
    gemini_operations = GeminiOperations(model)

    # all: Create an object of the PromptTemplate class
    prompt_template = Prompts()

    
    #all : read description of the example architecture 
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/examples/general_flow/example_input_description_architecture.txt', 'r') as f:
       exmaple_input_architecture = f.read()

    
    #all: read the flow description of the first architecture
    first_flow_prompt = """Este flujo actual consta de cuatro componentes principales. El primero es un archivo Excel denominado "archivo_1", 
        que incluye la información a procesar y consta de 82 columnas. Idealmente, este archivo se cargará en un bucket de 
        Google Cloud Platform (GCP) llamado "bucket_experiment". El segundo componente es el mencionado bucket, situado 
        en la región us-central-1 y de tipo estándar, que actúa como disparador para una Cloud Function. 
        El tercer componente es esta Cloud Function, ubicada en us-central-1, denominada "bucket_experiment". 
        Esta función se encarga de procesar el archivo Excel, asegurándose de que contenga las 82 columnas requeridas y, de ser así,
        exportar los datos a una tabla en BigQuery llamada "tabla_experiment", ubicada en el dataset "experiment".
        El cuarto y último componente es la mencionada tabla en BigQuery, que es una tabla en blanco.
        Esta tabla se reemplaza mediante un script en Python ejecutado desde la Cloud Function, encargándose de almacenar 
        temporalmente los datos exportados mientras se inserta otro archivo Excel en "bucket_experiment"."""



    #all: assignment of variables to the prompt for the architecture description
    template_segundo_prompt_extraer_descripcion = prompt_template.template_segundo_prompt_extraer_descripcion.format(
        example_input_description_architecture = exmaple_input_architecture, input_description_architecture_context = first_flow_prompt)

    
    #! A description of the flow can be added so that the Gemini model has a better interpretation.
    #all: function to generate the description of the image of the initial architecture with Gemini
    output_description_architecture = gemini_operations.generate_description_image (prompt_template.template_primer_prompt_extraer_descripcion ,
                                                                                    template_segundo_prompt_extraer_descripcion ,
                                                                                    'initial_architecture.png' )

    #all : save the description of the output architecture
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_description_architecture.txt', 'w') as f:
      f.write(output_description_architecture)

    print("The first prompt was generated correctly")

    
    #!###################################################################
    #!start of the second prompt to count the steps of the architecture

    #all: read the example of the number of steps in the example architecture
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/examples/general_flow/example_input_num_steps_architecture.txt', 'r') as f:
        example_input_steps_architecture = f.read()


    #all: assignment of variables to the prompt to count the steps of the architecture

    template_segundo_prompt = prompt_template.template_segundo_prompt.format(
                output_description_architecture = output_description_architecture,
                example_input_description_architecture = exmaple_input_architecture,
                example_input_num_steps_architecture = example_input_steps_architecture
            )

    #all: calls the step counting function with gemini
    steps_new_flow = gemini_operations.generate_count_steps(template_segundo_prompt)

    
    #all: save the output steps file
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_num_steps_architecture.txt', 'w') as f:
        f.write(steps_new_flow)

    
    
    #all: extract the number of steps with a regex function
    number_steps = re.findall(r'\d+', steps_new_flow)
    print(f"The number of flow steps are: {number_steps[0]}")

    
    print("The second prompt was generated correctly")

    #!###################################################################
    #!start the third prompt to get other aspects of the architecture in a file

    #all: read the example of other aspects of architecture
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/examples/general_flow/example_input_other_aspects_architecture.txt', 'r') as f:
        example_input_aspects_architecture = f.read()

    #all: assignment of variables to the prompt to obtain other aspects of the architecture
    template_tercer_prompt = prompt_template.template_tercer_prompt.format(
        example_input_description_architecture = exmaple_input_architecture,
        example_input_aspects_architecture = example_input_aspects_architecture,
        output_description_architecture = output_description_architecture
    )


    
    #all: calls the function of other aspects of the architecture, this in order to obtain other aspects of the architecture
    other_aspects = gemini_operations.get_aspects(template_tercer_prompt)

    #all: save file from other aspects of the architecture
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_other_aspects_architecture.txt', 'w') as f:
       f.write(other_aspects)

    print("The third prompt was generated correctly")

    #!######################################################################
    #!start of the fourth prompt to extract the exact step of the instructions

    
    #all: use the variable number_steps[0] for the number of steps in the architecture flow with a for loop from 1 to the number of steps
    for i in range(int(number_steps[0])):
        
        
        #*this option is deprecated because the option to add examples does not seem useful, it may have errors since the example number varies
        # with open(f'/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/examples/paso_{i+1}/paso_{i+1}.txt', 'r') as f:
        #     example_input_paso_architecture = f.read()

        
        #all: assignment of variables to the prompt to extract the exact step of the instructions
        template_extraer_paso = prompt_template.template_extraer_paso.format(
            output_description_architecture = output_description_architecture,
            num_paso = i+1
        )
        
        #all: calls the function to extract the exact step of the instructions
        step = gemini_operations.extract_step(template_extraer_paso)


        
        #all: save the file of the extracted steps
        with open(f'/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/final_output/step_{i+1}.txt', 'w') as f:
            f.write(step)

        print(f"The flow step number {i+1} was extracted correctly")


    print("The fourth prompt was generated correctly")


    #!######################################################################
    #!extract the code blocks of the extracted steps
    

    for i in range(int(number_steps[0])):


        #all: read a text file with the extracted steps       
        with open(f'/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/step_{i+1}.txt', 'r') as f:
            step = f.read()


        #all: Extract the text into a single list with the bash, python and txt tags in the correct order of steps 
        pattern = re.compile(r'```(bash|python|txt)(.*?)```', re.DOTALL)


        matches = pattern.findall(step)


        code_blocks = []

        for match in matches:
            
            code_blocks.append(match[1].strip())
            #all: save list to a text file
            with open(f'/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/code_blocks_{i}.txt', 'w') as f:
                f.write(str(code_blocks))

    print("The code blocks were extracted correctly")


if __name__ == "__main__":
    run ()