
#all: primera funcion para crear la descripcion del pipeline tenuiendo en cuenta que la service account ya esdta logueada en el entorno 

from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerativeModel,Part
import re
import os


#all: Ruta al archivo de clave de la cuenta de servicio
key_path = "/home/frealexandro/proyectos_personales/gemini_pro_competition/keys/key_service_account_analitycs_contactica.json"


#all : cargar la cuenta de servicio en el sistema con os esta se encuentra ya cargada en la variable key_path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path


