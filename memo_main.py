from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from memo_app import app
from memo_data import *
from memo_main_layout import *
from memo_card_layout import *
from memo_edit_layout import txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3

######################################              Константи:              #############################################
main_width, main_height = 1000, 450 # початкові розміри головного вікна
card_width, card_height = 600, 500 # початкові розміри віка "карточка"
time_unit = 1000    # стільки триває одна одиниця часу з тих, на які потрібно засипати 
                    # (у робочій версії програми збільшити у 60 разів!)

######################################          Глобальні змінні:      #############################################
questions_listmodel = QuestionListModel() # список питань
frm_edit = QuestionEdit(0, txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3) # запам'ятовуємо, що у формі редагування питання із чим пов'язано
radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4] # список віджетів, який потрібно перемішувати (для випадкового розміщення відповідей)
frm_card = 0 # тут буде пов'язуватись питання з формою тесту
timer = QTimer() # таймер для можливості "заснути" на час і прокинутися
win_card = QWidget() # вікно карточки
win_main = QWidget() # вікно редагування питань, основне у програмі

######################################             Тестові данні:         #############################################
def testlist():
    
    frm = Question('Яблуко', 'apple', 'application', 'pinapple', 'apply')
    questions_listmodel.form_list.append(frm)
    frm = Question('Дім', 'house', 'horse', 'hurry', 'hour')
    questions_listmodel.form_list.append(frm)
    frm = Question('Мишка', 'mouse', 'mouth', 'muse', 'museum')
    questions_listmodel.form_list.append(frm)
    frm = Question('Число', 'number', 'digit', 'amount', 'summary')
    questions_listmodel.form_list.append(frm)

######################################      Функції для проведення тестів:    #############################################

def set_card():
    ''' задає, як виглядає вікно картки'''
    win_card.resize(card_width, card_height)
    win_card.move(300, 300)
    win_card.setWindowTitle('Memory Card')
    win_card.setLayout(layout_card)

def sleep_card():
    ''' картка ховається на час, вказаний у таймері'''
    win_card.hide()
    timer.setInterval(time_unit * box_Minutes.value() )
    timer.start()

def show_card():
    ''' показывает окно (по таймеру), таймер останавливается'''
    win_card.show()
    timer.stop()

def show_random():
    ''' показати випадкове питання '''
    global frm_card # як би властивість вікна - поточна форма з даними картки
    # отримуємо випадкові дані, і випадково розподіляємо варіанти відповідей по радіокнопках:
    frm_card = random_AnswerCheck(questions_listmodel, lb_Question, radio_list, lb_Correct, lb_Result)
    # ми запускатимемо функцію, коли вікно вже є. Так що показуємо:
    frm_card.show() # завантажити потрібні дані у відповідні віджети 
    show_question() # показати на формі панель питань

def click_OK():
    ''' перевіряє питання чи завантажує нове питання '''
    if btn_OK.text() != 'Наступне питання':
        frm_card.check()
        show_result()
    else:
        # напис на кнопці дорівнює 'Наступний', от і створюємо наступне випадкове питання:
        show_random()

def back_to_menu():
    ''' повернення з тесту у вікно редактора '''
    win_card.hide()
    win_main.showNormal()

######################################     Функції для редагування питань:    ######################################
def set_main():
    ''' ставить, як виглядає основне вікно'''
    win_main.resize(main_width, main_height)
    win_main.move(100, 100)
    win_main.setWindowTitle('Список питань')
    win_main.setLayout(layout_main)
    
def edit_question(index):
    ''' завантажує у форму редагування питання та відповіді, що відповідають переданому рядку '''
    #  index - це об'єкт класу QModelIndex, див. потрібні методи нижче
    if index.isValid():
        i = index.row()
        frm = questions_listmodel.form_list[i]
        frm_edit.change(frm)
        frm_edit.show()

def add_form():
    ''' додає нове запитання та пропонує його змінити '''
    questions_listmodel.insertRows() # Нове питання з'явилося в даних та автоматично у списку на екрані
    last = questions_listmodel.rowCount(0) - 1   # Нове питання – останнє у списку. Знайдемо його позицію. 
                                                # У rowCount передаємо 0, щоб відповідати вимогам функції:
                                                # цей параметр все одно не використовується, але
                                                # потрібен за стандартом бібліотеки (метод із параметром index викликається при відтворенні списку)    
    index = questions_listmodel.index(last) # отримуємо об'єкт класу QModelIndex, який відповідає останньому елементу даних 
    list_questions.setCurrentIndex(index) # робимо відповідний рядок списку на поточному екрані
    edit_question(index)    # це питання треба підвантажити у форму редагування
                            # кліка мишкою у нас тут немає, викличемо потрібну функцію з програми
    txt_Question.setFocus(Qt.TabFocusReason) # Переводимо фокус на поле редагування питання, щоб відразу забиралися "болванки"
                                             # Qt.TabFocusReason переводить фокус так, якби була натиснута клавіша "tab"
                                             # це зручно тим, що виділяє "болванку", її легко відразу прибрати 

def del_form():
    ''' видаляє запитання та перемикає фокус '''
    questions_listmodel.removeRows(list_questions.currentIndex().row())
    edit_question(list_questions.currentIndex())

def start_test():
    ''' на початку тесту форма зв'язується з випадковим питанням і показується'''
    show_random()
    win_card.show()
    win_main.showMinimized()

######################################      Встановлення необхідних з'єднань:    #############################################
def connects():
    list_questions.setModel(questions_listmodel) # зв'язати список на екрані зі списком питань
    list_questions.clicked.connect(edit_question) # при натисканні на елемент списку відкриватиметься для редагування потрібне питання
    btn_add.clicked.connect(add_form) # з'єднали натискання кнопки "нове питання" з функцією додавання
    btn_delete.clicked.connect(del_form) # з'єднали натискання кнопки "видалити питання" з функцією видалення
    btn_start.clicked.connect(start_test) # натискання кнопки "почати тест" 
    btn_OK.clicked.connect(click_OK) # натискання кнопки "OK" на формі тесту
    btn_Menu.clicked.connect(back_to_menu) # натискання кнопки "Меню" для повернення з форми тесту до редактора питань
    timer.timeout.connect(show_card) # показуємо форму тесту після закінчення таймера
    btn_Sleep.clicked.connect(sleep_card) # натискання кнопки "спати" біля картки-тесту

######################################            Запуск програми:         #############################################
# Основний алгоритм іноді оформлюють у функцію, яка запускається, тільки якщо код виконується з цього файлу,
а не при підключенні як модуль. Дітям це зовсім не потрібне.
testlist()
set_card()
set_main()
connects()
win_main.show()
app.exec_()
