# Para loopear el último paso (la extracción de pasos específicos) en el flujo de trabajo, necesitas implementar un bucle dentro del flujo de Langchain para iterar sobre cada paso necesario. Aquí tienes un ejemplo de cómo puedes hacerlo:

# 1. **Implementar el bucle dentro del flujo de Langchain**: Modificamos la cadena final para incluir un bucle que iterará sobre cada paso específico.

# 2. **Modificar la estructura de Langchain para soportar múltiples ejecuciones**: Vamos a asegurarnos de que el último paso se ejecute múltiples veces y colecte los resultados.

# Aquí tienes el código modificado para incluir el bucle:

# ```python

from langchain.chains import SimpleChain
from langchain.prompts import PromptTemplate
from langchain.models import GenerativeModel
from langchain.storage import LocalStorage

# Asumimos que 'credentials' ya está definido en tu entorno.
vertexai.init(project="datalake-analytics-339922", location="us-central1", credentials=credentials)
model = GenerativeModel("gemini-1.5-pro-001")

# Define the individual functions as chains
def generate_description_image_chain(prompt_1, prompt_2, name_image):
    try:
        route_image2 = f"gs://gemini_pro/{name_image}"
        image1 = Part.from_uri(mime_type="image/png", uri="gs://gemini_pro/ejemplo_arquitectura.png")
        image2 = Part.from_uri(mime_type="image/png", uri=route_image2)
        response = model.generate_content([prompt_1, image1, prompt_2, image2, "output:"])
        return {"output_description_architecture": response.text}
    except Exception as e:
        print(f"Error al generar la descripción de la imagen {name_image}: {str(e)}")
        return {"output_description_architecture": ""}

def generate_count_steps_chain(prompt, output_description_architecture, example_input_description_architecture, example_input_num_steps_architecture):
    try:
        final_prompt = prompt.format(
            output_description_architecture=output_description_architecture,
            example_input_description_architecture=example_input_description_architecture,
            example_input_num_steps_architecture=example_input_num_steps_architecture
        )
        response = model.generate_content([final_prompt])
        return {"steps_new_flow": response.text}
    except Exception as e:
        print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")
        return {"steps_new_flow": ""}

def get_aspects_chain(prompt_aspects, output_description_architecture, example_input_description_architecture, example_input_aspects_architecture):
    try:
        final_prompt = prompt_aspects.format(
            output_description_architecture=output_description_architecture,
            example_input_description_architecture=example_input_description_architecture,
            example_input_aspects_architecture=example_input_aspects_architecture
        )
        response = model.generate_content([final_prompt])
        return {"other_aspects": response.text}
    except Exception as e:
        print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")
        return {"other_aspects": ""}

def extract_step_chain(prompt, output_description_architecture, num_paso):
    final_prompt = prompt.format(output_description_architecture=output_description_architecture, num_paso=num_paso)
    try:
        response = model.generate_content([final_prompt])
        return {"step": response.text}
    except Exception as e:
        print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")
        return {"step": ""}

# Define the prompts templates
template_primer_prompt_extraer_descripcion = """Quiero construir este flujo desde el inicio hasta el final solo usando la terminal de comandos de GCP.
No tengo ninguna API habilitada de ningún servicio de GCP. Solo tengo habilitada una service account con todos los accesos.  
Quiero las instrucciones Paso a Paso. Adicionalmente, dime los Prerrequisitos, Recomendaciones, Posibles errores y Testing para evaluar
este flujo correctamente. Puedes utilizar como lenguaje de programación python para completar la lógica dentro de algún componente. 
Si es necesario en caso tal, recuerda darme las dependencias y paquetes para tener un código exitoso.

input:"""

template_segundo_prompt_extraer_descripcion = """
output:{example_input_description_architecture}

input:
"""

template_segundo_prompt = """
Extrae el número de pasos PRINCIPALES de las siguientes instrucciones y dame un número entero de cuantos pasos PRINCIPALES son en total:

input:{example_input_description_architecture}

output:{example_input_num_steps_architecture}

input:{output_description_architecture}

output:
"""

template_tercer_prompt = """
Necesito que por favor extraigas exactamente la siguiente información de este texto ("Prerrequisitos", "Recomendaciones", "Posibles errores", "Testing")

input:{example_input_description_architecture}

output:{example_input_aspects_architecture}

input:{output_description_architecture}

output:
"""

template_extraer_paso = """
Extrae exactamente la información del paso principal número {num_paso} de las siguientes instrucciones. 
Quiero exactamente el mismo texto, puedes reconocerlo porque todos los pasos principales inician con estos caracteres "**1."

input:{output_description_architecture}

output:
"""

# Define the chain steps
generate_description_image_step = SimpleChain(
    input_variables=["prompt_1", "prompt_2", "name_image"],
    output_variables=["output_description_architecture"],
    chain_function=generate_description_image_chain
)

generate_count_steps_step = SimpleChain(
    input_variables=["prompt", "output_description_architecture", "example_input_description_architecture", "example_input_num_steps_architecture"],
    output_variables=["steps_new_flow"],
    chain_function=generate_count_steps_chain
)

get_aspects_step = SimpleChain(
    input_variables=["prompt_aspects", "output_description_architecture", "example_input_description_architecture", "example_input_aspects_architecture"],
    output_variables=["other_aspects"],
    chain_function=get_aspects_chain
)

# Function to handle looping over steps
def loop_extract_steps(output_description_architecture, num_steps):
    steps = []
    for i in range(1, num_steps + 1):
        step_result = extract_step_chain(template_extraer_paso, output_description_architecture, i)
        steps.append(step_result["step"])
    return steps

# Final chain execution
def run_chain():
    # Initialize variables
    example_input_description_architecture = "Ejemplo de descripción de arquitectura"
    example_input_num_steps_architecture = "3"
    example_input_aspects_architecture = "Ejemplo de aspectos de la arquitectura"

    # Generate description
    description_result = generate_description_image_step.run({
        "prompt_1": template_primer_prompt_extraer_descripcion,
        "prompt_2": template_segundo_prompt_extraer_descripcion,
        "name_image": "arquitectura_inicial.png"
    })
    output_description_architecture = description_result["output_description_architecture"]

    # Generate count of steps
    steps_result = generate_count_steps_step.run({
        "prompt": template_segundo_prompt,
        "output_description_architecture": output_description_architecture,
        "example_input_description_architecture": example_input_description_architecture,
        "example_input_num_steps_architecture": example_input_num_steps_architecture
    })
    steps_new_flow = steps_result["steps_new_flow"]
    num_steps = int(re.findall(r'\d+', steps_new_flow)[0])

    # Get aspects
    aspects_result = get_aspects_step.run({
        "prompt_aspects": template_tercer_prompt,
        "output_description_architecture": output_description_architecture,
        "example_input_description_architecture": example_input_description_architecture,
        "example_input_aspects_architecture": example_input_aspects_architecture
    })
    other_aspects = aspects_result["other_aspects"]

    # Loop to extract each step
    steps = loop_extract_steps(output_description_architecture, num_steps)
    
    return {
        "output_description_architecture": output_description_architecture,
        "steps_new_flow": steps_new_flow,
        "num_steps": num_steps,
        "other_aspects": other_aspects,
        "steps": steps
    }

# Run the final chain
final_result = run_chain()

print(final_result)
# ```

# En este código:

# 1. **`loop_extract_steps`**: Función que itera sobre el número de pasos y llama a `extract_step_chain` para cada paso, recolectando los resultados en una lista.
# 2. **`run_chain`**: Función que coordina la ejecución del flujo completo, manejando las entradas y salidas de cada paso y utilizando la función `loop_extract_steps` para iterar sobre los pasos.

# Este enfoque te permite encadenar y loopear los diferentes prompts, asegurando que la salida de un paso se utilice correctamente en el siguiente. ¿Hay algo más que te gustaría ajustar o agregar? 🔨🤖🔧