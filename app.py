from flask import Flask, render_template
from httpx import request
from celery import Celery
import os

fapp = Flask(__name__)

fapp.config['CELERY_BROKER_URL'] = os.environ.get("cloudamqp")
celery = Celery(fapp.name, broker=fapp.config['CELERY_BROKER_URL'])
celery.conf.update(fapp.config)


@celery.task(bind=True)
def fun_all(self, code):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import pandas as pd
    import time

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # code=input()

    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), options=options)
    driver.get("https://lordsmobile.igg.com/gifts/")
    data = pd.read_csv(
        os.environ.get("data_all"))
    for i in data["ID"]:
        # driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
        # driver.get("https://lordsmobile.igg.com/gifts/")
        element = driver.find_element(By.ID, "iggid")
        element.send_keys(int(i))
        element = driver.find_element(By.ID, "cdkey_1")
        element.send_keys(code)
        element = driver.find_element(By.ID, "btn_claim_1").click()
        element = driver.find_element(By.ID, "btn_msg_close").click()
        print("Redeemption Attempt Completed in ID :-", i)
        # driver.close()
        driver.refresh()
        time.sleep(5)

    driver.close()
    # return c


@celery.task(bind=True)
def fun(self, code):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import pandas as pd
    import time

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # code=input()

    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), options=options)
    driver.get("https://lordsmobile.igg.com/gifts/")
    data = pd.read_csv(
        os.environ.get("data"))
    for i in data["ID"]:
        # driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
        # driver.get("https://lordsmobile.igg.com/gifts/")
        element = driver.find_element(By.ID, "iggid")
        element.send_keys(int(i))
        element = driver.find_element(By.ID, "cdkey_1")
        element.send_keys(code)
        element = driver.find_element(By.ID, "btn_claim_1").click()
        element = driver.find_element(By.ID, "btn_msg_close").click()
        print("Redeemption Attempt Completed in ID :-", i)
        # driver.close()
        driver.refresh()
        time.sleep(5)

    driver.close()
    # return c


@fapp.route('/', methods=['POST', 'GET'])
def Home():
    return render_template("home.html")


@fapp.route('/redeem', methods=['POST', 'GET'])
def redeem():
    from flask import request
    if request.method == 'POST':
        print("The Redeem Code :-", request.form.get('code'))
        fun.delay(request.form.get('code'))
        fun_all.delay(request.form.get('code'))
        return render_template("task.html")
    else:
        return render_template("home.html")


if __name__ == '__main__':
    fapp.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
