import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import NUMERALS_URL, KAB_RUS_DICTIONARY_URL, RANDOM_WORD_URL
from constants import MESSAGE_MAX_LEN, MIN_NUMBER, MAX_NUMBER
from utils import to_integer, normalize_message, enumerate_roman

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(f"ФIэхъус апщий! Введи какое-нибудь слово или число.")


@router.message(Command("random"))
async def random_handler(msg: Message):
    response = requests.get(f"{RANDOM_WORD_URL}").json()
    word = response['word']
    translations = response['translations']
    answer = ''
    for index, item in enumerate(translations, start=1):
        translation = item['translation']
        description = f"{item['description']}\n" if item['description'] else ''
        answer += f"{index}) <b>{word}</b>\n{translation}\n{description}\n"
    await msg.answer(answer)


@router.message()
async def message_handler(msg: Message):
    if number := to_integer(msg.text):
        if number in range(MIN_NUMBER, MAX_NUMBER + 1):
            response = requests.get(f"{NUMERALS_URL}{number}")
            await msg.answer(f"{response.json()['translate_decimal']}")
        else:
            await msg.answer(f"<i>Число должно быть в диапазоне [{MIN_NUMBER}-{MAX_NUMBER}]</i>")
    else:
        response = requests.get(f"{KAB_RUS_DICTIONARY_URL}{normalize_message(msg.text)}")
        if results := response.json()['results']:
            answer = ''
            for index, item in enumerate(results, start=1):
                translations = item['translations']
                if len(translations) > 1:
                    for index_roman, translation in enumerate_roman(translations):
                        if len(answer) > MESSAGE_MAX_LEN:
                            break
                        description = f"{translation['description']}\n" if translation['description'] else ''
                        answer += f"{index}) <b>{item['word']} ({index_roman})</b>\n{translation['translation']}\n{description}\n"
                else:
                    for translation in translations:
                        if len(answer) > MESSAGE_MAX_LEN:
                            break
                        description = f"{translation['description']}\n" if translation['description'] else ''
                        answer += f"{index}) <b>{item['word']}</b>\n{translation['translation']}\n{description}\n"
            await msg.answer(answer)
        else:
            await msg.answer("<i>По Вашему запросу ничего не найдено</i>")
