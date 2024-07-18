
import vertexai
from vertexai.generative_models import GenerativeModel,Part

class GeminiOperations:

    #all: Class to perform operations with the language model
    def __init__(self, model):
        #all: Initialize the language model
        self.model = model


    
    #all: Method to generate the description of an image
    def generate_description_image(self, prompt_1, prompt_2, name_image):
        try:
            vertexai.init(project="datalake-analytics-339922", location="us-central1")

            model = GenerativeModel(self.model)

            route_image2 = f"gs://gemini_pro/{name_image}"
            image1 = Part.from_uri(mime_type="image/png", uri="gs://gemini_pro/ejemplo_arquitectura.png")
            image2 = Part.from_uri(mime_type="image/png", uri=route_image2)

            response = model.generate_content([prompt_1, image1, prompt_2, image2, "output:"])
            return response.text
        except Exception as e:
            print(f"Error al generar la descripción de la imagen {name_image}: {str(e)}")
            return ""


    
    #all: Method to extract the description of a step
    def generate_count_steps(self, final_prompt):
        try:
            vertexai.init(project="datalake-analytics-339922", location="us-central1")
            
            model = GenerativeModel(self.model)

            response = model.generate_content([final_prompt])

            return response.text
        except Exception as e:
            print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")

            return ""


    #all: Method to extract the aspects of an architecture
    def get_aspects(self, final_prompt):
        try:
            vertexai.init(project="datalake-analytics-339922", location="us-central1")

            model = GenerativeModel(self.model)

            response = model.generate_content([final_prompt])
            return response.text
        except Exception as e:
            print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")
            return ""


    #all: Method to extract a step from an architecture
    def extract_step(self, final_prompt):

        try:

            vertexai.init(project="datalake-analytics-339922", location="us-central1")
            
            model = GenerativeModel(self.model)

            response = model.generate_content([final_prompt])
            return response.text
        except Exception as e:
            print(f"Error al encontrar el número de pasos en {final_prompt}: {str(e)}")
            return ""