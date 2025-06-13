# =============================
# Part 1: Imports, Vars, consts
# =============================
from colorama import Fore
from os import system, name, getcwd
from os.path import isfile
from webbrowser import open_new as url
from time import sleep
from datetime import datetime as dt
from json import dump, load, loads, dumps
from shutil import copy, SameFileError
from pyrogram import Client, filters
from platform import system as sysname
from pyrogram.errors import RPCError, SessionPasswordNeeded
from pyrogram.types import User
from sqlite3 import DatabaseError
from pathlib import Path

Path("saves.jsonl").touch()
Path("saves.log").touch()

slctd = None
buffer = None
touch = None
error = None
code = None
bot_response = None
savefile = 'saves.jsonl'
logfile = 'saves.log'

art = Fore.BLUE + """/////////////////////////////////////////////////
//   ____    ______    _____                   //
//   \\ \\ \\  / /\\ \\ \\  / /  /    Wolfram        //
//    \\ \\ \\/ /  \\ \\ \\/ /  /     TeleTool       //
//     \\ \\/ /  / \\ \\/ /  /      Software       // 
//      \\ \\/  /   \\ \\/  /                      //
//       \\/__/     \\/__/        v 1.0.0        //
//                                             //
/////////////////////////////////////////////////
"""

comlist = """
1. Получить код             6. Выгрузить чат лист  
2. Создать сессию           7. Проверить сессию
3. Получить данные          8. Перейти по реф ссылке
4. Отправить сообщение      9. Выйти
5. Выгрузить сообщения      10. Крашнуть юзера             
0. Назад                    -1. Документация"""

comdict = ["Выдача кода", "Создание сессиии", "Выгрузка данных", "Отправка сообщения", "Выгрузка сообщений", "Выгрузка чат-листа", "Проверка сессии", "Переход по реф ссылке", "Выход", "Краш юзера"]

# =============================
# Part 2: Functions
# =============================

def log_out(sesname):
    with Client(name=sesname, workdir='clients', device_model="Wolfram TeleTool",
    system_version=sysname(),
    app_version="1.0.0",) as app:
        app.log_out()
        print('Вы вышли из аккаунта')
        sleep(3)
        main_menu()

def stick_boom(sesname, t, r):
    with Client(name=sesname, workdir='clients', device_model="Wolfram TeleTool",
    system_version=sysname(),
    app_version="1.0.0",) as app: 
        for i in range(int(r)):
            app.send_sticker(chat_id=t, sticker="CAACAgEAAxkBAAEBVQJoSXqMnPI1-sAMw6xeaJOw-plIzgACzQMAAp6GsEU05j9m55v7sTYE")
        print('Успешно отправлено!')
        sleep(3)
        main_menu()

def ref_send(sesname, link):
    bot = link.split('/')[-1].split('?start=')[0]
    try: start = '/start '+link.split('/')[-1].split('?start=')[1]
    except Exception:
        print('Неккоректная реферальная ссылка!')
        sleep(2)
        main_menu()
    with Client(name=sesname, workdir='clients', device_model="Wolfram TeleTool",
        system_version=sysname(),
        app_version="1.0.0",) as app:
            app.send_message(bot, start)
            print('Выполнено')
            main_menu()

def ses_check(sesname):
    try:
        with Client(name=sesname, workdir='clients', device_model="Wolfram TeleTool",
        system_version=sysname(),
        app_version="1.0.0",) as app: pass
        input('Сессия жива! нажмите Enter, чтоб продолжить\n>$*')
    except DatabaseError:
        input('Сессия бита, нажмите Enter, чтоб продолжить\n>$*')

def get_frs(sesname, sv):
    with Client(name=sesname, workdir='clients', device_model="Wolfram TeleTool",
        system_version=sysname(),
        app_version="1.0.0",) as app:
            if sv:
                for i in app.get_dialogs():
                    with open(logfile, 'a', encoding='utf-8') as f:
                        chat = i.chat
                        f.write(f'[{dt.now()}, {sesname}] {chat.id}, {chat.title or chat.first_name} - {chat.type}')
                print(f"Сохранено в файл {getcwd}/saves.log")
            else:
                for i in app.get_dialogs():
                    chat = i.chat
                    print(f'[{dt.now()}, {sesname}] {chat.id}, {chat.title or chat.first_name} - {chat.type}')
                input('Нажмите Enter чтоб вернутся в главное меню\n >$*  ')
            main_menu()   

def get_chat(sesname, lim, chat, sv):
    with Client(name=sesname, workdir='clients', device_model="Wolfram TeleTool",
        system_version=sysname(),
        app_version="1.0.0",) as app:
            if sv:
                for i in app.get_chat_history(chat_id=int(chat), limit=int(lim)):
                    with open(logfile, 'a', encoding='utf-8') as f:
                        f.write(f'[{dt.now()}, {sesname}] {i}')
                print(f"Сохранено в файл {getcwd}/saves.log")
            else:
                for i in app.get_chat_history(chat_id=int(chat), limit=int(lim)):
                    print(f'[{dt.now()}, {sesname}] {i}')
                input('Нажмите Enter чтоб вернутся в главное меню\n >$*  ')
            main_menu()

def send_msg(sesname, s, t):
    with Client(name=sesname, workdir='clients', device_model="Wolfram TeleTool",
        system_version=sysname(),
        app_version="1.0.0",) as app:
            app.send_message(s, t)
            print(f'сообщение с текстом {t} отправлено успешно {s}')
            main_menu()

def get_ids(sesname):
    with Client(name=sesname, workdir='clients', device_model="Wolfram TeleTool",
            system_version=sysname(),
            app_version="1.0.0",) as app:
        me = app.get_me()
        print(art, f'Выбрано: {slctd}\n',  Fore.CYAN, f'1. Номер телефона {me.phone_number}\n  2. Айди аккаунта {me.id}\n  3. Имя/Фамилия: {me.first_name}, {me.last_name}\n  4. Юзернейм: {me.username}\n  5. Наличие премиума: {me.is_premium}\n  6. Биография: {app.get_chat("me").bio}')
        input("Нажмите Enter, чтобы продолжить. \n>$*")

def code_wait(sesname):
    try:
        app = Client(workdir="clients", name=sesname, device_model="Wolfram TeleTool",
            system_version=sysname(),
            app_version="1.0.0",)

        @app.on_message(filters.chat(777000))
        def handler(client, message):
            try:
                code = message.text.split()[2] if message.text.split()[5] == "given" else message.text.split()[5]
                print(f'Ваш код: {code}')
                sleep(3)
                main_menu()
            except Exception:
                print(f'Ответ от 777000:\n{message.text}')
            client.stop()
        print('Ожидаю код подтверждения от Telegram...')
        app.run()  
    except DatabaseError:
        print('Файл сессии поврежден или побит.')
        sleep(1)
        main_menu()
    except Exception as e:
        print(f"Ошибка при ожидании кода: {type(e).__name__}: {e}")
        sleep(2)
        main_menu()
    finally:
        print('Успешно')
        sleep(1)
        main_menu()

def new_session(nameses, inpphone):
    global slctd, touch, buffer
    with open(savefile, 'r', encoding='utf-8') as file:
        for i in file:
            buffer = loads(i)
            if buffer["type"] == "tg_params":
                break
            else:
                print('У вас еще не заготовлены данные')
                sleep(1)
                main_menu()
    if nameses == "0":
        main_menu()
        return None
    else:
        app = Client(
            name=nameses,
            api_id=buffer["api_id"],
            api_hash=buffer["api_hash"],
            workdir="clients",
            device_model="Wolfram TeleTool",
            system_version=sysname(),
            app_version="1.0.0",
            lang_code="ru"
        )
        try:
            app.connect()
            phone = "+"+inpphone if inpphone.__contains__('+') else inpphone
            sent_code = app.send_code(phone)
            code = str(input("Введите код: \n>$> "))
            try:
                signed_in = app.sign_in(phone, sent_code.phone_code_hash, code)
                if isinstance(signed_in, User):
                    return signed_in
            except SessionPasswordNeeded:
                app.check_password(input('Введите пароль 2FA: \n>$> '))
            signed_up = app.sign_up(phone, sent_code.phone_code_hash, name)
            return signed_up
        except RPCError as e:
            pass
        finally:
            app.send_message("me", "WolframTeleTool working")
            app.disconnect()
            print(f'Успешно! Сессия создана по пути {getcwd()}/clients/{nameses}')
            sleep(3)
            main_menu()

def is_file_path(path: str) -> bool:
    return isfile(path)

def interprete(cmd):
    try:
        with open(savefile, 'r', encoding='utf-8') as f:
            for i in f:
                a = loads(i)
                if a["type"] == "fcparam" and a["name"] == cmd:
                    if a["fstcmd"] == 1:
                        if a["params"].get("inpphoe") is None:
                            a["params"]["inpphoe"] = input('Укажите параметр inpphoe\n>$> ')                    
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите параметр sesname\n>$> ')
                        code_wait(a["params"]["sesname"])
                        return True
                    elif a["fstcmd"] == 2:
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        if a["params"].get("inpphoe") is None:
                            a["params"]["inpphoe"] = input('Укажите номер телефона\n>$> ')
                        new_session(a["params"]["sesname"], a["params"]["inpphoe"])
                        return True
                    elif a["fstcmd"] == 3:
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        get_ids(a["params"]["sesname"])
                        return True
                    elif a["fstcmd"] == 4:
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        if a["params"].get("s") is None:
                            a["params"]["s"] = input('Укажите получателя\n>$> ')
                        if a["params"].get("t") is None:
                            a["params"]["t"] = input('Укажите текст\n>$> ')
                        send_msg(a["params"]["sesname"], a["params"]["s"], a["params"]["t"])
                        return True
                    elif a["fstcmd"] == 5:
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        if a["params"].get("lim") is None:
                            a["params"]["lim"] = input('Укажите лимит\n>$> ')
                        if a["params"].get("chat") is None:
                            a["params"]["chat"] = input('Укажите чат\n>$> ')
                        if a["params"].get("sv") is None:
                            a["params"]["sv"] = input('Сохранять в файл? (True/False)\n>$> ')
                        get_chat(a["params"]["sesname"], a["params"]["lim"], a["params"]["chat"], eval(a["params"]["sv"]))
                        return True
                    elif a["fstcmd"] == 6:
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        if a["params"].get("sv") is None:
                            a["params"]["sv"] = input('Сохранять в файл? (True/False)\n>$> ')
                        get_frs(a["params"]["sesname"], eval(a["params"]["sv"]))
                        return True
                    elif a["fstcmd"] == 7: 
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        ses_check(a["params"]["sesname"])
                        return True
                    elif a["fstcmd"] == 8:
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        if a["params"].get("link") is None:
                            a["params"]["link"] = input('Укажите реф-ссылку\n>$> ')
                        ref_send(a["params"]["sesname"], a["params"]["link"])
                        return True
                    elif a["fstcmd"] == 9:
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        log_out(a["params"]["sesname"])
                        return True
                    elif a["fstcmd"] == 10:
                        if a["params"].get("sesname") is None:
                            a["params"]["sesname"] = input('Укажите имя сессии\n>$> ')
                        if a["params"].get("s") is None:
                            a["params"]["s"] = input('Укажите пользователя\n>$> ')
                        if a["params"].get("r") is None:
                            a["params"]["r"] = input('Укажите количество повторений\n>$> ')
                        stick_boom(a["params"]["sesname"], a["params"]["s"], a["params"]["r"])
                        return True
                    else:
                        return False
            else:
                return
    except Exception as e:
        raise e

def analyzer(cmd):
    global slctd
    if is_file_path(cmd):
        slctd = cmd.split('/')[-1]
        return True
    try:
        l = interprete(cmd)
        if l == False: pass
        elif l == True: 
            print('комманда выполнена!')
            return True
    except Exception as e:
        print(f'ошибка интерпритатора {e}')
        return False
    
# =============================
# Part 3: Menu
# =============================

def main_menu():
    global slctd, touch
    system('cls' if name == 'nt' else 'clear')
    print(art, f'Выбрано: {slctd}\n', Fore.CYAN, '\n 1. Операции \n 2. Указать цель \n 3. Об авторе \n 4. Указать данные \n 5. быстрые комманды \n 6. Выйти')
    touch = str(input('>>> '))
    if touch == "2":
        system('cls' if name == 'nt' else 'clear')
        print(art, f'Выбрано: {slctd}\n', Fore.CYAN, '\n Укажите путь, по которому будут производится операции: \n 0. Назад ')
        touch = str(input('>>> '))
        if touch == "0": main_menu()
        else: slctd = touch.split('/')[-1]
        try:
            copy(touch, f"clients/{touch.split('/')[-1]}")
        except SameFileError:
            pass
        except FileNotFoundError:
            print("Неправильный путь!")
            sleep(2)
            main_menu()
        main_menu()
    elif touch == "1":
        system('cls' if name == 'nt' else 'clear')
        print(art, f'Выбрано: {slctd}\n', Fore.CYAN, '\n ', comlist)
        touch = str(input('>>> '))
        if touch == "1":
            if not slctd:
                print("Сначала укажите путь во вкладке 2.")
                sleep(1.5)
                return main_menu()
            print(art, f'Выбрано: {slctd}\n', Fore.CYAN) 
            with open(savefile, 'r') as f:
                for i in f:
                    f0 = loads(i)
                    if f0["type"] == "tg_params":
                        break
                try:
                    code_wait(sesname=slctd.split('.')[0])
                except AttributeError as e:
                    print(f'Ошибка, цель не укзана! Debug: {e}')
                    sleep(1)
                    main_menu()
        elif touch == "2":
            system('cls' if name == 'nt' else 'clear')
            print(art, f'Выбрано: {slctd}\n', Fore.CYAN, '\nУкажите имя сессии: \n 0. Назад')   
            new_session(nameses=str(input(">$> ")), inpphone = str(input("Укажите номер: \n>$> ")))
        elif touch == "3":
            try:
                get_ids(slctd.split('.')[0])
            except AttributeError as e:
                print(f'Ошибка, цель не укзана! Debug: {e}')
                sleep(1)
                main_menu()     
        elif touch == "4":
            try:
                send_msg(slctd.split('.')[0], input("Введите контакт получателя:\n>$> "), input("Введите текст сообщения:\n>$> "))
            except AttributeError as e:
                print(f'Ошибка, цель не укaзана! Debug: {e}')
                sleep(1)
                main_menu()   
        elif touch == "5":
            try:
                get_chat(sesname=slctd.split('.')[0], chat=input("Введите чат для выгрузки:\n>$> "), lim=input("Сколько сообщений нужно выгрузить?:\n>$> "), sv=True if str(input("Сохранить в файл или вывести в консоль?:\n 1. Консоль\n 2. Файл\n >$> ")) == "2" else False)
            except AttributeError as e:
                print(f'Ошибка, цель не укaзана! Debug: {e}')
                sleep(1)
                main_menu()
        elif touch == "6":
            try:
                get_frs(sesname=slctd.split('.')[0], sv=True if str(input("Сохранить в файл или вывести в консоль?:\n 1. Консоль\n 2. Файл\n >$> ")) == "2" else False)
            except AttributeError as e:
                print(f'Ошибка, цель не укaзана! Debug: {e}')
                sleep(1)
                main_menu()
        elif touch == "7":
            try:
                ses_check(sesname=slctd.split('.')[0])
            except AttributeError as e:
                print(f'Ошибка, цель не укaзана! Debug: {e}')
                sleep(1)
                main_menu()
        elif touch == "8":
            try:
                ref_send(sesname=slctd.split('.')[0], link=input('Введите реферальную ссылку:\n>$> '))
            except AttributeError as e:
                print(f'Ошибка, цель не укaзана! Debug: {e}')
                sleep(1)
                main_menu()
        elif touch == "9":
            try:
                log_out(sesname=slctd.split('.')[0])
            except AttributeError as e:
                print(f'Ошибка, цель не укaзана! Debug: {e}')
                sleep(1)
                main_menu()            
        elif touch == "10": 
            try:
                stick_boom(sesname=slctd.split('.')[0], t=input('Введите получателя:\n>$> '), r=input('Введите колво стикеров:\n>$> '))
            except AttributeError as e:
                print(f'Ошибка, цель не укaзана! Debug: {e}')
                sleep(1)
                main_menu()
        elif touch == "0": 
            pass
            main_menu()
        # elif touch == "-1":
        else: 
            print("Неккоректный ввод!")
            sleep(1)
            main_menu()
    elif touch == "3":
        system('cls' if name == 'nt' else 'clear')
        print(art, f'Выбрано: {slctd}\n', Fore.CYAN, '\n Привет-привет! \n 1. GitHub \n 2. Сайт (Временно не активен) \n 3. Telegram \n 4. Назад')
        touch = str(input('>>> '))
        if touch == "1": url('https://github.com/mp2128'), sleep(1), main_menu()
        elif touch == "2": sleep(1), main_menu()
        elif touch == "3": url('t.me/mainfrik'), sleep(1), main_menu()
        elif touch == "4": main_menu()
        else: print('Неверный ввод!'), sleep(1), main_menu()
    elif touch == "4":
        try:
            with open(savefile, "r", encoding="utf-8") as f:
                data = load(f)
        except:
            data = {"type": "tg_params", "api_id": None, "api_hash": None, "proxy": None, "ipv6": None}

        if data["type"] == "tg_params":
            system('cls' if name == 'nt' else 'clear')
            print(art, f'Выбрано: {slctd}\n', Fore.CYAN,
                f'ApiID - {data["api_id"]}\nApiHASH - {data["api_hash"]} \nProxy - SOON\n0. Назад\n1. Изменить')
            touch = input('>>> ')
            if touch == "0":
                return main_menu()
            elif touch == "1":
                system('cls' if name == 'nt' else 'clear')
                print(art, f'Выбрано: {slctd}\n', Fore.CYAN, 'Укажите ApiID')
                data["api_id"] = input('>$> ')
                system('cls' if name == 'nt' else 'clear')
                print(art, f'Выбрано: {slctd}\n', Fore.CYAN, 'Укажите ApiHASH')
                data["api_hash"] = input('>$> ')
                with open(savefile, "w", encoding="utf-8") as f:
                    dump(data, f, ensure_ascii=False)
                print("Данные сохранены.")
                sleep(1)
                return main_menu()
    elif touch == "5": 
        system('cls' if name == 'nt' else 'clear')
        print(art, f'Выбрано: {slctd}\n', Fore.CYAN, '\n 0. Выйти \n 1. Список комманд \n 2. Добавить комманду')   
        touch = str(input('>>> '))
        if touch == "0": 
            main_menu()
        if touch == "1":
            with open(savefile, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            fclist = []
            for line in lines:
                buffer = loads(line)
                if buffer["type"] == "fclist":
                    fclist = buffer["fclist"]
                    break
            for j, v in enumerate(fclist):
                for line in lines:
                    buffer2 = loads(line)
                    if buffer2["type"] == "fcparam" and buffer2["name"] == v:
                        print(f'{j + 1}. {v} - {comdict[buffer2["fstcmd"] - 1]}')
                        break
            input("Нажмите Enter для продолжения\n >$> ")
            main_menu()
        if touch == "2": 
            buffer = {"type": "fcparam", "name": None, "fstcmd": None, "params": {"sesname": None}, "api": [None, None]}
            while True:
                bufname = str(input('Введите имя комманды\n >$> '))
                valid = True

                with open(savefile, 'r', encoding='utf-8') as f:
                    for i in f:
                        a = loads(i)
                        try:
                            if "fstcmd" not in a: 
                                continue
                            if comdict[int(a["fstcmd"])] == send_msg:
                                print('Комманда занята. попробуйте назвать по-другому')
                                valid = False
                                break
                        except Exception:
                            continue
                if valid:
                    buffer["name"] = bufname
                    break 
        system('cls' if name == 'nt' else 'clear')
        print(art, f'Выбрано: {slctd}\n', Fore.CYAN, '\n Выберите функцию для быстрой комманды')
        for j, v in enumerate(comdict, 1):
            print(f"{j}. {v}")
        while True:
            try:
                buffer["fstcmd"] = int(input('>$> '))
                if buffer["fstcmd"] > 10 or buffer["fstcmd"] < 1:
                    raise TypeError
            except Exception as e:
                print(f'Неккоректный ввод! {e}')
                sleep(1)
                continue
            else:
                break
        print('Укажите следующие параметры для комманды')
        if buffer["fstcmd"] == 2: 
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
            buffer["params"]["inpphoe"] = input('Введите номер телефона или None если спрашивать\n>$> ')
        elif buffer["fstcmd"] == 1:
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
        elif buffer["fstcmd"] == 3:
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
        elif buffer["fstcmd"] == 4:
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
            buffer["params"]["s"] = input('Введите получателя или None если спрашивать\n>$> ')
            buffer["params"]["t"] = input('Введите текст или None если спрашивать\n>$> ')   
        elif buffer["fstcmd"] == 5:
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
            buffer["params"]["lim"] = input('Введите лимит или None если спрашивать\n>$> ')
            buffer["params"]["chat"] = input('Введите чат или None если спрашивать\n>$> ') 
            buffer["params"]["sv"] = input('Введите True если сохранять в файл или False если принтить в консоль или None если спрашивать\n>$> ')   
        elif buffer["fstcmd"] == 6:
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
            buffer["params"]["sv"] = input('Введите True если сохранять в файл или False если принтить в консоль или None если спрашивать\n>$> ') 
        elif buffer["fstcmd"] == 7:            
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
        elif buffer["fstcmd"] == 8:
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
            buffer["params"]["link"] = input('Введите ссылку или None если спрашивать\n>$> ') 
        elif buffer["fstcmd"] == 9:
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
        elif buffer["fstcmd"] == 10:
            buffer["params"]["sesname"] = input('Введите имя сессии или None если спрашивать\n>$> ')
            buffer["params"]["s"] = input('Введите получателя или None если спрашивать\n>$> ')
            buffer["params"]["r"] = input('Введите количество или None если спрашивать\n>$> ')          
        else: raise Exception("Непредвидимая ошибка!")
        with open(savefile, 'a', encoding='utf-8') as f:
            f.write("\n")
            f.write(dumps(buffer))
        lines = []
        with open(savefile, 'r', encoding='utf-8') as f:
            for i in f:
                if not i.strip():
                    continue
                a = loads(i)
                if a["type"] == "fclist":
                    if buffer["name"] not in a["fclist"]:
                        a["fclist"].append(buffer["name"])
                lines.append(dumps(a))
        with open(savefile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        input('Задача успешно создана. теперь вы ее можете призвать с главного меню! Нажмите Enter, чтоб продолжить.\n>$* ')
        main_menu()
        return
    elif touch == "6": exit()
    else: 
        buffer = analyzer(touch)
        if buffer: 
            main_menu()
        else:
            print('Неверный ввод!')
            sleep(1)
            main_menu()

# =============================
# Part X: Launch
# =============================
if __name__ == "__main__":
    while True:
        try:
            main_menu()
        except Exception as e:    
            error = e
            break
    if error:  
        print(f'Произошла ошибка: {error}. Нажмите Enter для перемещения на github создателя.')
        input('>$*')
        url('https://github.com/mp2128')



