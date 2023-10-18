from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import psycopg2
import time
# Conexão
conn = psycopg2.connect(
    host="xxxxxxx",
    database="xxxxxx",
    user="xxxxxxx",
    password="xxxxxxx"
)
# Crie um cursor para executar consultas
cur = conn.cursor()

class aluno:
    def __init__(self, user, password):
        self.user =user
        self.password = password
    
print('''
      Presença automatica:
      0-Arnaldo
      1-Enzo
      2-Lorena
      3-Vinicius
      ''')
cur = conn.cursor()
try:
    option = int(input("opção: "))

    while(option<0 or option>3):
        option = int(input("opção: "))
except:
    print("COLOCA A PORRA DE UM NUMERO")
    option = int(input("opção: "))

    while(option<0 or option>3):
        option = int(input("opção: "))

options_p_nomes = {
    0: 'Arnaldo',
    1: 'Enzo',
    2: 'Lorena',
    3: 'Vinicius'
}

nome = options_p_nomes[option]

cur.execute("select usuario from alunos where nome = '"+nome+"';")
user = cur.fetchone()[0]
cur.execute("select senha from alunos where nome = '"+nome+"';")
password = cur.fetchone()[0]
usuario = aluno(user,password)

# Feche o cursor e a conexão
cur.close()
conn.close()


servico = Service(ChromeDriverManager().install())
option = webdriver.ChromeOptions()
option.add_argument('--headless')

navegador = webdriver.Chrome(options=option,service=servico)
navegador.get("https://interage.fei.org.br/secureserver/portal/")
navegador.find_element('xpath','//*[@id="Usuario"]').send_keys(usuario.user)
navegador.find_element('xpath','//*[@id="Senha"]').send_keys(usuario.password)
navegador.find_element('xpath','//*[@id="btn-login"]').click()
navegador.find_element('xpath','//*[@id="nav-home"]/li[11]/a').click()

while True:
    try:
        navegador.find_element('xpath','//*[@id="cadastrar-5"]').click() #atualizar o xpath
        break
    except:
        print("Presença ainda não aberta\nTentando novamente em 60s...")
        time.sleep(60)
        navegador.refresh()