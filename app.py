from flask import Flask,render_template
from httpx import request

app = Flask(__name__)

def fun_all(code):
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
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # code=input()

    driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
    driver.get("https://lordsmobile.igg.com/gifts/")
    c=0
    data=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vStREOt4nVOvqHzL7M5JyW3OEbqXU5eH2o521cHRGE_8fiuSQpyzPKJXTf5queEFX_hu6XcLZfBYkAr/pub?output=csv")
    for i in data["ID"]:
        # driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
        # driver.get("https://lordsmobile.igg.com/gifts/")
        element = driver.find_element(By.ID, "iggid")
        element.send_keys(i)
        element = driver.find_element(By.ID, "cdkey_1")
        element.send_keys(code)
        element = driver.find_element(By.ID, "btn_claim_1").click()
        try:
            element = driver.find_element(By.ID, "btn_confirm").click()
            c+=1
            print("Redeemption Successfull in ID :-",i)
        except:
            element = driver.find_element(By.ID, "btn_msg_close").click()
            print("Redeemption Failed in ID :-",i)
        # driver.close()
        driver.refresh()
        time.sleep(5)

    driver.close()
    return c


def fun(code):
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
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # code=input()

    driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
    driver.get("https://lordsmobile.igg.com/gifts/")
    c=0
    data=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTtW5iFJu3zb3TB07eptxo7JExb4xCMTGy-s4rnSzzrm2je0m_eQCZMTikCPQiluMrmWO77dMaPfJc8/pub?output=csv")
    for i in data["ID"]:
        # driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
        # driver.get("https://lordsmobile.igg.com/gifts/")
        element = driver.find_element(By.ID, "iggid")
        element.send_keys(i)
        element = driver.find_element(By.ID, "cdkey_1")
        element.send_keys(code)
        element = driver.find_element(By.ID, "btn_claim_1").click()
        try:
            element = driver.find_element(By.ID, "btn_confirm").click()
            c+=1
            print("Redeemption Successfull in ID :-",i)
        except:
            element = driver.find_element(By.ID, "btn_msg_close").click()
            print("Redeemption Failed in ID :-",i)
        # driver.close()
        driver.refresh()
        time.sleep(5)

    driver.close()
    return c

@app.route('/', methods=['POST','GET'])
def Home():
	return render_template("home.html")

@app.route('/redeem',methods=['POST','GET'])
def redeem():
    from flask import request
    if request.method == 'POST':
        print(request.form.get('code'))
        c=fun(request.form.get('code'))
        cn=fun_all(request.form.get('code'))
        return render_template("task.html",c=c+cn)
    else:
        return render_template("home.html")

if __name__ == '__main__':
	app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
