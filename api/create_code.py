
#all: primera funcion para crear la descripcion del pipeline tenuiendo en cuenta que la service account ya esdta logueada en el entorno 

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

    # all: leer la imagen  de la primera arquitectura
    path_image = "/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/images_architectures/arquitectura_inicial.png"



    # all: usar el metodo upload_blob para subir un archivo a un bucket
    cloud_storage_manager.upload_blob("gemini_pro", path_image , 'arquitectura_inicial.png' )

    #!################################################################
    #!inicio del proceso de generacion de la descripcion de la arquitectura inicial

    # all: crear variable del modelo de lenguaje
    model = "gemini-1.5-pro-001"


    # all: Crear un objeto de la clase GeminiOperations
    gemini_operations = GeminiOperations(model)

    # all: Crear un objeto de la clase PromptTemplate
    prompt_template = Prompts()

    #all :leer descripcion de la arquitectura de ejemplo 
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/examples/general_flow/example_input_description_architecture.txt', 'r') as f:
       exmaple_input_architecture = f.read()

    #all: leer la descripcion del flujo de la primera arquitectura
    prompt_primer_flujo = """Este flujo actual consta de cuatro componentes principales. El primero es un archivo Excel denominado "archivo_1", 
        que incluye la información a procesar y consta de 82 columnas. Idealmente, este archivo se cargará en un bucket de 
        Google Cloud Platform (GCP) llamado "bucket_experiment". El segundo componente es el mencionado bucket, situado 
        en la región us-central-1 y de tipo estándar, que actúa como disparador para una Cloud Function. 
        El tercer componente es esta Cloud Function, ubicada en us-central-1, denominada "bucket_experiment". 
        Esta función se encarga de procesar el archivo Excel, asegurándose de que contenga las 82 columnas requeridas y, de ser así,
        exportar los datos a una tabla en BigQuery llamada "tabla_experiment", ubicada en el dataset "experiment".
        El cuarto y último componente es la mencionada tabla en BigQuery, que es una tabla en blanco.
        Esta tabla se reemplaza mediante un script en Python ejecutado desde la Cloud Function, encargándose de almacenar 
        temporalmente los datos exportados mientras se inserta otro archivo Excel en "bucket_experiment"."""



    #all: asignacion de varaibles al prompt para la descripcion de la arquitectura
    template_segundo_prompt_extraer_descripcion = prompt_template.template_segundo_prompt_extraer_descripcion.format(
        example_input_description_architecture = exmaple_input_architecture, input_description_architecture_context = prompt_primer_flujo)

    #! se puede agregar descripcion del flujo con el fin de que tenga una mejor interpretacion el modelo de gemini
    #all: funcion para generar la descripcion de la imagen de la arquitectura inicial con gemini
    output_description_architecture = gemini_operations.generate_description_image (prompt_template.template_primer_prompt_extraer_descripcion ,
                                                                                    template_segundo_prompt_extraer_descripcion ,
                                                                                    'arquitectura_inicial.png' )

    #all :guardar la descripcion de la arquitectura de salida
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_description_architecture.txt', 'w') as f:
      f.write(output_description_architecture)

    print("The first prompt was generated correctly")

    
    #!###################################################################
    #!inicio del segundo prompt para contar los pasos de la arquitectura

    #all: leer el ejemplo del numero de pasos de la arquitectura ejemplo
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/examples/general_flow/example_input_num_steps_architecture.txt', 'r') as f:
        example_input_steps_architecture = f.read()

    #all :asignacion de varaibles al prompt para contar los pasos de la arquitectura

    template_segundo_prompt = prompt_template.template_segundo_prompt.format(
                output_description_architecture = output_description_architecture,
                example_input_description_architecture = exmaple_input_architecture,
                example_input_num_steps_architecture = example_input_steps_architecture
            )

    #all: llama la funcion de contar los pasos con gemini
    steps_new_flow = gemini_operations.generate_count_steps(template_segundo_prompt)

    #all: guardar el archivo de los pasos de salida
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_num_steps_architecture.txt', 'w') as f:
        f.write(steps_new_flow)

    
    #all: extraer el numero de pasos con una funcion regex
    number_steps = re.findall(r'\d+', steps_new_flow)
    print(f"The number of flow steps are: {number_steps[0]}")

    
    print("The second prompt was generated correctly")

    #!###################################################################
    #!inicio del tercer prompt para obtener otros aspectos de la arquitectura en un archivo

    #all: leer el ejemplo de otros aspectos de la arquitectura
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/examples/general_flow/example_input_other_aspects_architecture.txt', 'r') as f:
        example_input_aspects_architecture = f.read()

    #all: asignacion de varaibles al prompt para obtener otros aspectos de la arquitectura
    template_tercer_prompt = prompt_template.template_tercer_prompt.format(
        example_input_description_architecture = exmaple_input_architecture,
        example_input_aspects_architecture = example_input_aspects_architecture,
        output_description_architecture = output_description_architecture
    )


    #all: llama la funcion de otros aspectos de la arquitectura, esto con el fin de obtener otros aspectos de la arquitectura 
    other_aspects = gemini_operations.get_aspects(template_tercer_prompt)

    #all: guardar archivo de otros aspectos de la arquitectura
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_other_aspects_architecture.txt', 'w') as f:
       f.write(other_aspects)

    print("The third prompt was generated correctly")

    #!#####################################################################
    #!inicio del cuarto prompt para extraer el paso exacto de las instrucciones


    #all: usar la variable number_steps[0] para el numero de pasos en el flujo de la arquitectura con un ciclo for desde 1 hasta el numero de pasos
    for i in range(int(number_steps[0])):
        
        #*se depreca esta opcion debido a que no se ve util la opcion de agregar ejemplos, puede tener fallos ya que el num de ejmplo varia
        # with open(f'/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/examples/paso_{i+1}/paso_{i+1}.txt', 'r') as f:
        #     example_input_paso_architecture = f.read()

        #all: asignacion de varaibles al prompt para extraer el paso exacto de las instrucciones
        template_extraer_paso = prompt_template.template_extraer_paso.format(
            output_description_architecture = output_description_architecture,
            num_paso = i+1
        )
        
        #all: llama la funcion de extraer el paso exacto de las instrucciones
        step = gemini_operations.extract_step(template_extraer_paso)


        #all: guardar el archivo de los pasos 
        with open(f'/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/final_output/step_{i+1}.txt', 'w') as f:
            f.write(step)

        print(f"The flow step number {i+1} was extracted correctly")


    print("The fourth prompt was generated correctly")


    #!######################################################################
    #!extraer los bloques de codigo de los pasos extraidos

    for i in range(int(number_steps[0])):


        #all: leer un archivo de texto con los pasos extraidos        
        with open(f'/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/step_{i+1}.txt', 'r') as f:
            step = f.read()


        #all: extraer el texto en una sola lista con las etiquetas bash , python y txt en el orden correcto de los pasos 
        pattern = re.compile(r'```(bash|python|txt)(.*?)```', re.DOTALL)


        matches = pattern.findall(step)


        code_blocks = []

        for match in matches:
            
            code_blocks.append(match[1].strip())
            #all: guardar lista en un archivo de texto
            with open(f'/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/code_blocks_{i}.txt', 'w') as f:
                f.write(str(code_blocks))

    print("The code blocks were extracted correctly")


if __name__ == "__main__":
    run ()