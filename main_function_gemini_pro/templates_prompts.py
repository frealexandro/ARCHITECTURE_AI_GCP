

#all: class Prompts
class Prompts:

    def __init__(self):
        self.template_primer_prompt_extraer_descripcion = """Quiero construir este flujo desde el inicio hata el final solo usando la terminal de comandos de GCP.
No tengo ninguna API habilitada de ningun servicio de GCP.Solo tengo habilitada una service account con todos los accesos.  
Quiero las intruciones Paso a Paso .Adicional dime los Prerrequisitios,Recomendaciones,Posibles errores y Testing para evaluar
este flujo correctamente. Puedes utilizar como lenguaje de programacion python para completar la logica dentro de algun componente. 
Si es necesario en caso tal recuerda darme la dependencias y paquetes para tener un codigo exitoso.

input:"""

        self.template_segundo_prompt_extraer_descripcion =  """

output:{example_input_description_architecture}


input:

"""

        self.template_segundo_prompt = """"

Extraeme el numero de pasos PRINICLPALES  de las siguientes intrucciones y dame un numero entero  de cuantos pasos PRINCIPALES son en total:


input:{example_input_description_architecture}

output:{example_input_num_steps_architecture}

input:{output_description_architecture}

output:

"""

        self.template_tercer_prompt = """"

Necesito que porfavor me extraigas exactamente la siguiente informacion de este texto ("Prerrequisitos","Recomendaciones","Posibles errores","Testing")

input:{example_input_description_architecture}

output:{example_input_aspects_architecture}

input:{output_description_architecture}

output:

"""

        self.template_extraer_paso = """"

Extraeme exactamente la informacion del paso principal numero {num_paso} de las siguientes intrucciones , 
quiero exactamente el mismo texto , puedes reconocerlo por que todos lo pasos principales inician con estos caracteres  "**1."

input:{output_description_architecture}

output:

"""