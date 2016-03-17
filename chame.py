import os
from flask import Flask, request
import hashlib
import json
import urllib

app = Flask(__name__)

@app.route('/')
def hello():
	return "hola"

@app.route('/validarFirma', methods=['POST'])
def validarFirma():
	mensajeTesteo = request.form['mensaje']
	mensajeTesteoEnBytes = mensajeTesteo.encode('utf-8')
	mensajeHasheado = hashlib.sha256(mensajeTesteoEnBytes).hexdigest()
	mensajeAComparar = request.form['hash']
	mensajeAComparar = mensajeAComparar.lower()
	if (mensajeAComparar == mensajeHasheado):
		data = {}
		data['valido'] = True
		data["mensaje"] = mensajeAComparar
		json_data = json.dumps(data)
		return json_data
	else:
		data = {}
		data['valido'] = False
		data["mensaje"] = mensajeAComparar
		json_data = json.dumps(data)
		return json_data

@app.route('/status',methods=['GET'])
def retornarStatus():
	return app.make_response(('',201))

@app.route('/texto', methods=['GET'])
def upload_file():
    if request.method == 'GET':
		txt = urllib.urlopen("https://s3.amazonaws.com/files.principal/texto.txt").read()
		mensajeHash = hashlib.sha256(txt).hexdigest()
		texto = {}
		texto['text'] = txt
		texto['hash'] = mensajeHash
		texto_json = json.dumps(texto)
		return texto_json

if __name__ == '__main__':
	port = int(os.environ.get('PORT',5000))
	app.run(host='0.0.0.0', port = port)