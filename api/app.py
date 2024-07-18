from fastapi import FastAPI, HTTPException , File, UploadFile
from pydantic import BaseModel
from verify_service_account import ServiceAccessChecker
from tempfile import NamedTemporaryFile
import shutil
import json

app = FastAPI()

@app.post("/check-access/")
async def check_access(credentials_file: UploadFile = File(...)):
    
    #! Create a temporary file to store the content of the uploaded file
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(credentials_file.file, temp_file)
        temp_file_path = temp_file.name

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
        results = checker.check_full_access_service_account(services)
        
        #! Add the project_id to the results
        results['project_id'] = project_id
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
