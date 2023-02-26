from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Row, Group
from aiogram_dialog.widgets.text import Const

from database.sqlite import Database

db = Database()


base_cd = CallbackData("cars", "item", sep=".")
pagination_cd = CallbackData("pagination", "start", "end", "max_pages", "action", sep=".")

async def go_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Going on!")


async def run_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Running!")



def cars_keyboard(start: int=0, end: int=10):
    cars = db.select_all_cars()
    i = 1
    items = []
    for car in cars:
        # (1, 'Suzuki', '2019', 'Blue') - car object
        items.append(
            Button(Const(text=str(i)), id=base_cd.new(item=car[0]))
        )
        if i == 10:
            break
        else: i+=1

    bottom_buttons = [
        Button(
            Const(text="<"),
            id=pagination_cd.new(
                start=start, end=end, max_pages=len(cars), action="prev"
            )
        ),
        Button(
            Const(text="0"),
            id=pagination_cd.new(
                start=start, end=end, max_pages=len(cars), action="none"
            )
        ),
        Button(
            Const(text=">"),
            id=pagination_cd.new(
                start=start, end=end, max_pages=len(cars), action="next"
            )
        )
    ]
    bottom_row_buttons = Row(*bottom_buttons, id="pagination")
    markup = Group(*items, bottom_row_buttons, id="items_keyboard")
    return markup



row = Row(
    Button(Const("Go"), id="go", on_click=go_clicked),
    Button(Const("Run"), id="run", on_click=run_clicked),
    Button(Const("Fly"), id="fly"),
)