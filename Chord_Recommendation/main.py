import uvicorn
from fastapi import FastAPI
from source.routers.core_router import router


application = FastAPI()
application.include_router(router)

if __name__=='__main__':
    uvicorn.run(app = "main:application",
                host = "0.0.0.0",
                port = 2155,
                reload = True)