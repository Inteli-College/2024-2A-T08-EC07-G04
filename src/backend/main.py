from fastapi import FastAPI
from models.database import engine, Base
from routes import predictionRoutes, healthChecksRoutes, dashboardRoutes
from fastapi.middleware.cors import CORSMiddleware

# Criação da tabela no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # This allows all headers
)

# Registro das rotas
app.include_router(predictionRoutes.router)
app.include_router(healthChecksRoutes.router)
app.include_router(dashboardRoutes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)