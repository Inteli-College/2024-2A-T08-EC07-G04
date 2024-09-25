from fastapi import FastAPI
from models.database import engine, Base
from routes import predictionRoutes

# Criação da tabela no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registro das rotas
app.include_router(predictionRoutes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)