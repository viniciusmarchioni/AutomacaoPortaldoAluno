from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import psycopg2
import time


conn = psycopg2.connect(
    host="xxxxxxxx", database="xxxxxxxx", user="xxxxxxxx", password="xxxxxxxx"
)  # Acesso postgresql


class aluno:
    def __init__(self, user, password):
        self.user = user
        self.password = password


cur = conn.cursor()  # Criando acesso ao banco de dados
servico = Service(ChromeDriverManager().install())  # Instalando o navegador

cur.execute("select max(id) from alunos")
size = cur.fetchone()[0]


def main(option):
    cur.execute(f"SELECT usuario FROM alunos WHERE id = {option};")
    user = cur.fetchone()[0]
    cur.execute(f"SELECT senha FROM alunos WHERE id = {option};")
    password = cur.fetchone()[0]
    usuario = aluno(user, password)

    option = webdriver.ChromeOptions()
    option.add_argument("--headless")

    navegador = webdriver.Chrome(options=option, service=servico)
    navegador.get(
        "https://interage.fei.org.br/secureserver/portal/graduacao/sala-dos-professores/aulas/presenca"
    )
    navegador.find_element("xpath", '//*[@id="Usuario"]').send_keys(usuario.user)
    navegador.find_element("xpath", '//*[@id="Senha"]').send_keys(usuario.password)
    navegador.find_element("xpath", '//*[@id="btn-login"]').click()

    varCountXpath = 0
    while True:
        try:
            xpath = f'//*[@id="cadastrar-{varCountXpath}"]'
            navegador.find_element(
                "xpath", xpath
            ).click()  # Atualizar o xpath da presença
            print("Presença cadastrada!")
            navegador.close()
            break

        except:
            varCountXpath += 1
            if varCountXpath == 10:
                print("Presença ainda não aberta\nTentando novamente em 60s...")
                time.sleep(60)
                varCountXpath = 0
                navegador.refresh()
                if (
                    navegador.current_url
                    != "https://interage.fei.org.br/secureserver/portal/graduacao/sala-dos-professores/aulas/presenca"
                ):
                    return "Algo deu errado"


for i in range(1, size + 1):
    main(i)

conn.close()  # Fechando conexão com banco de dados