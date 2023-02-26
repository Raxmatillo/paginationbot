from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ParseMode

from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const
from database.sqlite import Database

from environs import Env

from keyboards.inline.pagination_keyboards import cars_keyboard

env = Env()
env.read_env()

storage = MemoryStorage()
bot = Bot(token=env.str("BOT_TOKEN"))
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db="main.db")
registry = DialogRegistry(dp)


class MySG(StatesGroup):
    main = State()



cars = db.select_all_cars()[:10]

i = 1
text = ""
for car in cars:
    text += f"<b>{i})</b> {car[1]} - {car[2]}\n"
    i += 1


markup = cars_keyboard(0, 10)

main_window = Window(
    Const(text),
    markup,
    parse_mode=ParseMode.HTML,
    state=MySG.main,
)
dialog = Dialog(main_window)
registry.register(dialog)


@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)