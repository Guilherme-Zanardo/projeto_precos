from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep

def download_precos_deral() -> None:
    path_chromedriver = "S:\\chromedriver.exe"
    chromedriver_path = Path(path_chromedriver)
    chrome_service = Service(executable_path=chromedriver_path, service_log_path='/dev/null')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    print('Baixando arquivo...')
    driver.get("https://www.agricultura.pr.gov.br/system/files/publico/Precos/pva.xls")
    sleep(10)
    driver.close()

    return print('\nDownaload concluído!\nAcesse em Donwloads')

download_precos_deral()