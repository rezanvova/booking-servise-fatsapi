from app.users.models import Users
from app.bookings.models import Bookings
from sqladmin import ModelView
from app.hotels.models import Hotels, Rooms


class UsersAdmin(ModelView, model=Users):
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [Users.id, Users.email]


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    name = "Бронь"
    name_plural = "Брони"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Отель"
    name_plural = "Отели"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel]
    name = "Комната"
    name_plural = "Комнаты"
