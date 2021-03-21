import telebot
import random
import csv
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types
random_word = {}
# подгружаем базу со словами
with open('words.csv', mode='r') as f:
    random_word = dict(filter(None, csv.reader(f, delimiter = ';')))
#random_word = {'please': 'пожалуйста', 'sorry': 'извините', 'hello': 'здравствуйте', 'goodbye': 'пока', 'hi': 'привет'}
# вставьте свой токен
bot = telebot.TeleBot('1680694647:')

HELP = '''
Это бот "Учи английский!".
Я говорю тебе слово,
а тебе нужно его перевод.
Если всё понятно жми: /word
Если хочешь игру наоборот пиши: /rword
/help запросить эту справку.
'''
# функция обрабатывает игру со словами наоборот
def rnextword(message):
    global RBotQuestion
    global markup
    # подгружаем из базы 4 случайных слова
    RandomList = random.sample(list(random_word.values()), 4)
    RBotQuestion = RandomList[0]
    RandomTextOne = RandomList[1]
    RandomTexTwo = RandomList[2]
    RandomTexThree = RandomList[3]
    # создаем подсказки
    RandomListHint = [list(random_word.keys())[list(random_word.values()).index(RBotQuestion)], list(random_word.keys())[list(random_word.values()).index(RandomTextOne)], list(random_word.keys())[list(random_word.values()).index(RandomTexTwo)], list(random_word.keys())[list(random_word.values()).index(RandomTexThree)]]
    RandomListSample = random.sample(RandomListHint, k=len(RandomListHint))
    textsend = ('Как переводится слово ' + RBotQuestion + ' ?')
    # Готовим кнопки
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(RandomListSample[0], RandomListSample[1], RandomListSample[2], RandomListSample[3]) #Имена кнопок
    msg = bot.send_message(message.chat.id, textsend, reply_markup=markup)
    bot.register_next_step_handler(msg, rwordanswer)
# функция обрабатывает игру со словами
def nextword(message):
    global BotQuestion
    global markup
    # подгружаем из базы 4 случайных слова
    RandomList = random.sample(list(random_word), 4)
    BotQuestion = RandomList[0]
    RandomTextOne = RandomList[1]
    RandomTexTwo = RandomList[2]
    RandomTexThree = RandomList[3]
    # создаем подсказки
    RandomListHint = [random_word[BotQuestion], random_word[RandomTextOne], random_word[RandomTexTwo], random_word[RandomTexThree]]
    RandomListSample = random.sample(RandomListHint, k=len(RandomListHint))
    textsend = ('Как переводится слово ' + BotQuestion + ' ?')
    # Готовим кнопки
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(RandomListSample[0], RandomListSample[1], RandomListSample[2], RandomListSample[3]) #Имена кнопок
    msg = bot.send_message(message.chat.id, textsend, reply_markup=markup)
    bot.register_next_step_handler(msg, wordanswer)
# команды бота
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я бот "Учи английский!".\n' +
        'Давай поиграем?! Тогда быстрее жми /word.\n' +
        'Если нужна помошь, тогда тебе сюда: /help.'
  )

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['word'])
def word(message):
    nextword(message)

def wordanswer(message):
    text = (message.text).lower()
    if text != random_word[BotQuestion]:
        msg = bot.send_message(message.chat.id, 'Вы не угадали, попробуйте ещё раз', reply_markup=markup)
        bot.register_next_step_handler(msg, wordanswer)
    else:
        bot.send_message(message.chat.id, 'Поздравляю, вы правы!')
        nextword(message)

@bot.message_handler(commands=['rword'])
def word(message):
    rnextword(message)

def rwordanswer(message):
    text = (message.text).lower()
    if text != list(random_word.keys())[list(random_word.values()).index(RBotQuestion)]:
        msg = bot.send_message(message.chat.id, 'Вы не угадали, попробуйте ещё раз', reply_markup=markup)
        bot.register_next_step_handler(msg, rwordanswer)
    else:
        bot.send_message(message.chat.id, 'Поздравляю, вы правы!')
        rnextword(message)
# зацикливаем
bot.polling(none_stop=True)
