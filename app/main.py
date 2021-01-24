import os
from typing import Optional

import mechanicalsoup
from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, status, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware

# from pydantic import BaseModel

# class User(BaseModel):
#     usuario: str
#     contrasena: str


load_dotenv()
BASE_URL = os.environ.get('BASE_URL')
CERT_PEM_PATH = os.environ.get('CERT_PEM_PATH')
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
FAIL_AUTH = b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n\n<link rel="stylesheet" type="text/css" href="/sistema/includes/css/tec_estilo.css" />\n<script type="text/javascript" src="/sistema/includes/funciones/js/funciones.js"></script>\n\n<script type="text/javascript">\n\nfunction cambiar_imagen(id, imagen)\n{\n\tx=document.getElementById(id);\n\tx.src = "/sistema/img/acceso/"+imagen;\n}\n\nfunction mostrar(t)\n{\n\tdocument.acceso.tipo.value = t;\n\tacc = document.getElementById("tabla_acceso");\n\ttexto_usr = document.getElementById("user");\n\ttexto_pws = document.getElementById("pass");\n\tasp = document.getElementById("aspirantes");\n\n\tswitch(t)\n\t{\n\t\tcase \'p\':\t//asp.style.visibility = "hidden";\n\t\t\t\t\t\t\t//alert ("ATENCION: SE LES COMUNICA QUE POR MANTENIMIENTO A LA RED ELECTRICA(CFE) EL SISTEMA ESTARA FUERA DE SERVICIO\\nDEL 29 DE JULIO A LAS 21:00 HORAS A EL 30 DE JULIO A LAS 13:00 HORAS.");\n\n\t\t\t\t\t\t\tacc.style.visibility = "visible";\n\t\t\t\t\t\t\ttexto_usr.innerHTML = "Usuario:";\n\t\t\t\t\t\t\ttexto_pws.innerHTML = "Contrase\xf1a:";\n\t\t\t\t\t\t\tdocument.acceso.usuario.focus()\n\t\t\t\t\t\t\tbreak;\n\t\tcase \'a\':\t//asp.style.visibility = "hidden";\n\t\t\t\t\t\t\t//alert ("ATENCION: SE LES COMUNICA QUE POR MANTENIMIENTO A LA RED ELECTRICA(CFE) EL SISTEMA ESTARA FUERA DE SERVICIO\\nDEL 29 DE JULIO A LAS 21:00 HORAS A EL 30 DE JULIO A LAS 13:00 HORAS.");\n\t\t\t\t\t\t\t//alert ("AVISO IMPORTANTE: ERES ALUMNO DE PRIMER SEMESTRE Y NECESITAS IMPRIMIR LA FICHA DE PAGO, EN LA OPCION DE MENU: INSCRIPCIONES Y EN EL TITULO DE PRE-FICHA DE PAGO LA PUEDES IMPRIMIR\\n");\n\t\t\t\t\t\t\t//alert ("ATENCION: SE LES INFORMA QUE DEBIDO A LAS ANOMALIAS EN EL PROCESO DE INSCRIPCION SE PROCEDERA A REINICIAR EL PROCESO. \\n FAVOR DE CHECAR REDES SOCIALES OFICIALES PARA MAYOR INFORMACION.");\n\t\t\t\t\t\t\tacc.style.visibility = "visible";\n\t\t\t\t\t\t\ttexto_usr.innerHTML = "No. de Control:";\n\t\t\t\t\t\t\ttexto_pws.innerHTML = "NIP:";\n\t\t\t\t\t\t\tdocument.acceso.usuario.focus()\n\t\t\t\t\t\t\tbreak;\n\t\tcase \'s\':\t\n\t\t\n\t\t\n\t\t//alert ("\xbfEres aspirante nuevo y NO te has registrado ?. \\nRealiza tu pago, Canjea por Recibo Oficial y Acude a Oficina de Servicios Escolares del Instituto para que te proporcione acceso al sistema con tu correspondiente No solicitud y NIP. \\n Si ya cuentas con tu n\xfamero de solicitud proporciona tu n\xfamero y tu NIP correspondiente para actualizar los datos de la solicitud.");\n\t\t\t\t\t\t\tacc.style.visibility = "visible";\n\t\t\t\t\t\t\ttexto_usr.innerHTML = "No. Solicitud:";\n\t\t\t\t\t\t\ttexto_pws.innerHTML = "NIP:";\n\t\t\t\t\t\t\tdocument.acceso.usuario.focus();\n\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\tbreak;\n\t\t\t\t\t\t\t/*acc.style.visibility = "hidden";\n\t\t\t\t\t\t\tasp.style.visibility = "visible";\n\t\t\t\t\t\t\tbreak;*/\n\t}\n}\n\n\nfunction valida_datos()\n{\n\tformulario = document.acceso;\n\tif(formulario.tipo.value==\'p\')\n\t{\n\t\tmsj_usr = "usuario";\n\t\tmsj_pws = "contrase\xf1a";\n\t}\n\telse \n\t{\n\t\tmsj_usr = "n\xfamero de control";\n\t\tmsj_pws = "nip";\n\t\tif (formulario.tipo.value==\'s\')\n\t\t{\n\t\t\tif(isNaN(formulario.usuario.value))\n\t\t\t{\n\t\t\t\twindow.alert("Introduce un n\xfamero de solicitud num\xe9rico");\t\n\t\t\t\tformulario.usuario.focus();\n\t\t\t\treturn false;\t\n\t\t\t}\n\t\t}\n\t\t\n\t\tif(isNaN(formulario.contrasena.value))\n\t\t{\n\t\t\twindow.alert("Introduce un NIP num\xe9rico");\n\t\t\tformulario.contrasena.focus();\n\t\t\treturn false;\t\n\t\t}\n\t\tif(formulario.contrasena.value.length>4)\n\t\t{\n\t\t\twindow.alert("Introduce un NIP de 4 caracteres");\n\t\t\tformulario.contrasena.focus();\n\t\t\treturn false;\t\n\t\t}\n\t}\t\n\t\n\tif(formulario.usuario.value=="" || formulario.usuario.value==null)\n\t{\n\t\twindow.alert("Por favor introduce tu "+msj_usr);\n\t\tformulario.usuario.focus();\n\t\treturn false;\n\t}\n\t\n\tif(formulario.contrasena.value=="" || formulario.contrasena.value==null)\n\t{\n\t\twindow.alert("Por favor introduce tu "+msj_pws);\n\t\tformulario.contrasena.focus();\n\t\treturn false;\n\t}\n\treturn true\n\t//formulario.submit();\n}\n</script>\n</script>\n<title>SII :: Acceso</title>\n</head>\n\n<body> <!--onload="document.forms[0].elements[0].focus()"-->\n\t\n\t\t<form name="acceso" action="/sistema/acceso.php" method="post" onSubmit="return valida_datos()">\n\t\t\t<input name="tipo" type="hidden" value="a" />\n\t\t\t<table width="700" border="0" align="center" cellspacing="0" cellpadding="0">\n\t\t\t\t<tr>\n\t\t\t\t\t<td align="left" bgcolor="#eeeeee" height="60"> \n\t\t\t\t\t\t<img src="/sistema/img/acceso/personal.gif" onClick="mostrar(\'p\');" id="img_personal" onMouseOver="cambiar_imagen(\'img_personal\',\'personal_over.gif\',1)" onMouseOut="cambiar_imagen(\'img_personal\',\'personal.gif\')" /> \n\t\t\t\t\t</td>\n\t\t\t\t</tr>\n\t\t\t\t<tr>\n\t\t\t\t\t<td align="center" bgcolor="#eeeeee" height="60"> \n\t\t\t\t\t\t<img src="/sistema/img/acceso/alumnos.gif" onClick="mostrar(\'a\');" id="img_alumnos" onMouseOver="cambiar_imagen(\'img_alumnos\',\'alumnos_over.gif\',1)" onMouseOut="cambiar_imagen(\'img_alumnos\',\'alumnos.gif\')" />\n\t\t\t\t\t</td>\n\t\t\t\t</tr>\n\t\t\t\t<tr>\n\t\t\t\t\t<td align="right" bgcolor="#eeeeee" height="60"> \n\t\t\t\t\t\t<img src="/sistema/img/acceso/aspirantes.gif" onClick="mostrar(\'s\');" id="img_aspirantes" onMouseOver="cambiar_imagen(\'img_aspirantes\',\'aspirantes_over.gif\',1)" onMouseOut="cambiar_imagen(\'img_aspirantes\',\'aspirantes.gif\')" /> \n\t\t\t\t\t</td>\n\t\t\t\t</tr>\n\t\t\t</table>\n\t\t\t\t\t\t\t\t\t<div align="center" style="visibility:visible" id="tabla_acceso">\n\t\t\t\t<table align="center" width="360" cellspacing="2" cellpadding="2" border="0">\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th align="center" colspan="2"> Autentificaci\xf3n para acceso al sistema </th>\n\t\t\t\t\t</tr>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td colspan="2" align="center" id="rojo"> Datos incorrectos \xf3 no tiene acceso, verifique...</td>\n\t\t\t\t\t</tr>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th align="left" width="110" id="user"> No. de Control: </th>\n\t\t\t\t\t\t<td align="left" width="179"> <input type="Text" name="usuario" size="35" maxlength="30"> </td>\n\t\t\t\t\t</tr>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<th align="left" id="pass"> NIP: </th>\n\t\t\t\t\t\t<td align="left"><input type="password" name="contrasena" size="35" maxlength="15"></td>\n\t\t\t\t\t</tr>\n\t\t\t\t</table>\n\t\t\t\t<br />\n\t\t\t\t<div align="center">\n\t\t\t\t\t<input class="boton" type="submit" value="Acceso" />\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</form>\n\t\t\n</body>\n</html>\n'

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
browser.session.verify = CERT_PEM_PATH
# browser.set_verbose(2)


@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.route("/")
# def hello_world():
#     return render_template('index.html')

"""Cookies is not cleared if login fails. Cookie can be the same of the
    last attempt because it's not linked to any logged account,
    and its slower to delete cookie in every failure"""
@app.post("/login")
def login(
        response: Response,
        usuario: str = Form(default=None,min_length=8,max_length=8),
        contrasena: str = Form(default=None,min_length=4,max_length=4)
):
    if not usuario or not contrasena:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    browser.open(f'{BASE_URL}acceso.php', allow_redirects=False)
    browser.select_form()
    if not browser.get_current_form():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    browser['usuario'] = usuario
    browser['contrasena'] = contrasena
    browser['tipo'] = 'a'
    if browser.submit_selected().content == FAIL_AUTH:
        raise HTTPException(status_code=401)
    for key, value in browser.get_cookiejar().iteritems():
        response.set_cookie(
            key=key,
            value=value,
            samesite='None',
            secure=True
        )
    browser.session.cookies.clear()
    return 'logged in'


@app.get('/calif')
def calif(phpsessid: Optional[str] = Cookie(None,alias='PHPSESSID')):
    if not phpsessid:
        raise HTTPException(status_code=401)
    if browser.open(f'{BASE_URL}modulos/alu//cons/calif_parciales_adeudo.php', cookies={'PHPSESSID': phpsessid}).content == NOAUTH:
        raise HTTPException(status_code=401)
    browser.get_current_page().find('link').extract()
    return str(browser.get_current_page())


@app.get('/kardex')
def kardex(phpsessid: str = Cookie(None, alias='PHPSESSID')):
    if not phpsessid:
        raise HTTPException(status_code=401)
    if browser.open(f'{BASE_URL}modulos/cons/alumnos/kardex.php', cookies={'PHPSESSID': phpsessid}).content == NOAUTH:
        raise HTTPException(status_code=401)
    return str(browser.get_current_page())


@app.get('/session')
def session(phpsessid: str = Cookie(None, alias='PHPSESSID')):
    if not phpsessid:
        raise HTTPException(status_code=401)
    if browser.get(f'{BASE_URL}modulos/cons/alumnos/manto_alumno.php', cookies={'PHPSESSID': phpsessid}, allow_redirects=False).content == NOAUTH:
        raise HTTPException(status_code=401)
    return {'message': 'You are logged in'}


@app.get('/signout')
def logout(phpsessid: str = Cookie(None, alias='PHPSESSID')):
    if not phpsessid:
        raise HTTPException(status_code=400)
    res = browser.get(f'{BASE_URL}cerrar_sesion.php', cookies={'PHPSESSID': phpsessid}, allow_redirects=False)
    if not res.ok:
        raise HTTPException(status_code=res.status_code)

