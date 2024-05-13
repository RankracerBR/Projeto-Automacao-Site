from flask import Flask, render_template
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import requests
from datetime import datetime

app = Flask(__name__)

chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-dev-shm-usage')

# Função para enviar o webhook
def enviar_webhook(mensagem):
    url = ""
    payload = {"mensagem": mensagem}
    response = requests.post(url, json=payload)
    print("Enviando webhook para:", url)
    print("Payload:", payload)
    print("Resposta:", response.text)

@app.route('/')
def carregar_html():
    return render_template('form.html')

@app.route('/agendar/<nome>/<data>/<hora>/<horafinal>')
def agendar_compromisso(nome, data, hora, horafinal):
    # Substitui as barras por hífens na data
    data_datetime = datetime.strptime(data, '%Y-%m-%d')  # Correto: formato %Y-%m-%d
    data_formatada = data_datetime.strftime('%d/%m/%Y')  # Correto: formato %d/%m/%Y

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=chrome_options))

    try:
        # Acessa o site
        driver.get("")

        # Simula um clique no campo de e-mail e preenche com o e-mail
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(( ""))
        )
        email_field.click()
        email_field.send_keys("")

        # Simula um clique no campo de senha antes de preenchê-lo
        senha_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(( ""))
        )
        senha_field.click()

        # Preenche o campo de senha com a senha
        senha_field.send_keys("")

        # Clica no botão de login
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(( ""))
        )
        login_button.click()

        print("Login realizado com sucesso!")

        # Aguarda a presença do botão "AGENDAR +"
        agendar_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(( ''))
        )

        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView();", agendar_button)

        # Clica no botão "AGENDAR +"
        agendar_button.click()

        print("Clique no botão 'AGENDAR +' realizado com sucesso!")

        # Aguarda mais 5 segundos após clicar em "AGENDAR +"
        time.sleep(2)

        # Clica no botão "COMPROMISSO PARTICIPAR"
        compromisso_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(( ''))
        )
        compromisso_button.click()

        print("Clique no botão 'COMPROMISSO PARTICIPAR' realizado com sucesso!")

        # Aguarda 20 segundos após clicar em "COMPROMISSO PARTICIPAR"
        WebDriverWait(driver, 2).until(EC.presence_of_element_located(( '"]')))

        # Localiza o campo "COMPROMISSO PARTICIPAR" e preenche com "EVENTO TESTE"
        compromisso_textarea = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(( '"]'))
        )
        compromisso_textarea.clear()
        compromisso_textarea.send_keys(nome)

        print("Campo 'COMPROMISSO PARTICIPAR' preenchido com 'EVENTO TESTE'")

        # Simula o pressionamento da tecla TAB no teclado após preencher "COMPROMISSO PARTICIPAR"
        compromisso_textarea.send_keys(Keys.TAB)

        print("Pressionamento da tecla TAB realizado após 'COMPROMISSO PARTICIPAR'")

        # Aguarda 2 segundos antes de preencher o campo de data
        time.sleep(1)

        # Localiza o campo de data pelo placeholder
        data_input = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable(( ''))
        )

        # Cola a data recebida no campo de data
        data_input.send_keys(data_formatada)

        # Simula o pressionamento da tecla TAB no teclado para ir para o próximo campo (Hora de Início)
        data_input.send_keys(Keys.TAB)

        print("Campo de data preenchido com '{}'".format(data_formatada))

        # Aguarda 2 segundos antes de preencher o campo de hora de início
        time.sleep(1)

        # Localiza o campo de hora de início e limpa o conteúdo
        hora_inicio_input = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable(( ''))
        )
        hora_inicio_input.send_keys(Keys.CONTROL + 'a')  # Seleciona todo o conteúdo
        hora_inicio_input.send_keys(Keys.DELETE)         # Apaga o conteúdo

        # Preenche o campo de hora de início com a hora recebida
        hora_inicio_input.send_keys(hora)

        # Simula o pressionamento da tecla TAB no teclado para ir para o próximo campo (Hora de Término)
        hora_inicio_input.send_keys(Keys.TAB)

        print("Campo de hora de início preenchido com '{}'".format(hora))

        # Aguarda 2 segundos antes de preencher o campo de hora de término
        time.sleep(1)

        # Localiza o campo de hora de término e limpa o conteúdo
        hora_fim_input = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable(( ''))
        )
        hora_fim_input.send_keys(Keys.CONTROL + 'a')  # Seleciona todo o conteúdo
        hora_fim_input.send_keys(Keys.DELETE)         # Apaga o conteúdo

        # Preenche o campo de hora de término com "22:50"
        hora_fim_input.send_keys(horafinal)

        # Aguarda 2 segundos antes de clicar no botão "AGENDAR"
        time.sleep(1)

        # Localiza e clica no botão "AGENDAR"
        agendar_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable(( ''))
        )
        agendar_button.click()

        print("Clique no botão 'AGENDAR' realizado com sucesso!")
        hora_inicio = hora_inicio_input.get_property('value')
        hora_fim = hora_fim_input.get_property('value')

        # Aguarda a presença da mensagem de sucesso ou erro
        for _ in range(5):
            try:
                # Verifica se a mensagem de sucesso está presente
                mensagem_sucesso = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(( ''))
                )
                print("Compromisso salvo com sucesso!")
                # Envia webhook de sucesso
                enviar_webhook("AGENDADO COM SUCESSO")
                break
            except:
                pass
            try:
                # Verifica se a mensagem de erro está presente
                mensagem_erro = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(( ''))
                )
                print("Erro ao agendar compromisso!")
                # Envia webhook de erro
                enviar_webhook("ERRO AO AGENDAR")
                break
            except:
                pass
            time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente

        # Se nenhum dos casos acima for detectado
        else:
            print("Não foi possível verificar a mensagem de sucesso ou erro.")

    finally:
        # Fecha o navegador
        driver.quit()

    return "Compromisso agendado com sucesso para {} em {} às {} e {}".format(
    nome, data_formatada, hora_inicio, hora_fim)

if __name__ == '__main__':
    app.run(debug=True)