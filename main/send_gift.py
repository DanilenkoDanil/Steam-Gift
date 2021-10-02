import time
import random
from . import generate_code
from . import get_friends
import chromedriver_autoinstaller

import undetected_chromedriver.v2 as uc

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from seleniumwire import webdriver
from selenium.webdriver.support.select import Select


def steam_login(driver, login: str, password: str):
    driver.get('http://steamcommunity.com/login/home/?goto=')
    time.sleep(2)
    login_input = driver.find_element_by_xpath('//*[@id="input_username"]')
    for i in login:
        login_input.send_keys(i)
        time.sleep(random.uniform(0, 0.2))
    password_input = driver.find_element_by_xpath('//*[@id="input_password"]')
    for i in password:
        password_input.send_keys(i)
        time.sleep(random.uniform(0, 0.2))
    driver.find_element_by_xpath('//*[@id="login_btn_signin"]/button/span').click()
    time.sleep(5)

    code_input = driver.find_element_by_xpath('//*[@id="twofactorcode_entry"]')
    if code_input.is_displayed() is False:
        return True

    code = generate_code.generate(login)

    for i in code:
        code_input.send_keys(i)
        time.sleep(random.uniform(0, 0.2))
    driver.find_element_by_xpath('//*[@id="login_twofactorauth_buttonset_entercode"]/div[1]').click()
    time.sleep(10)

    try:
        code_input = driver.find_element_by_xpath('//*[@id="twofactorcode_entry"]')
        code_input.clear()
        code = generate_code.generate(login)
        for i in code:
            code_input.send_keys(i)
            time.sleep(random.uniform(0, 0.2))
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="login_twofactorauth_buttonset_incorrectcode"]/div[1]/div[1]').click()

    except NoSuchElementException:
        pass

    return True


def add_friend(driver, link: str):
    driver.get(link)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="btn_add_friend"]/span').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div/span').click()


def gift_game(driver, game_link, friend_name):
    driver.get(game_link)
    time.sleep(3)
    try:
        select_element = driver.find_element_by_xpath('//*[@id="ageYear"]')
        time.sleep(0.5)
        Select(select_element).select_by_value('2002')
        driver.find_element_by_xpath('//*[@id="app_agegate"]/div[1]/div[3]/a[1]/span').click()
        time.sleep(1)
    except NoSuchElementException:
        pass
    # Добавить в корзину
    try:
        driver.find_element_by_xpath("//*[contains(@href,'addToCart')]").click()
    except NoSuchElementException:
        driver.find_element_by_xpath("//*[contains(@href,'addBundleToCart')]").click()

    time.sleep(1)
    # Купить в подарок
    driver.find_element_by_xpath('//*[@id="btn_purchase_gift"]/span').click()
    time.sleep(1)
    # Выбрать друга
    friends_table = driver.find_element_by_xpath('//*[@id="friends_chooser"]')
    friends = friends_table.find_elements_by_tag_name('div')
    for friend in friends:
        if friend.text == friend_name:
            friend.click()
    time.sleep(1)
    # Продолжить
    driver.find_element_by_xpath('//*[@id="gift_recipient_tab"]/div[3]/div/a/span').click()
    time.sleep(1)
    # Заполняем письмо
    driver.find_element_by_xpath('//*[@id="gift_recipient_name"]').send_keys('Your game')
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="gift_message_text"]').send_keys('....')
    time.sleep(0.3)
    driver.find_element_by_xpath('//*[@id="gift_signature"]').send_keys('BBB')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="submit_gift_note_btn"]/span').click()

    time.sleep(3)
    # Покупка
    driver.find_element_by_xpath('//*[@id="accept_ssa"]').click()
    driver.find_element_by_xpath('//*[@id="purchase_button_bottom_text"]').click()


# Интегрировать прокси!
def main(login, password, target_name, game_link):
    print('!!!!!!!!!!!!!!!!!!!!')
    chromedriver_autoinstaller.install()
    driver = uc.Chrome()

    steam_login(driver, login, password)
    time.sleep(3)

    gift_game(driver, game_link, target_name)

    driver.quit()


# Интегрировать прокси!
def main_friend_add(login: str, password: str, proxy: str, target_link: str):
    print('!!!!!!!!!!!!!!!!!!!!')
    chromedriver_autoinstaller.install()
    print(proxy)
    driver = uc.Chrome()

    steam_login(driver, login, password)
    time.sleep(3)

    add_friend(driver, target_link)

    driver.quit()

# main()
