from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests
from datetime import datetime

app = Flask(__name__)

# Função para enviar o webhook
def enviar_webhook(mensagem):
    url = "https://webhook.n8n.agenciataruga.com/webhook/df4b672e-3c16-4490-b8fb-47fa6eeeadd0"
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

    # Inicializa o driver do Chrome
    driver = webdriver.Chrome()

    try:
        # Acessa o site
        driver.get("https://office.zenklub.com.br/")

        # Simula um clique no campo de e-mail e preenche com o e-mail
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#email"))
        )
        email_field.click()
        email_field.send_keys("consultasbrunaduarte@gmail.com")

        # Simula um clique no campo de senha antes de preenchê-lo
        senha_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-login/section/div[1]/form/zk-input[2]/label/input"))
        )
        senha_field.click()

        # Preenche o campo de senha com a senha
        senha_field.send_keys("Zenk@20244@")

        # Clica no botão de login
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-login/section/div[1]/form/div/button"))
        )
        login_button.click()

        print("Login realizado com sucesso!")

        # Aguarda a presença do botão "AGENDAR +"
        agendar_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="calendar-content"]/div[1]/div[3]/freud-button/p-button/button'))
        )

        # Clica no botão "AGENDAR +"
        agendar_button.click()

        print("Clique no botão 'AGENDAR +' realizado com sucesso!")

        # Aguarda mais 5 segundos após clicar em "AGENDAR +"
        time.sleep(2)

        # Clica no botão "COMPROMISSO PARTICIPAR"
        compromisso_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="bodyCalendar"]/app-root/app-calendar/appointment-sidebar/modal-sidebar/div/div/div[1]/div/div/freud-select-button/p-selectbutton/div/div[3]'))
        )
        compromisso_button.click()

        print("Clique no botão 'COMPROMISSO PARTICIPAR' realizado com sucesso!")

        # Aguarda 20 segundos após clicar em "COMPROMISSO PARTICIPAR"
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Escreva aqui"]')))

        # Localiza o campo "COMPROMISSO PARTICIPAR" e preenche com "EVENTO TESTE"
        compromisso_textarea = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//textarea[@placeholder="Escreva aqui"]'))
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
            EC.element_to_be_clickable((By.XPATH, '//p-calendar//input[@aria-required="true"]'))
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
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#initialTime > div > p-calendar > span > input'))
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
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#finalTime > div > p-calendar > span > input'))
        )
        hora_fim_input.send_keys(Keys.CONTROL + 'a')  # Seleciona todo o conteúdo
        hora_fim_input.send_keys(Keys.DELETE)         # Apaga o conteúdo

        # Preenche o campo de hora de término com "22:50"
        hora_fim_input.send_keys(horafinal)

        # Aguarda 2 segundos antes de clicar no botão "AGENDAR"
        time.sleep(1)

        # Localiza e clica no botão "AGENDAR"
        agendar_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="bodyCalendar"]/app-root/app-calendar/appointment-sidebar/modal-sidebar/div/div/div[3]/div/freud-button[2]/p-button/button'))
        )
        agendar_button.click()

        print("Clique no botão 'AGENDAR' realizado com sucesso!")

        # Aguarda a presença da mensagem de sucesso ou erro
        for _ in range(5):
            try:
                # Verifica se a mensagem de sucesso está presente
                mensagem_sucesso = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.p-toast-message-success'))
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
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.p-toast-message-error'))
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

    return "Compromisso agendado com sucesso para {} em {} às {}".format(nome, data_formatada, hora, horafinal)

if __name__ == '__main__':
    app.run(debug=True)
