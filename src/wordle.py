# Импорт необходимых библиотек
from wordfreq import zipf_frequency, top_n_list  # для проверки существования слов и получения популярных слов
import random                                     # для случайного выбора слова
from colorama import init, Fore, Back, Style      # для цветного отображения букв
from pymorphy3 import MorphAnalyzer               # для морфологической проверки слов

# Инициализация colorama, чтобы цвета сбрасывались после каждого print
init(autoreset=True)

# Инициализация морфологического анализатора для украинского языка
morph = MorphAnalyzer(lang='uk')

# ==============================
# Функции для цветного отображения букв
# ==============================
def green(msg):
    print(Back.GREEN + msg, end='')  # зелёный фон — буква на правильной позиции

def white(msg):
    print(Style.DIM + Back.WHITE + msg, end='')  # белый фон — буква отсутствует в слове

def red(msg):
    print(Back.YELLOW + msg, end='')  # жёлтый фон — буква есть в слове, но не на своём месте

# ==============================
# Заголовок игры
# ==============================
print("[W]", "[O]", "[R]", "[D]", "[L]", "[E]")

def is_good_word(w):
    parses = morph.parse(w)
    for p in parses:
        if (
            p.tag.POS == 'NOUN' and
            'Name' not in p.tag and
            'Surn' not in p.tag and
            'Patr' not in p.tag 
        ):
            return True
    return False

# ==============================
# Генерация случайного слова
# ==============================
word = ''  # переменная для загаданного слова

# Получаем список 50000 самых популярных слов украинского языка
words = top_n_list("uk", 50000)

# Выбираем случайное слово длиной 5 букв, которое является существительным
while len(word) != 5:
    w = random.choice(words)  
    if w.isalpha() and len(w) == 5 and is_good_word(w):
        word = morph.parse(w)[0].normal_form  # приводим к нормальной форме

# ==============================
# Функция проверки буквы игрока
# ==============================
def word_check(secret, guess):
    """
    secret - список букв загаданного слова
    guess - список букв введённого слова
    Возвращает список из 5 элементов:
    0 - буква отсутствует в слове
    1 - буква на правильной позиции (зелёная)
    2 - буква есть в слове, но не на своём месте (жёлтая)
    """
    result = [0] * 5
    secret_copy = secret.copy()

    # Сначала проверяем зелёные буквы
    for i in range(5):
        if guess[i] == secret[i]:
            result[i] = 1
            secret_copy[i] = None

    # Потом проверяем жёлтые буквы
    for i in range(5):
        if result[i] == 0 and guess[i] in secret_copy:
            result[i] = 2
            secret_copy[secret_copy.index(guess[i])] = None

    return result

# ==============================
# Проверка существования слова
# ==============================
def exists(word):
    return zipf_frequency(word, 'uk') > 0  # True, если слово реально существует

# ==============================
# Игровой цикл
# ==============================

## print(word)  # для теста, чтобы видеть загаданное слово


wordl = list(word)  # список букв загаданного слова
attempts = 6         # количество попыток

while attempts > 0:
    print("Введи слово: ")
    guess_word = input()  # ввод слова игроком

    correct_letters = 5  # счётчик зелёных букв

    if len(guess_word) < 5:
        print("Слово слишком короткое!")
    elif len(guess_word) > 5:
        print("Слово слишком длинное!")
    else:
        if exists(guess_word):
            guess_word = list(guess_word)
            result = word_check(wordl, guess_word)
            attempts -= 1

            # Отображение букв с цветами
            for i in range(5):
                if result[i] == 1:
                    green(guess_word[i])
                    correct_letters -= 1
                elif result[i] == 0:
                    white(guess_word[i])
                else:
                    red(guess_word[i])
            print()

            # Проверка победы
            if correct_letters == 0:
                print("Вітаю! Ви вгадали слово!")
                break
        else:
            print("Такого слова не існує.")

# Показываем загаданное слово после окончания игры
print("Загадане слово:", word)
