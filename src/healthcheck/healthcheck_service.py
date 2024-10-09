from fastapi import FastAPI
import httpx
import asyncpg
import asyncio
app = FastAPI()
DATABASE_URL = "postgresql://postgres:KXQDTu5XrbsVDhe@postgres:5432/fillmore"
@app.get("/healthcheck")
async def healthcheck():
    health_status = {
        "backend": await check_backend(),
        "frontend": await check_frontend(),
        "database": await check_database(),
        "pocketbase": await check_pocketbase(),
    }
    return health_status
async def check_backend():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://backend:8000/", timeout=5.0)
            if response.status_code == 200:
                return "OK"
    except Exception as e:
        print(f"Backend Error: {e}")
    return "DOWN"
async def check_frontend():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://frontend:4173/", timeout=5.0)
            if response.status_code == 200:
                return "OK"
    except Exception as e:
        print(f"Frontend Error: {e}")
    return "DOWN"
@app.on_event("startup")
async def startup():
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)
@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()
async def check_database():
    try:
        async with app.state.db_pool.acquire() as connection:
            await connection.execute("SELECT 1")
        return "OK"
    except Exception as e:
        print(f"Database Error: {e}")
    return "DOWN"
async def check_pocketbase():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://pocketbase:8090/_/", timeout=5.0)
            if response.status_code == 200:
                return "OK"
    except Exception as e:
        print(f"PocketBase Error: {e}")
        if 'response' in locals():
            print(f"PocketBase Error: {response.status_code}")
    return "DOWN"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)