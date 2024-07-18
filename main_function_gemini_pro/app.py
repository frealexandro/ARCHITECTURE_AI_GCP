from fastapi import FastAPI, HTTPException , File, UploadFile
from pydantic import BaseModel
from verify_service_account import ServiceAccessChecker
from tempfile import NamedTemporaryFile
import shutil
import json

app = FastAPI()

@app.post("/check-access/")
async def check_access(credentials_file: UploadFile = File(...)):
    # Crear un archivo temporal para guardar el contenido del archivo subido
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(credentials_file.file, temp_file)
        temp_file_path = temp_file.name

    try:
        # Leer el contenido del archivo JSON
        with open(temp_file_path, 'r') as f:
            credentials_data = json.load(f)
        
        # Extraer el project_id del archivo de credenciales
        project_id = credentials_data.get('project_id')
        
        if not project_id:
            raise ValueError("No se encontró 'project_id' en el archivo de credenciales")

        checker = ServiceAccessChecker(temp_file_path, project_id)
        services = ['compute', 'storage', 'pubsub', 'cloudfunctions', 'bigquery', 'gemini']
        results = checker.check_full_access_service_account(services)
        
        # Añadir el project_id a los resultados
        results['project_id'] = project_id
        
        return results
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="El archivo proporcionado no es un JSON válido")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Asegúrate de eliminar el archivo temporal
        import os
        os.unlink(temp_file_path)
