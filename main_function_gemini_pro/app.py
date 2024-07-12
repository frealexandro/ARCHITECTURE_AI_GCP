from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from verify_service_account import ServiceAccessChecker

app = FastAPI()


class ServiceList(BaseModel):
    services: list





@app.post("/check-access/")
def check_access(service_list: ServiceList):
    credentials_file = '/home/frealexandro/proyectos_personales/gemini_pro_competition/keys/key_service_account_analitycs_contactica.json'  # Asegúrate de poner la ruta correcta
    project_id = 'datalake-analytics-339922'  # Asegúrate de poner el ID de proyecto correcto

    checker = ServiceAccessChecker(credentials_file, project_id)
    try:
        results = checker.check_full_access_service_account(service_list.services)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
