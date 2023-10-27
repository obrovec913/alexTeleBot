from aiogram import types, Dispatcher
import os
import json
from keyboard.keybord import kb, get_cancel, get_kb
from aiogram.dispatcher import FSMContext
from models.modelstate import ClientStatesGroup, ClientStatesGroup1, ClientStatesGroup2, ClientStatesGroup3, ClientStatesGroup4, ClientStatesGroup5
from aiogram.dispatcher.filters import Text
from req.imgGenerator import image_generator
from aiogram.types import  InputFile
from req.text_to import text_to_speech
from req.speech_recognition import speech_recognition
from req.chat import chat_generation
from db.cr__db import prover_profile
from req.pdf_to_doc import pdf_converter_docx



async def startstate(messag: types.Message):
    if not await prover_profile(user_id=messag.from_user.id):
        await messag.answer('Изините, но вы не зарегистрированы', reply_markup=get_kb())
    await ClientStatesGroup.text1.set()
    await messag.reply("введите текст для генераций картинок", reply_markup=get_cancel())


async def cmd_start(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('Отменил',
                        reply_markup=kb)
    await state.finish()


async def prossNata(messag: types.Message, state: FSMContext):
    async with state.proxy() as  data:
        data['text1'] = messag.text
    async with state.proxy()as data:
        await messag.answer("пошла генерация, скоро вам придет ваша картинка")
        try:
            photoname = image_generator(data['text1'])
            
            photo = InputFile(f"{photoname}.jpg")

        except Exception:
            await messag.answer("что то пошло не так, попробуйте еще раз", reply_markup=kb)
            await state.finish()
        await messag.answer_photo(photo=photo,reply_markup=kb)
        os.remove(f"{photoname}.jpg")
        
    await state.finish()



async def startstate_to_cpeech(messag: types.Message):
    if not await prover_profile(user_id=messag.from_user.id):
        await messag.answer('Изините, но вы не зарегистрированы', reply_markup=get_kb())
    await ClientStatesGroup1.text1.set()
    await messag.reply("введите текст для генерации аудио файла с озвучкой вашего текста", reply_markup=get_cancel())
    

async def cmd_start_to_cpeech(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('Отменил',
                        reply_markup=kb)
    await state.finish()


async def text_to_cp(messag: types.Message, state: FSMContext):
    async with state.proxy() as  data:
        data['text1'] = messag.text
    async with state.proxy()as data:
        await messag.answer("пошла генерация, скоро вам придет ваша аудио запись")
        try:
            audio = text_to_speech(data['text1'])

            await messag.answer_audio(audio=audio, reply_markup=kb)    
        except Exception:
            await messag.answer("что то пошло не так, попробуйте еще раз", reply_markup=kb)
            await state.finish()
    
    await state.finish()


async def startstate_to_text(messag: types.Message):
    if not await prover_profile(user_id=messag.from_user.id):
        await messag.answer('Изините, но вы не зарегистрированы', reply_markup=get_kb())
    
    await ClientStatesGroup2.text1.set()
    await messag.reply("пришлите аудио файл для того чтобы получить из него весь текст в текстовом документе", reply_markup=get_cancel())
    



async def speech_to_text(messag: types.Message, state: FSMContext):
    a = messag.audio.file_id
    await messag.audio.download(destination_file=f"./audio/{a}.mp3")
    await messag.answer("ващ файл принят... ")
    async with state.proxy() as  data:
        data['text1'] = a
    async with state.proxy()as data:
        await messag.answer("пошла перевод голоса в текст")
        try:
            await speech_recognition(fileame=f'./audio/{data["text1"]}.mp3', fi=messag.audio.file_name)
            await messag.answer('пошла отправка файла  в текстовом формате')
            await messag.answer_document(open(f'{messag.audio.file_name}.txt', "rb"), reply_markup=kb)
            await os.remove(f'{messag.audio.file_name}.txt') 
            await os.remove(f'./audio/{data["text1"]}.mp3')            

        except Exception as e:
            await messag.answer("что то пошло не так, попробуйте еще раз", reply_markup=kb)
            await state.finish()
    


    await messag.answer_document(open(f'{messag.audio.file_name}.txt', "rb"), reply_markup=kb)
    await os.remove(f'{messag.audio.file_name}.txt') 
    await os.remove(f'./audio/{data["text1"]}.mp3')         
    await state.finish()


async def startstate_to_dipf(messag: types.Message):
    if not await prover_profile(user_id=messag.from_user.id):
        await messag.answer('Изините, но вы не зарегистрированы', reply_markup=get_kb())
    await ClientStatesGroup3.text1.set()
    await messag.reply("пришлите видео для замены в нем лиц", reply_markup=get_cancel())


async def video_to_dipf(messag: types.Message, state: FSMContext):
    a = messag.video.file_name
    await messag.video.download(destination_file=f"./video/{a}")
    await messag.answer("ващ файл принят... ")
    async with state.proxy() as  data:
        data['text1'] = a
    await ClientStatesGroup3.next()
    await messag.answer("пришлите фото с лицом человека которое вы хотите заметить в  видео", reply_markup=get_cancel())



async def photo_to_dipf(messag: types.Message, state: FSMContext):
    a = messag.photo[-1].file_id
    await messag.photo[-1].download(destination_file=f"./photo/{a}.jpg")
    await messag.answer("ващ файл принят... ")
    async with state.proxy() as  data:
        data['photo'] = a
    async with state.proxy()as data:
        await messag.answer("пошла проверка видео")
        user = {messag.from_user.id:[{data['text1']:data['photo']}]}
        with open(f'applications/{messag.from_user.id}.json', 'w') as file:
            json.dump(user, file, indent=3, ensure_ascii=False)
    await messag.answer("наш модератор проверит ваше видео и фото чтоб там не было противозаконного и бот пришлет вам результат... ожидайте", reply_markup=kb)
    await state.finish()


async def startstate_to_chat(messag: types.Message):
    if not await  prover_profile(user_id=messag.from_user.id):
        await messag.answer('Изините, но вы не зарегистрированы', reply_markup=get_kb())
    await ClientStatesGroup4.text1.set()
    await messag.reply("Добро пожаловать в GPT-CHAT, задавайте свои вопросы.", reply_markup=get_cancel())


async def chat_to_text(messag: types.Message, state: FSMContext):
    try:
        await messag.answer("ващ вопрос принят... ")
        async with state.proxy() as  data:
            data['text1'] = messag.text
        
        
        ot, mess = chat_generation(messag.text)
        await messag.answer(ot,reply_markup=get_cancel())
    except Exception as e:
        print(e)

        await messag.answer("что то пошло не так... попробуйте еще раз.", reply_markup=get_cancel())
    

async def startstate_to_pdf(messag: types.Message):
    if not await  prover_profile(user_id=messag.from_user.id):
        await messag.answer('Изините, но вы не зарегистрированы', reply_markup=get_kb())
    await ClientStatesGroup5.text1.set()
    await messag.reply("Отправьте pdf документ чтоб конвентироавть его в docx.", reply_markup=get_cancel())


async def pdf_to_docx(messag: types.Message, state: FSMContext):
    try:
        await messag.answer("ващ вопрос принят... ")
        await messag.document.download(destination_file=f"db/{messag.document.file_name}")
        docx = pdf_converter_docx(f"db/{messag.document.file_name}")
        await messag.answer_document(document=open(docx, 'rb'), reply_markup=kb)
    except Exception as e:
        print(e)

        await messag.answer("что то пошло не так... попробуйте еще раз.", reply_markup=kb)
    await state.finish()
    


def registerKlient(dp: Dispatcher):
    dp.register_message_handler(startstate, Text(equals='Генерация картинок!', ignore_case=True), state=None)
    dp.register_message_handler(cmd_start, commands=['cancel'], state='*')
    dp.register_message_handler(prossNata, state=ClientStatesGroup.text1)
    dp.register_message_handler(startstate_to_cpeech, Text(equals='Генерация аудио озвучки!', ignore_case=True), state=None)
    dp.register_message_handler(cmd_start_to_cpeech, commands=['cancel'], state='*')
    dp.register_message_handler(text_to_cp, state=ClientStatesGroup1.text1)
    dp.register_message_handler(startstate_to_text, Text(equals='Генерация текста из аудио файла!', ignore_case=True), state=None)
    dp.register_message_handler(speech_to_text, content_types=["audio"], state=ClientStatesGroup2.text1)
    dp.register_message_handler(startstate_to_dipf, Text(equals='Подать заявку на дипфейк', ignore_case=True), state=None)
    dp.register_message_handler(video_to_dipf, content_types=["video"], state=ClientStatesGroup3.text1)
    dp.register_message_handler(photo_to_dipf, content_types=["photo"], state=ClientStatesGroup3.photo)
    dp.register_message_handler(startstate_to_chat, Text(equals='Чат gpt', ignore_case=True), state=None)
    dp.register_message_handler(chat_to_text, content_types=["text"], state=ClientStatesGroup4.text1)
    dp.register_message_handler(startstate_to_pdf, Text(equals='конвертер pdf в docx', ignore_case=True), state=None)
    dp.register_message_handler(pdf_to_docx, content_types=["document"], state=ClientStatesGroup5.text1)