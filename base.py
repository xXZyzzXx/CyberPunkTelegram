import pickle
import os
import config

USERS_PATH = os.getcwd() + '/users/'

try:
    os.mkdir(USERS_PATH)
except:
    pass

data = {
    'nickname': config.nickname,
    'damage': config.damage,
    'money': config.money,
    'crypt': config.crypt,
    'stamina': config.stamina,
    'level': config.level,
    'exp': config.exp,
    'expto': config.expto,
    'maxstamina': config.maxstamina,
    'timestamina': config.timestamina,
    'animal': config.animal,
    'wood': config.wood,
    'iron': config.iron,
    'game': config.game,
    'workspace': config.workspace,
    'well': config.well,
    'garden': config.garden,
    'house': config.house,
    'status1': config.status1,
    'terra': config.terra,
    'inv': config.inv,
    'inv1': config.inv1,
    'inv_size': config.inv_size,
    'inv_max_size': config.inv_max_size,
    'shlem': config.shlem,
    'chest': config.chest,
    'ponozhi': config.ponozhi,
    'boots': config.boots,
    'gun': config.gun,
    'food': config.food,
    'shop': config.shop,
    'buildings': config.buildings,
    'crafts': config.crafts,
    'index': config.index}


def get_fname(uid):
    return USERS_PATH + '/{0}'.format(uid)


def save_user(usr, uid, data):
    if usr is None:
        print('Уже есть')
        return

    with open(get_fname(uid), 'wb') as outfile:
        pickle.dump(data, outfile)
        print('Создан файл')


def new_user(uid):
    usr = get_user(uid)
    if usr is None:
        usr = uid
        print(uid)
        print('Надо сохранить')
        save_user(usr, uid, data)

    else:
        print('Уже есть файл')


def get_user(uid):
    if os.path.exists(get_fname(uid)):
        with open(get_fname(uid), 'rb') as outfile:
            usr = pickle.load(outfile)
        return usr
    else:
        return None


def delete(uid):
    if os.path.exists(get_fname(uid)):
        os.remove(get_fname(uid))


# Обновить дату всех пользователей
def update_data(new_data):
    list1 = os.listdir(USERS_PATH)
    a = 0
    for i in os.listdir(USERS_PATH):
        data = get_user(list1[a])
        usr = str(list1[a])
        uid = str(list1[a])
        data.update(new_data)
        save_user(usr, uid, data)
        print(get_user(list1[a]))
        print('Перезаписан файл для: ', str(list1[a]))
        a += 1


# Обновить дату конкретного пользователя
def update_data_id(new_data, uid):
    data = get_user(uid)
    usr = uid
    data.update(new_data)
    save_user(usr, uid, data)
    print(get_user(uid))
    print('Перезаписан файл для: ', uid, ' Добавлен: ', new_data)
