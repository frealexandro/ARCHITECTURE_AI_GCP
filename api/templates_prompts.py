

#all: class Prompts
class Prompts:

    def __init__(self):
        self.template_first_prompt_extract_description = """Construir un flujo completo utilizando solo la terminal de comandos de 
        Google Cloud Platform (GCP), sin tener ninguna API habilitada de ningún servicio de GCP. Solo se cuenta con una cuenta de 
        servicio con todos los accesos necesarios.

input:  Este flujo actual consta de cuatro componentes principales. El primero es un archivo Excel denominado "archivo_1", 
        que incluye la información a procesar y consta de 82 columnas. Idealmente, este archivo se cargará en un bucket de 
        Google Cloud Platform (GCP) llamado "bucket_experiment". El segundo componente es el mencionado bucket, situado 
        en la región us-central-1 y de tipo estándar, que actúa como disparador para una Cloud Function. 
        El tercer componente es esta Cloud Function, ubicada en us-central-1, denominada "bucket_experiment". 
        Esta función se encarga de procesar el archivo Excel, asegurándose de que contenga las 82 columnas requeridas y, de ser así,
        exportar los datos a una tabla en BigQuery llamada "tabla_experiment", ubicada en el dataset "experiment".
        El cuarto y último componente es la mencionada tabla en BigQuery, que es una tabla en blanco.
        Esta tabla se reemplaza mediante un script en Python ejecutado desde la Cloud Function, encargándose de almacenar 
        temporalmente los datos exportados mientras se inserta otro archivo Excel en "bucket_experiment".  """

        self.template_second_prompt_extract_description = """

output:{example_input_description_architecture}


input:{input_description_architecture_context}

"""

        self.template_second_prompt = """"

Extraeme el numero de pasos PRINICLPALES  de las siguientes intrucciones y dame un numero entero  de cuantos pasos PRINCIPALES son en total:


input:{example_input_description_architecture}

output:{example_input_num_steps_architecture}

input:{output_description_architecture}

output:

"""

        self.template_third_prompt = """"

Necesito que porfavor me extraigas exactamente la siguiente informacion de este texto ("Prerrequisitos","Recomendaciones","Posibles errores","Testing")

input:{example_input_description_architecture}

output:{example_input_aspects_architecture}

input:{output_description_architecture}

output:

"""

        self.template_extract_step = """"

Extraeme exactamente la informacion del paso principal numero {num_paso} de las siguientes intrucciones , 
quiero exactamente el mismo texto , puedes reconocerlo por que todos lo pasos principales inician con estos caracteres  "**1."

input:{output_description_architecture}

output:

"""