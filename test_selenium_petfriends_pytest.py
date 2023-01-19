# More info about pytest-selenium:
#    https://pytest-selenium.readthedocs.io/en/latest/user_guide.html
#
# How to run:
#  1) Download geko driver for Chrome here:
#     https://chromedriver.storage.googleapis.com/index.html?path=2.43/
#  2) Install all requirements:
#     pip install -r requirements.txt
#  3) Run tests:
#     pytest -s -v .\test_selenium_petfriends_pytest.py
#
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_logging_in_to_petfriends(browser):
    """ Search some phrase in google and make a screenshot of the page. """
    # Open PetFriends base page:
    browser.get("https://petfriends.skillfactory.ru/")

    # Find the field for search text input:
    btn_newuser = browser.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    btn_exist_acc = browser.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    field_email = browser.find_element(By.ID, "email")
    field_email.click()
    field_email.clear()
    field_email.send_keys("hulk4891@gmail.com")

    field_pass = browser.find_element(By.ID, "pass")
    field_pass.click()
    field_pass.clear()
    field_pass.send_keys("tatavova8486")

    btn_submit = browser.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    # Save cookies of the browser after the login
    with open('my_cookies.txt', 'wb') as cookies:
        pickle.dump(browser.get_cookies(), cookies)

    # Make the screenshot of browser window:
    browser.save_screenshot('result_petfriends.png')

def test_show_my_pets_page(browser):
    browser.get("http://petfriends.skillfactory.ru/login")
   # Вводим email
    browser.find_element(By.ID, 'email').send_keys('hulk4891@gmail.com')
   # Вводим пароль
    browser.find_element(By.ID,'pass').send_keys('tatavova8486')
   # Нажимаем на кнопку входа в аккаунт
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку Мои питомцы
    browser.find_element(By.CSS_SELECTOR, '.nav-item  [href="/my_pets"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
    assert browser.current_url == "https://petfriends.skillfactory.ru/my_pets"

def test_pets_have_name_age_type(browser):
    browser.get("http://petfriends.skillfactory.ru/login")
   # Вводим email
    browser.find_element(By.ID, 'email').send_keys('hulk4891@gmail.com')
   # Вводим пароль
    browser.find_element(By.ID,'pass').send_keys('tatavova8486')
   # Нажимаем на кнопку входа в аккаунт
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку Мои питомцы
    browser.find_element(By.CSS_SELECTOR, '.nav-item  [href="/my_pets"]').click()
    # нахоим все элементы с именами, породой и возрастом
    # images = browser.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')))
    names = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')
    descriptions = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(3)')
    age = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(4)')

    for i in range(len(names)):
        assert names[i].text != ""
        assert descriptions[i].text != ''
        assert age[i].text != ''

def test_number_of_pets_equal_to_one_that_is_stated(browser):
    browser.get("http://petfriends.skillfactory.ru/login")
   # Вводим email
    browser.find_element(By.ID, 'email').send_keys('hulk4891@gmail.com')
   # Вводим пароль
    browser.find_element(By.ID,'pass').send_keys('tatavova8486')
   # Нажимаем на кнопку входа в аккаунт
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку Мои питомцы
    browser.find_element(By.CSS_SELECTOR, '.nav-item  [href="/my_pets"]').click()
    # находим элемент со строкой о количестве питомцев и убираем ненужную информацию
    number = int(browser.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text.split(": ")[1].split("\n")[0])

    # нахоим всех питомцев с именами (чтоб ухнать сколько их всего)
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')))
    names = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')

    print(f"{number}")
    print(f"{len(names)}")
    assert number == len(names)

def test_atlist_half_of_pets_have_photo(browser):
    browser.get("http://petfriends.skillfactory.ru/login")
   # Вводим email
    browser.find_element(By.ID, 'email').send_keys('hulk4891@gmail.com')
   # Вводим пароль
    browser.find_element(By.ID,'pass').send_keys('tatavova8486')
   # Нажимаем на кнопку входа в аккаунт
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку Мои питомцы
    browser.find_element(By.CSS_SELECTOR, '.nav-item  [href="/my_pets"]').click()
    # находим элементы со фото
    images = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(1) img')
    number_of_photos = 0
    for i in range(len(images)):
        if (images[i].get_attribute('src') != ''):
            number_of_photos += 1

    # находим всех питомцев с именами (чтоб узнать сколько их всего)
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')))
    names = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')
    print(f"Кол-во питомцев с фото: {number_of_photos}")
    print(f"Общее кол-во питомцев: {len(names)}")
    number_of_pets = len(names)
    print(f"Процент питомцев с фото: {float(number_of_photos/number_of_pets)}")
    assert float(number_of_photos/number_of_pets) >= 0.5

def test_my_pets_dont_have_same_name_age_type(browser):
    browser.get("http://petfriends.skillfactory.ru/login")
    # Вводим email
    browser.find_element(By.ID, 'email').send_keys('hulk4891@gmail.com')
    # Вводим пароль
    browser.find_element(By.ID, 'pass').send_keys('tatavova8486')
    # Нажимаем на кнопку входа в аккаунт
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку Мои питомцы
    browser.find_element(By.CSS_SELECTOR, '.nav-item  [href="/my_pets"]').click()
    # нахоим все элементы с именами, породой и возрастом
    # images = browser.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')))
    names = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')
    descriptions = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(3)')
    age = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(4)')

    # cоздаем список питомцев состоящий из кортежей, каждый из которых хранит имя, возраст и породу питомца
    bd = []
    for i in range(len(names)):
        bd.append((names[i].text, descriptions[i].text, age[i].text))
        print(bd[i])
    # проверяем есть ли в списке одинаковые элементы
    all_elements_are_different = True
    for j in range (len(names)):
        checking_element = bd[j]
        for i in range(len(names)):
            if checking_element == bd[i] and i !=j:
                all_elements_are_different = False

    if (all_elements_are_different):
        print("все элементы разные")
    else:
        print("есть одинаковые элементы")

    assert all_elements_are_different == True

def test_my_pets_dont_have_same_name(browser):
    browser.get("http://petfriends.skillfactory.ru/login")
    # Вводим email
    browser.find_element(By.ID, 'email').send_keys('hulk4891@gmail.com')
    # Вводим пароль
    browser.find_element(By.ID, 'pass').send_keys('tatavova8486')
    # Нажимаем на кнопку входа в аккаунт
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку Мои питомцы
    browser.find_element(By.CSS_SELECTOR, '.nav-item  [href="/my_pets"]').click()
    # нахоим все элементы с именами, породой и возрастом
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')))
    names = browser.find_elements(By.CSS_SELECTOR, '.text-center tbody tr :nth-child(2)')

    # cоздаем список питомцев состоящий из кортежей, каждый из которых хранит имя, возраст и породу питомца
    bd = []
    for i in range(len(names)):
        bd.append((names[i].text))
        print(bd[i])
    # проверяем есть ли в списке одинаковые элементы
    all_elements_are_different = True
    for j in range (len(names)):
        checking_element = bd[j]
        for i in range(len(names)):
            if checking_element == bd[i] and i !=j:
                all_elements_are_different = False

    if (all_elements_are_different):
        print("все элементы разные")
    else:
        print("есть одинаковые элементы")

    assert all_elements_are_different == True