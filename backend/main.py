from backend.routers import auth, search, ask, portfolio, invest
from fastapi import FastAPI

app = FastAPI()

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(ask.router, prefix="/ask", tags=["Ask"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
app.include_router(invest.router, prefix="/invest", tags=["Investments"])

@app.get("/")
def root():
    return {"message": "SmartInvest backend is running"}
