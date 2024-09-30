import pygats.pygats as pyg
import pygats.recog as rec
from pygats.formatters import MarkdownFormatter as MD
import subprocess
import time

# Контекст, содержащий форматтер, который описывает правила
# форматирования строк при выводе на экран
ctx = pyg.Context(MD())

# Функция запуска тестируемого ПО
def setup(ctx):
    ctx.formatter.print_header(3, 'Подготовка стенда к работе')

    server = subprocess.Popen(['python3', '../app/app.py'])
    time.sleep(1)
    if server is None:
        pyg.failed(msg='Ошибка запуска сервера')

    browser = subprocess.Popen(['firefox', '--new-tab', 'http://localhost:5000'])
    time.sleep(1)
    if browser is None:
        pyg.failed(msg='Ошибка запуска firefox')
    print(browser.pid)

    pyg.passed(ctx)
    return server, browser

# Функция завершения работы тестируемого ПО
def teardown(ctx, server, browser):
    ctx.formatter.print_header(3, 'Завершение работы стенда')
    pyg.alt_with_key(ctx, 'F4')
    server.kill()
    browser.kill()
    pyg.passed(ctx)


def test_greeteng():
    # Сбрасывает счетчик шагов и печатает заголовок тест
    pyg.begin_test(ctx, 'Проверить работу первой страницы')

    # Находит слово "Иван" на экране и нажимает по нему левой кнопкой мыши
    rec.click_text(ctx, rec.SearchedText('Иван', 'rus', 'top-left'))

    # Печатает строку (Важно, чтобы был включен английский язык раскладки)
    pyg.typewrite(ctx, 'Тестировщик', 'rus')

    # Нажимаем на кнопку с надписью "Поздороваться"
    rec.click_text(ctx, rec.SearchedText('Поздороваться', 'rus', 'all'))

    # Проверяем, появилась ли на экране надпись "Привет, Тестировщик!"
    rec.check_text_on_screen(ctx, rec.SearchedText('Привет, Тестировщик!', 'rus', 'all'))


def test_go_to_admin_panel():
    pyg.begin_test(ctx, 'Проверить переход на вторую страницу')
    rec.click_text(ctx, rec.SearchedText('Перейти', 'rus', 'all'))

    rec.check_text_on_screen(ctx, rec.SearchedText('Форма', 'rus', 'all'))


def test_create_note():
    pyg.begin_test(ctx, 'Проверить возможность создания новой записи')
    
    rec.click_text(ctx, rec.SearchedText('Имя', 'rus', 'all'))
    pyg.typewrite(ctx, 'Иван', 'rus')

    rec.click_text(ctx, rec.SearchedText('Фамилия', 'rus', 'all'))
    pyg.typewrite(ctx, 'Иванов', 'rus')

    rec.click_text(ctx, rec.SearchedText('Пользователь', 'rus', 'all'))
    pyg.typewrite(ctx, 'Tester', 'eng')

    rec.click_text(ctx, rec.SearchedText('Почта', 'rus', 'all'))
    pyg.typewrite(ctx, 'email', 'eng')

    rec.click_text(ctx, rec.SearchedText('Адрес', 'rus', 'all'))
    pyg.typewrite(ctx, 'Саров', 'rus')

    rec.click_text(ctx, rec.SearchedText('Страна', 'rus', 'all'))

    # Нажимаем соответствую клавишу на клавиатуре
    pyg.press(ctx, 'down')
    pyg.press(ctx, 'enter')
    
    rec.click_text(ctx, rec.SearchedText('Область', 'rus', 'all'))
    pyg.press(ctx, 'down')
    pyg.press(ctx, 'enter')
    rec.click_text(ctx, rec.SearchedText('Создать', 'rus', 'all'))

    rec.check_text_on_screen(ctx, rec.SearchedText('Успешно', 'rus', 'all'))


test_suites = [
    test_greeteng,
    test_go_to_admin_panel,
    test_create_note
]


if __name__ == '__main__':
    server, browser = set_up(ctx)
    time.sleep(10)
    pyg.suite(ctx, 'ex_1', 'Тестовый пример, показывающий возможности pyGATs, используя инструменты распознавания объектов на экране')
    pyg.run(ctx, test_suites)
    teardown(ctx, server, browser)
