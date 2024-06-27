
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

    # all: leer el archivo de la primera arquitectura
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

    #all: asignacion de varaibles al prompt para la descripcion de la arquitectura
    template_segundo_prompt_extraer_descripcion = prompt_template.template_segundo_prompt_extraer_descripcion.format(
        example_input_description_architecture = exmaple_input_architecture)

    #! se puede agregar descripcion del flujo con el fin de que tenga una mejor interpretacion el modelo de gemini
    #all: funcion para generar la descripcion de la imagen de la arquitectura inicial con gemini
    output_description_architecture = gemini_operations.generate_description_image (prompt_template.template_primer_prompt_extraer_descripcion ,
                                                                                    template_segundo_prompt_extraer_descripcion ,
                                                                                    'arquitectura_inicial.png' )

    #all :guardar la descripcion de la arquitectura de salida
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_description_architecture.txt', 'w') as f:
      f.write(output_description_architecture)

    print("el primer prompt fue generado correctamente")

    
    #!###################################################################
    #!inicio del segundo prompt para contar los pasos de la arquitectura

    #all: leer el ejemplo del numero de pasos de la arquitectura ejemplo
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/examples/general_flow/example_input_num_steps_architecture.txt', 'r') as f:
        example_input_steps_architecture = f.read()

    #all: llama la funcion de contar los pasos con gemini
    steps_new_flow = gemini_operations.generate_count_steps(prompt_template.template_segundo_prompt ,
                                                            output_description_architecture, 
                                                            exmaple_input_architecture ,
                                                            example_input_steps_architecture)

    #all: guardar el archivo de los pasos de salida
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_num_steps_architecture.txt', 'w') as f:
        f.write(steps_new_flow)

    
    #all: extraer el numero de pasos con una funcion regex
    number_steps = re.findall(r'\d+', steps_new_flow)
    print(f"El numero de pasos en el flujo es: {number_steps[0]}")

    
    print("el segundo prompt fue generado correctamente")

    #!###################################################################
    #!inicio del tercer prompt para obtener otros aspectos de la arquitectura en un archivo

    #all: leer el ejemplo de otros aspectos de la arquitectura
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/examples/general_flow/example_input_other_aspects_architecture.txt', 'r') as f:
        example_input_aspects_architecture = f.read()


    #all: llama la funcion de otros aspectos de la arquitectura, esto con el fin de obtener otros aspectos de la arquitectura 
    other_aspects = gemini_operations.get_aspects(prompt_template.template_tercer_prompt,
                                                  output_description_architecture, 
                                                  exmaple_input_architecture,
                                                  example_input_aspects_architecture,)

    #all: guardar archivo de otros aspectos de la arquitectura
    with open('/home/frealexandro/proyectos_personales/gemini_pro_competition/main_function_gemini_pro/final_output/output_other_aspects_architecture.txt', 'w') as f:
       f.write(other_aspects)

    print("el tercer prompt fue generado correctamente")

    #!#####################################################################
    #!inicio del cuarto prompt para extraer el paso exacto de las instrucciones


    #all: usar la variable number_steps[0] para el numero de pasos en el flujo de la arquitectura con un ciclo for desde 1 hasta el numero de pasos
    for i in range(int(number_steps[0])):
        
        #*se depreca esta opcion debido a que no se ve util la opcion de agregar ejemplos, puede tener fallos ya que el num de ejmplo varia
        # with open(f'/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/examples/paso_{i+1}/paso_{i+1}.txt', 'r') as f:
        #     example_input_paso_architecture = f.read()
        
        #all: llama la funcion de extraer el paso exacto de las instrucciones
        step = gemini_operations.extract_step(prompt_template.template_extraer_paso, output_description_architecture,
                                              i+1 )


        #all: guardar el archivo de los pasos 
        with open(f'/home/frealexandro/projects/Notebooks_2024/GEN_GCP_AI/competition_gemini_pro/final_output/step_{i+1}.txt', 'w') as f:
            f.write(step)

        print(f"se extrajo correctamente el paso:  {i+1}")


    print("el cuarto prompt fue generado correctamente")


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

    print("se extrajo correctamente los bloques de codigo de los pasos")


if __name__ == "__main__":
    run ()