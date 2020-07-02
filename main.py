# -*- coding: utf-8 -*-

import config
import datetime
import asyncio
import base
import os
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import test

# from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

message_with_inline_keyboard = None

PATH = os.getcwd()
PATHimages = str(os.getcwd()) + '\images\\'
PATHenemies = str(os.getcwd()) + '\images\enemies\\'
PATHbuild = str(os.getcwd()) + '\images\\buildings\\'


async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type)
    print('Chat:', content_type, chat_type, chat_id,
          datetime.datetime.fromtimestamp(int(msg['date'])).strftime('(%Y-%m-%d %H:%M:%S)'))

    if content_type != 'text':
        if content_type == 'sticker':
            print(msg['sticker'].get('file_id'))  # Получаем код стикера

    elif content_type == 'text':
        print(msg['text'].encode('unicode-escape').decode(
            'ascii'))  # Получаем код текста (смайликов), доделать print текста

        command = msg['text'].lower()
        if command == '/start':
            uid = str(chat_id)
            usr = uid
            base.new_user(uid)
            if base.get_user(uid).get('game'):

                img1 = open(PATHimages + 'img1.jpg', 'rb')
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['Осмотреть шкафчики в поиске провизии'],
                    ['Не тратить время на поиски и выйти']], resize_keyboard=True)
                await bot.sendMessage(chat_id, 'Над радиационными тучами встаёт солнце...')
                await bot.sendPhoto(chat_id, photo=img1,
                                    caption='Здравствуй, %s! ' % msg["from"].get("first_name") + config.dintro,
                                    reply_markup=markup)

                data = base.get_user(uid)
                data['game'] = False  # Game over=False, продолжаем игру
                base.save_user(usr, uid, data)
                img1.close()
                # =============Основной цикл игры==========
                # tick() - Пока не работает

                # =========================================

            else:
                print(msg["from"].get("last_name", msg["from"].get(
                    "last_name")))  # Приветствие пользователя по никнейму, работает неккоректно
                if msg["from"].get("username") == "None":
                    markup = ReplyKeyboardMarkup(keyboard=[
                        ['Панель действий']], resize_keyboard=True)
                    await bot.sendMessage(chat_id,
                                          "Эй, %s!" % msg["from"].get("first_name") + ' Ты ведь уже начал игру..',
                                          reply_markup=markup)
                else:
                    markup = ReplyKeyboardMarkup(keyboard=[
                        ['Панель действий']], resize_keyboard=True)
                    await bot.sendMessage(chat_id,
                                          "Эй, %s!" % msg["from"].get("username") + ' Ты ведь уже начал игру..',
                                          reply_markup=markup)

        # ==================================================      Вылазка, поселение и тд

        uid = str(chat_id)
        usr = uid
        data = base.get_user(uid)
        if command == 'c' or msg['text'] == '\U0001f519 Назад' or msg['text'] == 'Понял' or msg[
            'text'] == 'Панель действий' or msg['text'] == '/stats':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['\U0001f6b7 Вылазка', '\U0001f468\U0001f3fb\u200d\U0001f3a4 Персонаж', '\U0001f4dc Модули'],
                ['\U0001f303 Найт-сити', '\U0001f3de Поселение', '\U0001f3ec Магазин'],
                ['/restart']], resize_keyboard=True)

            await bot.sendMessage(chat_id, "\U0001f4be*Статистика*: \n`ID%s`" % uid + "\n`Выживших: %s`" % len(
                os.listdir(base.USERS_PATH)) + "\n\n\U0001f468\U0001f3fb\u200d\U0001f3a4 YourName" +
                                  "\n\U0001f396 Уровень: %s" % data['level'] + "\n\U0001f52e Опыт : %s" % data['exp'] +
                                  "/%s" % data['expto'] + '\n\n\U0001f9e8 Урон: %s' % data[
                                      'damage'] + "\n\n\U0001f4a0 Крипта: %s" % data[
                                      'crypt'] + "\n\U0001f4b5 Доллары: %s" % data['money'] +
                                  "\n\U0001f333 Дерево: %s" % data['wood'] + "\n\U0001f529 Металл: %s" % data['iron'] +
                                  "\n\n\U0001f50b Запас сил: %s" % data['stamina'] +
                                  " / %s" % data['maxstamina'] + "\n\n\u23f1 Восстановление: %s" % data[
                                      'timestamina'] + " сек" + "\n\n `Подробно` /me", reply_markup=markup,
                                  parse_mode='markdown')

        #########################################################################
        elif command == 'Инфа':  # Дебаг базы данных
            text = '|' + str(base.get_user(uid)).replace(',', '|') + '|'
            print(text)
            await bot.sendMessage(chat_id, text)
        # ===================================================================== UPDATE
        elif msg['text'].split(' ')[0] == '/update':  # Update DATA
            if msg['from'].get('username') == 'xXZyzzXx':
                if len(msg['text'].split(' ')) > 3:
                    if msg['text'].split(' ')[3] == 'int':
                        await bot.sendMessage(chat_id, 'Выбран цифровой тип данных')
                        new_data = {msg['text'].split(' ')[1]: int(msg['text'].split(' ')[2])}
                        base.update_data(new_data)
                    elif msg['text'].split(' ')[3] == 'bool':
                        await bot.sendMessage(chat_id, 'Выбран тип данных логических переменных')
                        new_data = {msg['text'].split(' ')[1]: bool(msg['text'].split(' ')[2])}
                        base.update_data(new_data)
                else:
                    new_data = {msg['text'].split(' ')[1]: msg['text'].split(' ')[2]}
                    base.update_data(new_data)
                    await bot.sendMessage(chat_id,
                                          'Значение поменяно на обычное. Для цифры необходимо ввести текст в формате /update переменная значение int/bool')
            else:
                await bot.sendMessage(chat_id, "You don't have an enought permission to doing that..")

        elif msg['text'].split(' ')[0] == '/updateid':  # Update DATA for ID user
            if msg['from'].get('username') == 'xXZyzzXx':
                if len(msg['text'].split(' ')) > 3:
                    if msg['text'].split(' ')[4] == 'int':
                        await bot.sendMessage(chat_id, 'Выбран цифровой тип данных')
                        new_data = {msg['text'].split(' ')[2]: int(msg['text'].split(' ')[3])}
                        uid = msg['text'].split(' ')[1]
                        base.update_data_id(new_data, uid)
                    elif msg['text'].split(' ')[4] == 'bool':
                        await bot.sendMessage(chat_id, 'Выбран тип данных логических переменных')
                        new_data = {msg['text'].split(' ')[2]: bool(msg['text'].split(' ')[3])}
                        uid = msg['text'].split(' ')[1]
                        base.update_data_id(new_data, uid)
                    elif msg['text'].split(' ')[4] == 'str':
                        new_data = {msg['text'].split(' ')[2]: msg['text'].split(' ')[3]}
                        uid = msg['text'].split(' ')[1]
                        base.update_data_id(new_data, uid)
                        await bot.sendMessage(chat_id, 'Значение поменяно на строка')
            else:
                await bot.sendMessage(chat_id, "You don't have an enought permission to doing that..")

        elif msg['text'].split(' ')[0] == '/users':
            if msg['from'].get('username') == 'xXZyzzXx':
                await bot.sendMessage(chat_id, os.listdir(base.USERS_PATH))
            else:
                await bot.sendMessage(chat_id, "You don't have an enought permission to doing that..")

        # ============Cюжетка============================================= (Доделать анти-абуз квестов)
        elif msg['text'] == 'Осмотреть шкафчики в поиске провизии':
            img2 = open(PATHimages + 'img2.jpg', 'rb')
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Засунуть руку подальше'],
                ['Взять первые банки и уйти']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'Надеюсь, будет чем подкрепиться...')
            await bot.sendPhoto(chat_id, photo=img2,
                                caption='Ты открываешь дверцу шкафа и видишь кучу банок с стёртыми названиями.',
                                reply_markup=markup)
            img2.close()
        elif msg['text'] == 'Засунуть руку подальше':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Сложить пожитки в рюкзак и уйти']], resize_keyboard=True)
            await bot.sendMessage(chat_id,
                                  'Ничего полезного.. Срок годности некоторых продуктов закончился много лет назад, надо уходить.',
                                  reply_markup=markup)

        elif msg['text'] == 'Взять первые банки и уйти' or msg['text'] == 'Сложить пожитки в рюкзак и уйти':
            img5 = open(PATHimages + 'img5.jpg', 'rb')
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Продолжить движение']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'Расставив найденное на стол, ты начинаешь проводить ревизию...')
            await bot.sendPhoto(chat_id, photo=img5,
                                caption='\U0001f392 Рюкзак:\n\n+2 Консервы "Говяжий дошик"\n+1 Бутылка чистой воды ',
                                reply_markup=markup)
            img5.close()

        elif msg['text'] == 'Не тратить время на поиски и выйти' or msg['text'] == 'Продолжить движение':
            img3 = open(PATHimages + 'img3.jpg', 'rb')
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Подойти ближе, чтоб разглядеть врага'],
                ['Потихоньку отойти назад и убежать']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'Вещи собраны и герой потихоньку двигается в сторону двери...')
            await bot.sendPhoto(chat_id, photo=img3,
                                caption='Просторы пустоши были невероятно красивы. В этой атмосфере постапокалиптического утра чуствовалось что-то загадочное. Твоё внимание привлёк шелест кустов в ста метрах и рука опустилась на спусковые крючки обреза.',
                                reply_markup=markup)
            img3.close()
        elif msg['text'] == 'Подойти ближе, чтоб разглядеть врага':
            img6 = open(PATHenemies + 'img6.jpg', 'rb')
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Активировать боевой модуль'],
                ['Убежать']], resize_keyboard=True)
            await bot.sendMessage(chat_id,
                                  'По мере приближения к источнику шума стало понятно, что перед тобой виднеется гигантская *крыса*..',
                                  parse_mode='Markdown')
            await bot.sendPhoto(chat_id, photo=img6,
                                caption='Такой большой размер (животного) ты видел пару недель назад в эротическом сне, что заставляет тебя принимать какие-то меры по устранению проблемы.',
                                reply_markup=markup)
            img6.close()
        elif msg['text'] == 'Убежать' or msg['text'] == 'Потихоньку отойти назад и убежать':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Понял']], resize_keyboard=True)
            await bot.sendMessage(chat_id,
                                  'Едва засверкав пятками, ты подскочил с настила из листьев и судорожно огляделся по сторонам. Это был лишь сон. На самом деле ты проснулся в лагере, который ждёт своего развития уже несколько недель с момента его основания. Предлагаю тебе осмотреться по сторонам и найти себе занятия по душе. \n\nПоверь, в пустоши их хватает.',
                                  reply_markup=markup)
        elif msg['text'] == 'Активировать боевой модуль':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Понял']], resize_keyboard=True)
            await bot.sendMessage(chat_id,
                                  text='Едва активировав боевой модуль, ты подскочил с настила из листьев и судорожно огляделся по сторонам. Это был лишь сон. На самом деле ты проснулся в лагере, который ждёт своего развития уже несколько недель с момента его основания. Предлагаю тебе осмотреться по сторонам и найти себе занятия по душе. \n\nПоверь, в пустоши их хватает.',
                                  reply_markup=markup)
        # ================================================================

        elif command == 'admin':  # Переделать админ панель под нужные опции, добавить трекер по пользователям

            if msg['from'].get('username') == 'xXZyzzXx' or chat_id == 624737506:
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['+exp', '+money', '+crypt', '+wood', '+iron', '+stamina'],
                    ['Инфа', '\U0001f519 Назад']], resize_keyboard=True)
                await bot.sendMessage(chat_id, 'Выбери действие: ', reply_markup=markup)
        # =======Вылазка===
        elif msg['text'] == '\U0001f6b7 Вылазка':
            img10 = open(PATHimages + 'back.jpg', 'rb')
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Отправиться в пустошь'],
                ['\U0001f519 Назад']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'Выходим в *зону опасности*...', parse_mode='Markdown')
            await bot.sendPhoto(chat_id, photo=img10,
                                caption='Вылазки такого типа требуют хорошей подготовки и сноровки. Ты точно уверен в своих силах?',
                                reply_markup=markup)
            img10.close()
        # ==========Магазин===
        elif msg['text'] == '\U0001f3ec Магазин':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['Плазменные пушки', 'Броня'],
                ['\U0001f519 Назад']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'Выберите интересующий товар:', parse_mode='Markdown', reply_markup=markup)
        # ===================Персонаж
        elif msg['text'] == '\U0001f468\U0001f3fb\u200d\U0001f3a4 Персонаж':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['\U0001f9f0 Инвентарь'],
                ['\U0001f519 Назад']], resize_keyboard=True)
            await bot.sendMessage(chat_id, "\U0001f4be*Статистика*: \n`ID%s`" % uid + "\n`Выживших: %s`" % len(
                os.listdir(base.USERS_PATH)) + "\n\n\U0001f468\U0001f3fb\u200d\U0001f3a4 %s" % msg["from"].get(
                "username") +
                                  "\n\U0001f396 Уровень: %s" % data['level'] + "\n\U0001f52e Опыт : %s" % data['exp'] +
                                  "/%s" % data['expto'] + '\n\n\U0001f9e8 Урон: %s' % data[
                                      'damage'] + "\n\n\U0001f4a0 Крипта: %s" % data[
                                      'crypt'] + "\n\U0001f4b5 Доллары: %s" % data['money'] +
                                  "\n\U0001f333 Дерево: %s" % data['wood'] + "\n\U0001f529 Металл: %s" % data['iron'] +
                                  "\n\n\U0001f50b Запас сил: %s" % data['stamina'] +
                                  " / %s" % data['maxstamina'] + "\n\n\u23f1 Восстановление: %s" % data[
                                      'timestamina'] + " сек" + "\n\n `Подробно` /me", reply_markup=markup,
                                  parse_mode='Markdown')
        # ==============Инвентарь===
        elif msg['text'] == '\U0001f9f0 Инвентарь':

            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='[%s] Инвентарь' % len(base.get_user(uid).get('inv').keys()),
                                      callback_data='inv')],
                [InlineKeyboardButton(text='Амуниция', callback_data='amunition'),
                 InlineKeyboardButton(text='Провизия', callback_data='food')]])
            global message_with_inline_keyboard
            message_with_inline_keyboard = await bot.sendMessage(chat_id, '\U0001f392 *Рюкзак* %s' % len(
                base.get_user(uid).get('inv')) + '/%s' % base.get_user(uid).get('inv_max_size') +
                                                                 '\n\n\U0001f468\U0001f3fb\u200d\U0001f3a4 %s' % msg[
                                                                     "from"].get("username") +
                                                                 '\n\n\u25aa\ufe0f Шлем: [%s]' % base.get_user(uid).get(
                'shlem') +
                                                                 '\n\u25aa\ufe0f Нагрудник: [%s]' % base.get_user(
                uid).get('chest') +
                                                                 '\n\u25aa\ufe0f Поножи: [%s]' % base.get_user(uid).get(
                'ponozhi') +
                                                                 '\n\u25aa\ufe0f Сапоги: [%s]' % base.get_user(uid).get(
                'boots') +
                                                                 '\n\n\u25aa\ufe0f Оружие: [%s]' % base.get_user(
                uid).get('gun') +
                                                                 '\n\n\u25aa\ufe0f Еда: [%s]' % base.get_user(uid).get(
                'food'), parse_mode='Markdown', reply_markup=markup)

        # ===================Пушки===
        elif msg['text'] == 'Плазменные пушки':
            index = base.get_user(uid).get('index')
            shp = base.get_user(uid).get('shop')
            data['index'] = 0
            base.save_user(usr, uid, data)
            ke = list(shp.keys())  # Список ключей словаря айтемов

            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Купить', callback_data='bought')],
                [InlineKeyboardButton(text='\u2b05\ufe0f', callback_data='left'),
                 InlineKeyboardButton(text='\u27a1\ufe0f', callback_data='right')]
            ])

            text = '\u2694\ufe0f *{}* [{}/{}]\n\n\U0001f9e8 Урон: {}\n\n\U0001f9ff Некое свойство: {}\n\nДоступно: ' \
                   '\U0001f4b5 {}\nСтоимость: \U0001f4b5 {}'.format(ke[index], index + 1, len(ke),
                                                                    shp.get(ke[index])[0],
                                                                    shp.get(ke[index])[1], base.get_user(uid).get(
                    'money'), shp.get(ke[index])[2])

            message_with_inline_keyboard = await bot.sendMessage(chat_id, text, reply_markup=markup,
                                                                 parse_mode='Markdown')

            # ==============Поселение====
        elif msg['text'] == '\U0001f3de Поселение' or msg['text'] == '\u2b05\ufe0f Назад':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['\U0001f3e1 Участок', '\U0001f417 Хозяйство', '\U0001f6e0 Крафт'],
                ['\U0001f527 Улучшения', '\U0001f3d7 Строения', '\U0001f519 Назад']], resize_keyboard=True)
            if data['status1'] == 1:
                await bot.sendMessage(chat_id, config.status,
                                      reply_markup=markup, parse_mode='Markdown')
            elif data['status1'] == 2:
                await bot.sendMessage(chat_id, config.status2, reply_markup=markup, parse_mode='Markdown')

        # =========================================== Модули
        elif msg['text'] == '\U0001f4dc Модули':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['\U0001f519 Назад']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'Пока ещё нет модулей', parse_mode='Markdown')
        # ============================================= Участок
        elif msg['text'] == '\U0001f3e1 Участок':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['\U0001f3e0 Дом', '\U0001f331 Огород'],
                ['\U0001f4a7 Колодец', '\u2b05\ufe0f Назад']], resize_keyboard=True)
            await bot.sendMessage(chat_id,
                                  'На участке временно пусто, найдите зерна а так же постройте грядки в разделе "Строения"',
                                  reply_markup=markup)
        # ================================================= Колодец
        elif msg['text'] == '\U0001f4a7 Колодец':
            if data['well'] == '\u2705':
                img7 = open(PATHbuild + 'well.jpg', 'rb')
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['Набрать воды', 'Кинуть монетку'],
                    ['\U0001f3e1 Участок']], resize_keyboard=True)
                await bot.sendPhoto(chat_id, photo=img7, caption='Вы можете набрать чистой воды для полива огорода.',
                                    reply_markup=markup)
                img7.close()
            else:
                img8 = open(PATHbuild + 'nothing.jpg', 'rb')
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\U0001f3d7 Строения'],
                    ['\U0001f3e1 Участок']], resize_keyboard=True)
                await bot.sendPhoto(chat_id, photo=img8, caption='Необходимо построить колодец в \U0001f3d7 Строениях.',
                                    reply_markup=markup)
                img8.close()
        # ===================================================== Дом
        elif msg['text'] == '\U0001f3e0 Дом':
            if data['house'] == '\u2705':
                img9 = open(PATHbuild + 'house.jpg', 'rb')
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['Поспать', 'Сложить вещи'],
                    ['\U0001f3e1 Участок']], resize_keyboard=True)
                await bot.sendPhoto(chat_id, photo=img9, caption='Нет ничего лучше, чем уют собственного дома',
                                    reply_markup=markup)
                img9.close()
            else:
                img8 = open(PATHbuild + 'nothing.jpg', 'rb')
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\U0001f3d7 Строения'],
                    ['\U0001f3e1 Участок']], resize_keyboard=True)
                await bot.sendPhoto(chat_id, photo=img8, caption='Необходимо построить дом в \U0001f3d7 Строениях.',
                                    reply_markup=markup)
                img8.close()
        # ============================================================= Animals
        elif msg['text'] == '\U0001f417 Хозяйство':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['\u2b05\ufe0f Назад']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'В загоне сейчас ' + str(config.animal) + ' животных', reply_markup=markup)
        # =============================================================== Craft

        elif msg['text'] == '\U0001f6e0 Крафт':
            if data['workspace'] == True:
                crf = base.get_user(uid).get('crafts')
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\u267b\ufe0f Терраформировочная машина'],
                    ['\u2b05\ufe0f Назад']], resize_keyboard=True)

                text = 'Ты заходишь в мастерскую, обвешанную инструментами разных эпох, подходишь к верстаку и ' \
                       'включаешь у себя в мозгу `строительный модуль`. Дряблые процессоры выдали обширный (нет) ' \
                       'список доступных крафтов и ты приступил к делу.\n\n`Ресурсы:` \U0001f333 {} дерева,' \
                       '\U0001f529 {} металла,\U0001f50b {} выносливости'.format(data['wood'], data['iron'],
                                                                                 data['stamina'])
                for x in crf:
                    text = text + "\n\n\u25ab\ufe0f *{}* - \U0001f333 {}, \U0001f529 {}, \U0001f50b {} {}".format(
                        x, crf.get(x)[0], crf.get(x)[1], crf.get(x)[2], crf.get(x)[3])

                await bot.sendMessage(chat_id, text, reply_markup=markup, parse_mode='Markdown')

            else:
                if data['wood'] >= 100:
                    markup = ReplyKeyboardMarkup(keyboard=[
                        ['Построить верстак'],
                        ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                    await bot.sendMessage(chat_id,
                                          'В твоей мастерской ещё нет верстака, для постройки необходимо 100 \U0001f333 дерева. Сейчас у тебя ' + str(
                                              data['wood']) + ' \U0001f333 дерева. Можешь приступать к созданию.',
                                          reply_markup=markup)
                else:
                    markup = ReplyKeyboardMarkup(keyboard=[
                        ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                    await bot.sendMessage(chat_id,
                                          'В твоей мастерской ещё нет верстака, для постройки необходимо 100 \U0001f333 дерева! У тебя ' + str(
                                              data['wood']) + ' \U0001f333 дерева. Подсобирай ещё ресурсов.',
                                          reply_markup=markup)
        # ======================================================================Terra
        elif msg['text'] == '\u267b\ufe0f Терраформировочная машина':
            if data['workspace'] == True and data['terra'] == '\u2705':
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\u267b\ufe0f Терраформировать'],
                    ['Статус земли', '\U0001f6e0 Крафт']], resize_keyboard=True)
                await bot.sendMessage(chat_id,
                                      'Огромная махина зависла в ожидании указаний.\n\n`Доступная \U0001f4a0 Крипта: %s`' %
                                      data['crypt'] +
                                      '\n\nСтоимость терраформирования: 100 \U0001f4a0', reply_markup=markup,
                                      parse_mode='Markdown')
            else:
                await bot.sendMessage(chat_id,
                                      'Тебе необходимо построить верстак и терраформировочную машину прежде, чем пользоваться ей.')

        elif msg['text'] == 'sudo python terra.py install':
            if data['workspace'] == True and data['terra'] == '\u2705' and data['crypt'] >= 100 and data[
                'status1'] == 1:
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                crypt = int(data['crypt']) - 100
                data['crypt'] = crypt
                data['status1'] = 2
                base.save_user(usr, uid, data)
                await bot.sendMessage(chat_id, 'Терраформирование произведено успешно.', reply_markup=markup)
            elif data['status1'] == 2:
                await bot.sendMessage(chat_id, 'Терраформирование уже было произведено.')
            else:
                await bot.sendMessage(chat_id, 'Без оборудования и крипты такими вещами заниматься рано..')

        elif msg['text'] == '\u267b\ufe0f Терраформировать':
            if data['workspace'] == True and data['terra'] == '\u2705' and data['crypt'] >= 100 and data[
                'status1'] == 1:
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                await bot.sendMessage(chat_id,
                                      '\U0001f5a5 JARVIS Terminal [[Version 7.1.2336]]\n(c) Corporation JARVIS, 2044. All rights reserved.\n\n' +
                                      '`F:\\Users\%s>`' % msg['from'].get(
                                          'username') + 'Для терраформирования необходимо обойти систему безопасности.\n`F:\\Users\%s>`' %
                                      msg['from'].get(
                                          'username') + 'Запустите скрипт.\n\n`sudo python terra.py install`',
                                      reply_markup=markup, parse_mode='Markdown')
            elif data['status1'] == 2:
                await bot.sendMessage(chat_id, 'Терраформирование уже было произведено.')
            else:
                await bot.sendMessage(chat_id, 'Без оборудования и крипты такими вещами заниматься рано..')
                # ================================================================= верстак
        elif msg['text'] == 'Построить верстак':
            if data['wood'] >= 100 and data['workspace'] == False:
                wood = int(data['wood']) - 100
                data['wood'] = wood
                data['workspace'] = True
                base.save_user(usr, uid, data)
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\U0001f6e0 Крафт'],
                    ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                await bot.sendMessage(chat_id,
                                      'Ты успешно создал верстак, теперь в твоём лагере доступны продвинутые крафты.',
                                      reply_markup=markup)
            else:
                await bot.sendMessage(chat_id, 'У тебя не хватает дерева либо ты уже построил верстак.')
        # ============================================================= Улучшения
        elif msg['text'] == '\U0001f527 Улучшения':
            markup = ReplyKeyboardMarkup(keyboard=[
                ['\u2b05\ufe0f Назад']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'Временно нечего улучшать. Уходи..', reply_markup=markup)
        # ================================================================= Строения
        elif msg['text'] == '\U0001f3d7 Строения':
            bld = base.get_user(uid).get('buildings')
            markup = ReplyKeyboardMarkup(keyboard=[
                ['\u2b05\ufe0f Назад']], resize_keyboard=True)

            text = 'На текущий момент известны только такие чертежи зданий:\n\n`Ресурсы:` \U0001f333 {} дерева, ' \
                   '\U0001f529 {} металла, \U0001f50b {} выносливости'.format(data['wood'], data['iron'],
                                                                              data['stamina'])
            for x in bld:
                text = text + '\n\n\u25ab\ufe0f *{}* - \U0001f333 {}, \U0001f529 {}, \U0001f50b {}   {}'.format(x,
                                                                                                                bld.get(
                                                                                                                    x)[
                                                                                                                    0],
                                                                                                                bld.get(
                                                                                                                    x)[
                                                                                                                    1],
                                                                                                                bld.get(
                                                                                                                    x)[
                                                                                                                    2],
                                                                                                                bld.get(
                                                                                                                    x)[
                                                                                                                    3])

            await bot.sendMessage(chat_id, text, reply_markup=markup, parse_mode='Markdown')
            '''
            await bot.sendMessage(chat_id, "На текущий момент известны только такие чертежи зданий:\n\n`Ресурсы:` "
                                           "\U0001f333 {} дерева, \U0001f529 {} металла, \U0001f50b {} "
                                           "выносливости\n\n\u25ab\ufe0f *Колодец* - \U0001f333 {}, \U0001f529 {}, "
                                           "\U0001f50b {}   {}\n\n\u25ab\ufe0f *Грядка* - \U0001f333 {}, \U0001f50b {} "
                                           "  {}\n\n\u25ab\ufe0f *Дом* - \U0001f333 {}, \U0001f50b {}   {}".format(
                data['wood'], data['iron'], data['stamina'], bld.get('Колодец')[0], bld.get('Колодец')[1],
                bld.get('Колодец')[2], data['well'], bld.get('Грядка')[0], bld.get('Грядка')[2], data['garden'],
                bld.get('Дом')[0], bld.get('Дом')[2], data['house']), reply_markup=markup, parse_mode='Markdown')
            '''
        elif msg['text'] == '/create01':
            if data['wood'] >= 100 and data['iron'] >= 150 and data['stamina'] >= 5 and data['well'] != '\u2705':
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\U0001f4a7 Колодец'],
                    ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                data['well'] = '\u2705'
                wood = int(data['wood']) - 100
                iron = int(data['iron']) - 150
                stamina = int(data['stamina']) - 5
                data['wood'] = wood
                data['iron'] = iron
                data['stamina'] = stamina
                base.save_user(usr, uid, data)
                await bot.sendMessage(chat_id, 'Ты создал колодец. Пользуйся в удовольствие.', reply_markup=markup)
            elif data['well'] == '\u2705':
                await bot.sendMessage(chat_id, 'У тебя уже есть колодец. Зачем тебе второй?)')
            else:
                await bot.sendMessage(chat_id, 'Не хватает ресурсов для постройки колодца!')
        elif msg['text'] == '/create02':
            if data['wood'] >= 200 and data['stamina'] >= 2 and data['garden'] != '\u2705':
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\U0001f331 Огород'],
                    ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                data['garden'] = '\u2705'
                wood = int(data['wood']) - 200
                stamina = int(data['stamina']) - 2
                data['wood'] = wood
                data['stamina'] = stamina
                base.save_user(usr, uid, data)
                await bot.sendMessage(chat_id, 'Ты создал огород. Пользуйся в удовольствие.', reply_markup=markup)
            elif data['garden'] == '\u2705':
                await bot.sendMessage(chat_id, 'У тебя уже есть огород. Зачем тебе второй?)')
            else:
                await bot.sendMessage(chat_id, 'Не хватает ресурсов для постройки огорода!')
        elif msg['text'] == '/create03':
            if data['wood'] >= 200 and data['stamina'] >= 2 and data['house'] != '\u2705':
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\U0001f3e0 Дом'],
                    ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                data['house'] = '\u2705'
                wood = int(data['wood']) - 200
                stamina = int(data['stamina']) - 2
                data['wood'] = wood
                data['stamina'] = stamina
                base.save_user(usr, uid, data)
                await bot.sendMessage(chat_id,
                                      'Ты построил дом. Теперь тебе открылось много функций и занятий в поселении. Ищи его в поселении.',
                                      reply_markup=markup)
            elif data['house'] == '\u2705':
                await bot.sendMessage(chat_id, 'У тебя уже есть дом. Зачем тебе второй?)')
            else:
                await bot.sendMessage(chat_id, 'Не хватает ресурсов для постройки дома!')
        elif msg['text'] == '/create11':
            if data['wood'] >= 100 and data['iron'] >= 150 and data['stamina'] >= 1 and data['terra'] != '\u2705':
                markup = ReplyKeyboardMarkup(keyboard=[
                    ['\u267b\ufe0f Терраформировочная машина'],
                    ['\u2b05\ufe0f Назад']], resize_keyboard=True)
                data['terra'] = '\u2705'
                wood = int(data['wood']) - 100
                iron = int(data['iron']) - 150
                stamina = int(data['stamina']) - 1
                data['wood'] = wood
                data['iron'] = iron
                data['stamina'] = stamina
                base.save_user(usr, uid, data)
                await bot.sendMessage(chat_id,
                                      'С `большим усилием`, сломав несколько деталей, ты всё-таки собрал эту хреновину. Немного подумав, ' +
                                      'ты пришёл к выводу, `что оно того не стоило`. Тем не менее, сейчас можно воспользоваться функционалом машины.',
                                      reply_markup=markup)
            elif data['house'] == '\u2705':
                await bot.sendMessage(chat_id,
                                      'У тебя уже есть этот агрегат, собирать второй раз эту штуковину ты не вынесешь.')
            else:
                await bot.sendMessage(chat_id, 'Не хватает ресурсов для постройки терраформировочной машины!')
        # =================== Команды
        elif msg['text'] == '/restart':
            base.delete(uid)
            markup = ReplyKeyboardMarkup(keyboard=[
                ['/start']], resize_keyboard=True)
            await bot.sendMessage(chat_id, 'Ты решил начать игру заново. Нажми start', reply_markup=markup)

        # =============================== Добавление чего-либо
        elif msg['text'] == '+exp':
            exp = base.get_user(uid).get('exp')
            exp += 10
            data['exp'] = exp
            print(data)
            base.save_user(usr, uid, data)
            await bot.sendMessage(chat_id, base.get_user(uid))
        elif msg['text'] == '+wood':
            wood = base.get_user(uid).get('wood')
            wood += 100
            data['wood'] = wood
            base.save_user(usr, uid, data)
            await bot.sendMessage(chat_id, base.get_user(uid))
        elif msg['text'] == '+iron':
            iron = base.get_user(uid).get('iron')
            iron += 100
            data['iron'] = iron
            base.save_user(usr, uid, data)
            await bot.sendMessage(chat_id, base.get_user(uid))
        elif msg['text'] == '+money':
            money = base.get_user(uid).get('money')
            money += 100
            data['money'] = money
            base.save_user(usr, uid, data)
            await bot.sendMessage(chat_id, base.get_user(uid))
        elif msg['text'] == '+crypt':
            crypt = base.get_user(uid).get('crypt')
            crypt += 100
            data['crypt'] = crypt
            base.save_user(usr, uid, data)
            await bot.sendMessage(chat_id, base.get_user(uid))
        elif msg['text'] == '+stamina':
            stamina = base.get_user(uid).get('stamina')
            stamina += 5
            data['stamina'] = stamina
            base.save_user(usr, uid, data)
            await bot.sendMessage(chat_id, base.get_user(uid))
        # =======(Функции в разработке, пока не трогать)=
        elif command == 'h':
            markup = ReplyKeyboardRemove()
            await bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)
        elif command == 'f':
            markup = ForceReply()
            await bot.sendMessage(chat_id, 'Хуле хочешь', reply_markup=markup)

        elif command == 'i':
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [dict(text='Telegram URL', url='https://core.telegram.org/')],
                [InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
                [dict(text='Callback - show alert', callback_data='alert')],
                [InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
                [dict(text='Switch to using bot inline', switch_inline_query='initial query')],
            ])

            message_with_inline_keyboard = await bot.sendMessage(chat_id, 'Inline keyboard with various buttons',
                                                                 reply_markup=markup)

        # Ещё одна хуетень, к которой надо прийти с временем


async def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    uid = from_id
    usr = uid
    data2 = base.get_user(uid)
    print('Callback query:', query_id, from_id, data)

    if data == 'notification':
        await bot.answerCallbackQuery(query_id, text='Notification at top of screen')
    elif data == 'alert':
        await bot.answerCallbackQuery(query_id, text='Alert1!', show_alert=True)

    # ============================Плазмоган==
    elif data == 'right':
        # global message_with_inline_keyboard
        # index
        shp = base.get_user(uid).get('shop')
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        ke = list(shp.keys())  # Список ключей словаря айтемов
        index = base.get_user(uid).get('index')

        if index < len(ke)-1:
            index = int(index) + 1
            print('index== ' + str(index))
            data2['index'] = index
            base.save_user(usr, uid, data2)
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Купить', callback_data='bought')],
                [InlineKeyboardButton(text='\u2b05\ufe0f', callback_data='left'),
                 InlineKeyboardButton(text='\u27a1\ufe0f', callback_data='right')]
            ])

            text = '\u2694\ufe0f *{}* [{}/{}]\n\n\U0001f9e8 Урон: {}\n\n\U0001f9ff Некое свойство: {}\n\nДоступно: ' \
                   '\U0001f4b5 {}\nСтоимость: \U0001f4b5 {}'.format(ke[index], index + 1, len(ke),
                                                                    shp.get(ke[index])[0],
                                                                    shp.get(ke[index])[1], base.get_user(uid).get(
                    'money'), shp.get(ke[index])[2])

            await bot.editMessageText(msg_idf, text, reply_markup=markup, parse_mode='Markdown')
        else:
            pass


    elif data == 'left':
        # global message_with_inline_keyboard
        index = base.get_user(uid).get('index')
        shp = base.get_user(uid).get('shop')
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        ke = list(shp.keys())  # Список ключей словаря айтемов

        if index <= 0:
            pass
        else:
            index = index - 1
            print(index)
            data2['index'] = index
            base.save_user(usr, uid, data2)
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Купить', callback_data='bought')],
                [InlineKeyboardButton(text='\u2b05\ufe0f', callback_data='left'),
                 InlineKeyboardButton(text='\u27a1\ufe0f', callback_data='right')]
            ])

            text = '\u2694\ufe0f *{}* [{}/{}]\n\n\U0001f9e8 Урон: {}\n\n\U0001f9ff Некое свойство: {}\n\nДоступно: ' \
                   '\U0001f4b5 {}\nСтоимость: \U0001f4b5 {}'.format(ke[index], index + 1, len(ke),
                                                                    shp.get(ke[index])[0],
                                                                    shp.get(ke[index])[1], base.get_user(uid).get(
                    'money'), shp.get(ke[index])[2])

            await bot.editMessageText(msg_idf, text, reply_markup=markup, parse_mode='Markdown')


    elif data == 'bought':
        #message_with_inline_keyboard
        index = base.get_user(uid).get('index')
        shp = base.get_user(uid).get('shop')
        money = base.get_user(uid).get('money')
        ke = list(shp.keys())  # Список ключей словаря айтемов
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        
        if money >= base.get_user(uid).get('shop').get('Плазмоган')[2]:
            await bot.answerCallbackQuery(query_id, text='Куплен *Плазмоган*')
            money -= base.get_user(uid).get('shop').get('Плазмоган')[2]
            data = base.get_user(uid)
            data['money'] = money
            # data['inv_size']+=1
            data['inv'] = {**data['inv'], **{'Плазмоган': base.get_user(uid).get('shop').get('Плазмоган')}}
            base.save_user(usr, uid, data)
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Купить', callback_data='bought1')],
                [InlineKeyboardButton(text='\u2b05\ufe0f', callback_data='n'),
                 InlineKeyboardButton(text='\u27a1\ufe0f', callback_data='right1')]
            ])
            await bot.editMessageText(msg_idf,
                                      '\u2694\ufe0f *Плазмоган* [1/3]\n\n\U0001f9e8 Урон: %s' % shp.get('Плазмоган')[
                                          0] +
                                      '\n\n\U0001f9ff Некое свойство: %s' % shp.get('Плазмоган')[
                                          1] + '\n\nДоступно: \U0001f4b5 %s' % base.get_user(uid).get('money') +
                                      '\nСтоимость: \U0001f4b5 %s' % shp.get('Плазмоган')[2], parse_mode='Markdown',
                                      reply_markup=markup)
        else:
            await bot.answerCallbackQuery(query_id, text='Не хватает \U0001f4b5 денег на покупку!')

    elif data == 'gun':
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        data = base.get_user(uid)
        for g in data['gun']:
            pass

        if data['gun'] != 'Плазмоган':
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='\u2705 Надеть', callback_data='wear1')],
                [InlineKeyboardButton(text='\U0001f4b5 Продать', callback_data='sell1')],
                [InlineKeyboardButton(text='Назад', callback_data='inv')]])
        else:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='\U0001f6ab Снять', callback_data='unwear1')],
                [InlineKeyboardButton(text='\U0001f4b5 Продать', callback_data='sell1')],
                [InlineKeyboardButton(text='Назад', callback_data='inv')]])
        await bot.editMessageReplyMarkup(msg_idf, reply_markup=markup)

    elif data == 'wear1':
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='inv')]])
        data = base.get_user(uid)
        data['gun'] = 'Плазмоган'
        data['damage'] += base.get_user(uid).get('shop').get('Плазмоган')[0]
        base.save_user(usr, uid, data)
        await bot.editMessageText(msg_idf,
                                  '\U0001f392 *Рюкзак* %s' % len(base.get_user(uid).get('inv')) + '/%s' % base.get_user(
                                      uid).get('inv_max_size') +
                                  '\n\n\U0001f468\U0001f3fb\u200d\U0001f3a4 %s' % msg["from"].get("username") +
                                  '\n\n\u25aa\ufe0f Шлем: [%s]' % base.get_user(uid).get('shlem') +
                                  '\n\u25aa\ufe0f Нагрудник: [%s]' % base.get_user(uid).get('chest') +
                                  '\n\u25aa\ufe0f Поножи: [%s]' % base.get_user(uid).get('ponozhi') +
                                  '\n\u25aa\ufe0f Сапоги: [%s]' % base.get_user(uid).get('boots') +
                                  '\n\n\u25aa\ufe0f Оружие: [%s]' % base.get_user(uid).get('gun') +
                                  '\n\n\u25aa\ufe0f Еда: [%s]' % base.get_user(uid).get('food'), parse_mode='Markdown',
                                  reply_markup=markup)
    elif data == 'unwear1':
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='inv')]])
        data = base.get_user(uid)
        data['gun'] = '[-]'
        data['damage'] -= base.get_user(uid).get('shop').get('Плазмоган')[0]
        base.save_user(usr, uid, data)
        await bot.editMessageText(msg_idf,
                                  '\U0001f392 *Рюкзак* %s' % len(base.get_user(uid).get('inv')) + '/%s' % base.get_user(
                                      uid).get('inv_max_size') +
                                  '\n\n\U0001f468\U0001f3fb\u200d\U0001f3a4 %s' % msg["from"].get("username") +
                                  '\n\n\u25aa\ufe0f Шлем: [%s]' % base.get_user(uid).get('shlem') +
                                  '\n\u25aa\ufe0f Нагрудник: [%s]' % base.get_user(uid).get('chest') +
                                  '\n\u25aa\ufe0f Поножи: [%s]' % base.get_user(uid).get('ponozhi') +
                                  '\n\u25aa\ufe0f Сапоги: [%s]' % base.get_user(uid).get('boots') +
                                  '\n\n\u25aa\ufe0f Оружие: [%s]' % base.get_user(uid).get('gun') +
                                  '\n\n\u25aa\ufe0f Еда: [%s]' % base.get_user(uid).get('food'), parse_mode='Markdown',
                                  reply_markup=markup)
    # ======================Гранатомед


    elif data == 'Гранатомед':
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        data = base.get_user(uid)
        if data['gun'] != 'Гранатомед':
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='\u2705 Надеть', callback_data='wear2')],
                [InlineKeyboardButton(text='\U0001f4b5 Продать', callback_data='sell2')],
                [InlineKeyboardButton(text='Назад', callback_data='inv')]])
        else:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='\U0001f6ab Снять', callback_data='unwear2')],
                [InlineKeyboardButton(text='\U0001f4b5 Продать', callback_data='sell2')],
                [InlineKeyboardButton(text='Назад', callback_data='inv')]])
        await bot.editMessageReplyMarkup(msg_idf, reply_markup=markup)

    elif data == 'wear2':
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='inv')]])
        data = base.get_user(uid)
        data['gun'] = 'Гранатомед'
        data['damage'] += base.get_user(uid).get('shop').get('Плазмоган')[0]
        base.save_user(usr, uid, data)
        await bot.editMessageText(msg_idf,
                                  '\U0001f392 *Рюкзак* %s' % len(base.get_user(uid).get('inv')) + '/%s' % base.get_user(
                                      uid).get('inv_max_size') +
                                  '\n\n\U0001f468\U0001f3fb\u200d\U0001f3a4 %s' % msg["from"].get("username") +
                                  '\n\n\u25aa\ufe0f Шлем: [%s]' % base.get_user(uid).get('shlem') +
                                  '\n\u25aa\ufe0f Нагрудник: [%s]' % base.get_user(uid).get('chest') +
                                  '\n\u25aa\ufe0f Поножи: [%s]' % base.get_user(uid).get('ponozhi') +
                                  '\n\u25aa\ufe0f Сапоги: [%s]' % base.get_user(uid).get('boots') +
                                  '\n\n\u25aa\ufe0f Оружие: [%s]' % base.get_user(uid).get('gun') +
                                  '\n\n\u25aa\ufe0f Еда: [%s]' % base.get_user(uid).get('food'), parse_mode='Markdown',
                                  reply_markup=markup)
    elif data == 'unwear2':
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='inv')]])
        data = base.get_user(uid)
        data['gun'] = '[-]'
        data['damage'] -= base.get_user(uid).get('shop').get('Гранатомед')[0]
        base.save_user(usr, uid, data)
        await bot.editMessageText(msg_idf,
                                  '\U0001f392 *Рюкзак* %s' % len(base.get_user(uid).get('inv')) + '/%s' % base.get_user(
                                      uid).get('inv_max_size') +
                                  '\n\n\U0001f468\U0001f3fb\u200d\U0001f3a4 %s' % msg["from"].get("username") +
                                  '\n\n\u25aa\ufe0f Шлем: [%s]' % base.get_user(uid).get('shlem') +
                                  '\n\u25aa\ufe0f Нагрудник: [%s]' % base.get_user(uid).get('chest') +
                                  '\n\u25aa\ufe0f Поножи: [%s]' % base.get_user(uid).get('ponozhi') +
                                  '\n\u25aa\ufe0f Сапоги: [%s]' % base.get_user(uid).get('boots') +
                                  '\n\n\u25aa\ufe0f Оружие: [%s]' % base.get_user(uid).get('gun') +
                                  '\n\n\u25aa\ufe0f Еда: [%s]' % base.get_user(uid).get('food'), parse_mode='Markdown',
                                  reply_markup=markup)


    # =============================inv
    elif data == 'inv':
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        keyboard = []
        data = base.get_user(uid)
        if len(list(base.get_user(uid).get('inv').keys())) >= 1:
            for i in base.get_user(uid).get('inv').keys():
                if data['gun'] == '%s' % i:
                    keyboard.append([InlineKeyboardButton(text='\u2705 ' + '%s' % i, callback_data='%s' % i)])
                else:
                    keyboard.append([InlineKeyboardButton(text='%s' % i, callback_data='%s' % i)])
        if len(keyboard) == 0:
            return
        else:
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await bot.editMessageReplyMarkup(msg_idf, reply_markup=markup)


    # ======================
    elif data == 'edit':

        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            await bot.editMessageText(msg_idf, 'NEW MESSAGE HERE!!!!!')
        else:
            await bot.answerCallbackQuery(query_id, text='No previous message to edit')


# ===============(Запускаторы игровых процессов)===
TOKEN = config.token

bot = telepot.aio.Bot(TOKEN)
answerer = telepot.aio.helper.Answerer(bot)

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, {'chat': on_chat_message,
                                   'callback_query': on_callback_query, }).run_forever())
print('Listening ...')
# ===================================================


loop.run_forever()
