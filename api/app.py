
#all: Import the necessary libraries
from fastapi import FastAPI, HTTPException , File, UploadFile, Form
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
import shutil
import json
import uuid
import os
import uvicorn


#all: object to check the access of the service account
from verify_service_account import ServiceAccessChecker

#all: object to create the code
from create_code import Createcode



app = FastAPI()



#all: endpoint to create the code
@app.post("/check-access/")
async def check_access(credentials_file: UploadFile = File(...)):
    
    #! Create a temporary file to store the content of the uploaded file
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(credentials_file.file, temp_file)
        temp_file_path = temp_file.name
        
        #all: Load the service account into the system using os, as it is already loaded in the variable key_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

    try:
        #! Read the content of the JSON file
        with open(temp_file_path, 'r') as f:
            credentials_data = json.load(f)
        
        #! Extract the project_id from the credentials file
        project_id = credentials_data.get('project_id')
        
        if not project_id:
            raise ValueError("No se encontró 'project_id' en el archivo de credenciales")

        checker = ServiceAccessChecker(temp_file_path, project_id)
        services = ['compute', 'storage', 'pubsub', 'cloudfunctions', 'bigquery', 'gemini']
        #! invoke the method to check the access of the service account
        results = checker.check_full_access_service_account(services)
        
        #! Add the project_id to the results
        results['project_id'] = project_id
        
        return results
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="El archivo proporcionado no es un JSON válido")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        #! Make sure to delete the temporary file
        import os
        os.unlink(temp_file_path)




#* ejemplo de como se puede inicializar el proyecto y la ubicacion con las credenciales de la cuenta de servicio
#* vertexai.init(project="datalake-analytics-339922", location="us-central1", credentials=credentials)

#all: endpoint to create the code
@app.post("/upload-image-and-prompt/")
async def upload_image_and_prompt(image: UploadFile = File(...), prompt: str = Form(...)):
    #! Generate a unique file name for the image
    file_name = f"{uuid.uuid4()}.png"
    #! Save the image to a directory
    with open(f"./images_architectures/{file_name}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    #! Create an object of the Createcode class
    create_code = Createcode()

    print(prompt)

    #! Invoke the create_code method to generate the code
    mensaje_de_exito = create_code.create_code(f"./images_architectures/{file_name}", prompt)

    #! Return the route or URL to the image and the processed prompt
    return mensaje_de_exito




