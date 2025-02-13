from fastapi import APIRouter, Depends, UploadFile, HTTPException
from dependency_injector.wiring import Provide, inject
from starlette.formparsers import MultiPartParser

from application.use_cases.process_csv_billing import ProcessCsvBilling
from container import Container

router = APIRouter(prefix="/billing", tags=["Billing"])

MultiPartParser.max_file_size = 110 * 1024 * 1024


@router.post("/upload")
@inject
async def upload_csv(
    file: UploadFile,
    process_csv_use_case: ProcessCsvBilling = Depends(Provide[Container.process_csv_use_case])
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        await process_csv_use_case.execute(file.file)
        return {"message": "File processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

