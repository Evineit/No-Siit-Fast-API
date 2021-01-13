import os
from warnings import filterwarnings

from typing import Optional
from fastapi import FastAPI, Form, HTTPException, status, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import mechanicalsoup
# from pydantic import BaseModel

from urllib3.exceptions import InsecureRequestWarning

# class User(BaseModel):
#     usuario: str
#     contrasena: str


load_dotenv()
filterwarnings(action='ignore', category=InsecureRequestWarning)
BASE_URL = os.environ.get('BASE_URL')
app = FastAPI()
origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOAUTH = b'\t\t<script type="text/javascript"> \r\n  \t\twindow.top.location = "/sistema";\r\n  \t\t/*alert("PARA ACCEDER A ESTA OPCI\xd3N ES NECESARIO AUTENTIFICARSE EN EL SISTEMA")\r\n  \t\tjavascript: close()\r\n  \t\tjavascript: history.go(-1)*/\r\n\t\t</script> \r\n\t\tSi esta viendo este mensaje, es porque no tiene habilitado Javascript en su navegador, habilitelo y trate de nuevo'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "es-ES,es;q=0.9,en;q=0.8,en-GB;q=0.7",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "frame",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

browser = mechanicalsoup.StatefulBrowser(user_agent=HEADERS.get('User-Agent'))
browser.session.headers.update(HEADERS)


# browser.set_verbose(2)

@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.route("/")
# def hello_world():
#     return render_template('index.html')


# @app.get("/start")
# def get_cookie():
#     if browser.get_cookiejar().get('PHPSESSID'):
#         return
#     browser.open(f'{BASE_URL}acceso.php', verify=False)
#     if browser.get_cookiejar().get('PHPSESSID'):
#         return
#     raise HTTPException(
#         status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@app.post("/login")
def login(
        response: Response,
        usuario: str = Form(default=None),
        contrasena: str = Form(default=None)
):
    browser.open(f'{BASE_URL}acceso.php', verify=False, allow_redirects=False)
    browser.select_form()
    browser['usuario'] = usuario
    browser['contrasena'] = contrasena
    browser['tipo'] = 'a'
    # print(browser.get_current_form().print_summary())
    browser.submit_selected()
    print(browser.get_cookiejar())
    for key, value in browser.get_cookiejar().iteritems():
        response.set_cookie(
            key=key,
            value=value,
            samesite='None',
            secure=True
        )
    # TODO: Remove cookies for stateless login
    # Response.
    # TODO: Maybe pass no redirect
    # Add validation of being logged in
    return 'logged in'


# @app.get('/calif')
# def calif():
#     if not browser.get_cookiejar().get('PHPSESSID'):
#         raise HTTPException(status_code=401)
#     browser.open(f'{BASE_URL}modulos/alu//cons/calif_parciales_adeudo.php', verify=False)
#     # TODO: Remove tec_estilo.css
#     # browser
#     browser.get_current_page().find('link').extract()
#     return str(browser.get_current_page())
#     # return s.cookies.get('PHPSESSID')


# @app.get('/session', status_code=status.HTTP_204_NO_CONTENT)
# def session():
#     if not browser.get_cookiejar().get('PHPSESSID'):
#         raise HTTPException(status_code=401)
#     if browser.get(f'{BASE_URL}modulos/alu//cons/calif_parciales_adeudo.php', verify=False) == NOAUTH:
#         raise HTTPException(status_code=401)

@app.get('/calif')
def calif(phpsessid: Optional[str] = Cookie(None,alias='PHPSESSID')):
    if not phpsessid:
        raise HTTPException(status_code=401)
    print(phpsessid)
    x = mechanicalsoup.StatefulBrowser()
    x.session.headers.update(HEADERS)
    x.session.cookies.set('PHPSESSID', phpsessid)
    x.open(f'{BASE_URL}modulos/alu//cons/calif_parciales_adeudo.php', verify=False)
    browser.open(f'{BASE_URL}modulos/alu//cons/calif_parciales_adeudo.php', verify=False)
    # browser
    x.get_current_page().find('link').extract()
    return str(x.get_current_page())
    # return s.cookies.get('PHPSESSID')


@app.get('/session', status_code=status.HTTP_204_NO_CONTENT)
def session(phpsessid: str = Cookie(None, alias='PHPSESSID')):
    if not phpsessid:
        raise HTTPException(status_code=401)
    x = mechanicalsoup.StatefulBrowser()
    x.session.headers.update(HEADERS)
    x.session.cookies.set('PHPSESSID', phpsessid)
    if x.get(f'{BASE_URL}modulos/alu//cons/calif_parciales_adeudo.php', verify=False) == NOAUTH:
        raise HTTPException(status_code=401)


@app.get('/signout')
def logout():
    res = browser.get(f'{BASE_URL}cerrar_sesion.php', verify=False)
    # browser.close()
    return "Signed out", res.status_code
