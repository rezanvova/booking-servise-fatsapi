import time
from contextlib import asynccontextmanager

from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from app.admin.auth import authentication_backend
from app.admin.models import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import setting
from app.database import engine
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.static.images.router import router as router_images
from app.users.router import router as router_users
from app.users.router import router2 as router_users2
import sentry_sdk

app = FastAPI()


sentry_sdk.init(
    dsn="https://8a45e53172dc52b179f47ab40d5c7201@o4508082300583936.ingest.de.sentry.io/4508082304647248",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_users2)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{setting.REDIS_HOST}:{setting.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # logger.info(f"Request processing time: {process_time}", extra={
    #     "process_time": round(process_time, 4)
    #  })
    response.headers["X-Process-Time"] = str(process_time)
    return response