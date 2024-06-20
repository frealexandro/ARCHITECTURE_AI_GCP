
import vertexai
from vertexai.generative_models import GenerativeModel,Part

class GeminiOperations:

    #all: Clase para realizar operaciones con el modelo de lenguaje
    def __init__(self, model):
        #all: Inicializar el modelo de lenguaje
        self.model = model


    #all: Metodo para generar la descripcion de una imagen
    def generate_description_image_chain(self, prompt_1, prompt_2, name_image):
        try:
            route_image2 = f"gs://gemini_pro/{name_image}"
            image1 = Part.from_uri(mime_type="image/png", uri="gs://gemini_pro/ejemplo_arquitectura.png")
            image2 = Part.from_uri(mime_type="image/png", uri=route_image2)
            response = self.model.generate_content([prompt_1, image1, prompt_2, image2, "output:"])
            return response.text
        except Exception as e:
            print(f"Error al generar la descripción de la imagen {name_image}: {str(e)}")
            return ""


    #all: Metodo para extraer la descripcion de un paso
    def generate_count_steps_chain(self, prompt, output_description_architecture, example_input_description_architecture, example_input_num_steps_architecture):
        try:
            final_prompt = prompt.format(
                output_description_architecture=output_description_architecture,
                example_input_description_architecture=example_input_description_architecture,
                example_input_num_steps_architecture=example_input_num_steps_architecture
            )
            response = self.model.generate_content([final_prompt])
            return response.text
        except Exception as e:
            print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")
            return ""


    #all: Metodo para extraer los aspectos de una arquitectura
    def get_aspects_chain(self, prompt_aspects, output_description_architecture, example_input_description_architecture, example_input_aspects_architecture):
        try:
            final_prompt = prompt_aspects.format(
                output_description_architecture=output_description_architecture,
                example_input_description_architecture=example_input_description_architecture,
                example_input_aspects_architecture=example_input_aspects_architecture
            )
            response = self.model.generate_content([final_prompt])
            return response.text
        except Exception as e:
            print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")
            return ""


    #all: Metodo para extraer un paso de una arquitectura
    def extract_step_chain(self, prompt, output_description_architecture, num_paso):
        final_prompt = prompt.format(output_description_architecture=output_description_architecture, num_paso=num_paso)
        try:
            response = self.model.generate_content([final_prompt])
            return response.text
        except Exception as e:
            print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")
            return ""