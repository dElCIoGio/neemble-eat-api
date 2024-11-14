from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, APIRouter
from fastapi import HTTPException, Request

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

import json
import logging
from typing import Callable

from app.websocket.manager import manager

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


class CORSHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def preflight_handler(request: Request) -> Response:
            if request.method == 'OPTIONS':
                response = Response()
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
            else:
                response = await original_route_handler(request)

        return preflight_handler


router = APIRouter(route_class=CORSHandler)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if True:
    app.include_router(category_router, prefix="/categories", tags=["Categories"])
    app.include_router(representant_router, prefix="/representants", tags=["Representants"])
    app.include_router(restaurant_router, prefix="/restaurants", tags=["Restaurants"])
    app.include_router(invoice_router, prefix="/invoices", tags=["Invoices"])
    app.include_router(menu_router, prefix="/menus", tags=["Menus"])
    app.include_router(table_router, prefix="/tables", tags=["Tables"])
    app.include_router(order_router, prefix="/orders", tags=["Orders"])
    app.include_router(table_session_router, prefix="/table-sessions", tags=["Table Sessions"])
    app.include_router(menu_item_router, prefix="/menu-items", tags=["Menu Items"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws/{restaurant_id}/{category}")
async def websocket_endpoint(
        websocket: WebSocket,
        restaurant_id: str,
        category: str):
    key = f"{restaurant_id}/{category}"
    await manager.connect(websocket, key)
    try:
        while True:
            # if websocket.application_state == WebSocketState.CONNECTED:
            data = await websocket.receive_text()
            data_json = json.loads(data)  # Deserialize JSON string to Python dict
            response_json = json.dumps({"message": category, "data": data_json})
            await manager.broadcast(response_json, key)
    except WebSocketDisconnect as close:
        print(f"WebSocket disconnected: {restaurant_id} to the websocket {category}")
        print(f"Reason: {close.reason} ({close.code})")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        await manager.disconnect(websocket, key)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/")
async def test_post(val: str):
    return {"POST Resquest": f"Working. See: {val}!"}


@app.on_event("startup")
async def startup_event():
    print("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources
    print("Shutting down...")


# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     response = await call_next(request)
#     print(f"Request headers: {request.headers}")
#     print(f"Response headers: {response.headers}")
#     return response


