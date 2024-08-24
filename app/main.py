from fastapi import FastAPI
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.representant import router as representant_router
from app.api.restaurant import router as restaurant_router
from app.api.category import router as category_router
from app.api.invoice import router as invoice_router
from app.api.menu import router as menu_router
from app.api.table import router as table_router
from app.api.order import router as order_router
from app.api.tableSession import router as table_session_router
from app.api.menuItem import router as menu_item_router

app = FastAPI(debug=True)

app.include_router(category_router, prefix="/categories", tags=["Categories"])
app.include_router(representant_router, prefix="/representants", tags=["Representants"])
app.include_router(restaurant_router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(invoice_router, prefix="/invoices", tags=["Invoices"])
app.include_router(menu_router, prefix="/menus", tags=["Menus"])
app.include_router(table_router, prefix="/tables", tags=["Tables"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(table_session_router, prefix="/table-sessions", tags=["Table Sessions"])
app.include_router(menu_item_router, prefix="/menu-items", tags=["Menu Items"])

origins = [
    "http://localhost:5173",
    "https://2c52-31-205-5-212.ngrok-free.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    # Initialize resources
    print("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources
    print("Shutting down...")
