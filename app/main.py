
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from fastapi import HTTPException

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

# caching dependencies
from contextlib import asynccontextmanager
import redis.asyncio as aioredis
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

import json
from typing import Callable

from app.core.dependencies import get_settings
from app.websocket.manager import manager

from app.api.business import router as business_router
from app.api.invitationToken import router as invitation_token_router
from app.api.user import router as user_router
from app.api.restaurant import router as restaurant_router
from app.api.category import router as category_router
from app.api.invoice import router as invoice_router
from app.api.menu import router as menu_router
from app.api.table import router as table_router
from app.api.order import router as order_router
from app.api.tableSession import router as table_session_router
from app.api.menuItem import router as menu_item_router
from app.api.page import router as page_router
from app.api.analytics import router as analytics_router


import os
print("ENV CHECK:", os.getenv("GOOGLE_CLOUD_CREDENTIALS"))


settings = get_settings()

@asynccontextmanager
async def lifespan(application: FastAPI):
    print("Starting up...")

    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield

    await redis.close()

    print("Shutting down...")


app = FastAPI(lifespan=lifespan,
              title=settings.TITLE,
              description=settings.DESCRIPTION)


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

app.include_router(business_router, prefix="/service", tags=["General"])
app.include_router(invitation_token_router, prefix="/invitation-tokens", tags=["Invitation Tokens"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(restaurant_router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(invoice_router, prefix="/invoices", tags=["Invoices"])
app.include_router(menu_router, prefix="/menus", tags=["Menus"])
app.include_router(table_router, prefix="/tables", tags=["Tables"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(table_session_router, prefix="/table-sessions", tags=["Table Sessions"])
app.include_router(menu_item_router, prefix="/menu-items", tags=["Menu Items"])
app.include_router(page_router, prefix="/pages", tags=["Pages"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://neemble-eat.ao", "http://localhost:5173"],
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
@cache(expire=60)
async def read_root():
    return {"Hello": "World"}
