import time
import random
from . import generate_code
from . import get_friends
import chromedriver_autoinstaller

import undetected_chromedriver.v2 as uc
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from seleniumwire import webdriver
from selenium.webdriver.support.select import Select
from pyvirtualdisplay import Display


def steam_login(driver, login: str, password: str):
    driver.get('http://steamcommunity.com/login/home/?goto=')
    time.sleep(10)
    try:
        login_input = driver.find_element_by_xpath('//*[@id="input_username"]')
    except NoSuchElementException:
        time.sleep(15)
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
        time.sleep(2)
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

    time.sleep(5)
    # Купить в подарок
    driver.find_element_by_xpath('//*[@id="btn_purchase_gift"]/span').click()
    time.sleep(12)
    # Выбрать друга
    friends_table = driver.find_element_by_xpath('//*[@id="friends_chooser"]')
    friends = friends_table.find_elements_by_tag_name('div')
    for friend in friends:
        if friend.text == friend_name:
            friend.click()
    time.sleep(3)
    # Продолжить
    
    driver.find_element_by_xpath('//*[@id="gift_recipient_tab"]/div[3]/div/a/span').click()
    print("Breaaaaaaaaaaaaaaak")
    time.sleep(8)
    # Заполняем письмо
    driver.find_element_by_xpath('//*[@id="gift_recipient_name"]').send_keys('Your game')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="gift_message_text"]').send_keys('....')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="gift_signature"]').send_keys('BBB')
    time.sleep(3)
    print("Breaaaaaaaaaaaaaaak")
    driver.find_element_by_xpath('//*[@id="submit_gift_note_btn"]/span').click()

    time.sleep(8)
    # Покупка
    print("Breaaaaaaaaaaaaaaak")
    driver.find_element_by_xpath('//*[@id="accept_ssa"]').click()
    driver.find_element_by_xpath('//*[@id="purchase_button_bottom_text"]').click()

    
def check_gift_status(login: str, password: str, proxy: str, nickname: str, game_name: str):
    display = Display(size=(1920, 1080))
    display.start()

    print('!!!!!!!!!!!!!!!!!!!!')
    print(proxy)
    options = {
        'proxy': {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
            'no_proxy': 'localhost,127.0.0.1'  # excludes
        }
    }
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), seleniumwire_options=options)

    steam_login(driver, login, password)
    time.sleep(3)

    steam_id = driver.current_url.split('id/')[1]
    driver.get(f'https://steamcommunity.com/id/{steam_id}/inventory/')
    time.sleep(6)
    driver.find_element_by_xpath('//*[@id="inventory_more_link"]').click()
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="inventory_more_dropdown"]/div/a[3]').click()
    time.sleep(6)
    gifts = driver.find_element_by_xpath('//*[@id="tabcontent_pendinggifts"]').find_elements_by_tag_name('div')
    for i in gifts:
        try:
            status_area = i.find_element_by_class_name('gift_status_area')
        except NoSuchElementException:
            continue
        print(status_area.text)
        if nickname in status_area.find_element_by_tag_name('a').text and game_name in i.text:
            if 'Получен' in i.text:
                driver.quit()
                # display.stop()
                return 'Received'
            elif 'Отправлен' in i.text:
                driver.quit()
                # display.stop()
                return 'Submitted'
    driver.quit()
    display.stop()
    return 'Rejected'

def main(login, password, target_name, game_link, proxy):
    display = Display(size=(1920, 1080))
    display.start()
    print('!!!!!!!!!!!!!!!!!!!!')
    chromedriver_autoinstaller.install()
    options = {
        'proxy': {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
            'no_proxy': 'localhost,127.0.0.1'  # excludes
        }
    }
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), seleniumwire_options=options)

    steam_login(driver, login, password)
    time.sleep(3)

    gift_game(driver, game_link, target_name)

    driver.quit()
    display.stop()


def main_friend_add(login: str, password: str, proxy: str, target_link: str):
    display = Display(size=(1920, 1080))
    display.start()

    print('!!!!!!!!!!!!!!!!!!!!')
    chromedriver_autoinstaller.install()
    print(proxy)
    options = {
        'proxy': {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
            'no_proxy': 'localhost,127.0.0.1'  # excludes
        }
    }
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), seleniumwire_options=options)

    steam_login(driver, login, password)
    time.sleep(3)

    add_friend(driver, target_link)

    driver.quit()
    display.stop()

# main()
