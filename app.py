from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.cncRoutes import cncRoutes
from routes.fileRoutes import fileRoutes
from routes.materialRoutes import materialRoutes
from routes.monitorRoutes import monitorRoutes
from routes.toolRoutes import toolRoutes
from routes.taskRoutes import taskRoutes
from routes.userRoutes import userRoutes
from routes.workerRoutes import workerRoutes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_main():
    return {"message": "Hello World from FastAPI"}


# Routes
app.include_router(cncRoutes)
app.include_router(fileRoutes)
app.include_router(materialRoutes)
app.include_router(monitorRoutes)
app.include_router(toolRoutes)
app.include_router(taskRoutes)
app.include_router(userRoutes)
app.include_router(workerRoutes)
