from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers import auth_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, err) -> JSONResponse:
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=500,
                        content={"message": f"{base_error_message}. Detail: {str(err)}"})


app.include_router(auth_router, tags=["Auth"])
