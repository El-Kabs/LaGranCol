import json
import math
import random
import utils
import time
import datetime
from flask import Flask, request
import math

app = Flask(__name__)

data = "438.2633634783864,186.37216723514948,454.2766544841678,87.10955380356526,474.3867255673035,255.54615653443673,466.4401611169303,138.6836451097427,502.9572524653339,216.92162512604455,444.94717613077626,228.13480401924832,480.3611587601357,347.60806469330885,404.77099570299674,305.21135793269224,492.094984292024,117.26250986417203,432.8268638749349,148.42873839714773,476.87562903995104,242.13240746759945,401.87138214409504,210.8251549062853,437.0722287826331,301.42861322886574,519.7568539811517,66.32186142342105,472.6150220284845,98.65153390398044,507.07527695709814,280.9786534550593,378.17959006490275,327.4562562420789,508.54545667784885,156.06021874383464,435.7513525213346,250.5705101802268,429.6952820956763,235.07254633926175,492.699240203572,192.75244994109957,450.58543148060636,129.6585021476646,446.8548004269021,261.9518735217093,413.66192651749066,266.645859316867,558.8888553910843,196.42643183837524,542.2425179813807,227.1598544844675,431.17047194165826,356.4466294853668,544.7460947904583,408.8287339963778,616.1271580606194,298.080154479216,529.0425455668212,318.23715946588356,569.6823374407016,351.9515156018002,599.5767042152997,245.52424034643622,281.9355815773836,26.988813872475767"
data = data.split(",")

jsonC = ""
insurrects = 0
vInsu = 0
jsonUltimoT = {}
fecha = datetime.datetime.now()

i = 0
with open('granColombia.geo.json', 'r', encoding='utf8') as f:
	jsonC = json.load(f)

def distancia(puntoA, puntoB):
	return math.sqrt(pow((float(puntoB[0])-float(puntoA[0])), 2) + pow((float(puntoB[1])-float(puntoA[1])), 2))

	
def darFronteras(departamento):
	return departamento['properties']['FRONTERAS']
def kNN(departamento):
	global jsonC
	#k = utils.darCuantos(departamento['properties']['NOMBRE_DPT'])
	print(departamento['properties']['NOMBRE_DPT'])
	k = int(random.randint(4,7))
	#k = 5
	centroide = departamento['properties']['CENTROIDE']
	retorno = []
	for x in jsonC['features']:
		aux = {}
		distanciaB = distancia(centroide, x['properties']['CENTROIDE'])
		aux = (distanciaB, x['properties']['NOMBRE_DPT'])
		retorno.append(aux)
	retorno = sorted(retorno)
	return retorno[1:k+1]

def elegirPaisAtacar():
	global jsonC
	depto = random.choice(jsonC['features'])
	return depto

def darFinDeJuego():
	global jsonC
	temp = jsonC['features'][0]['properties']['DOMINADO']
	igual = True
	for x in jsonC['features']:
		if temp != x['properties']['DOMINADO']:
			igual = False
			break
	return igual
finJuego = darFinDeJuego()	
def darPaisesInsurrect():
	global jsonC
	retorno = []
	for x in jsonC['features']:
		aux = {}
		if(x['properties']['NOMBRE_DPT']!=x['properties']['DOMINADO']):
			aux = x
			retorno.append(aux)
	return retorno
	
def insurrectM():
	global jsonC
	global insurrects
	global vInsu
	global jsonUltimoT
	insurrects = insurrects + 1
	insurre = darPaisesInsurrect()
	if(len(insurre)>0):
		deptoInsurre = random.choice(insurre)
		dominado = deptoInsurre['properties']['NOMBRE_DPT']
		dominador = deptoInsurre['properties']['DOMINADO']
		azarDominado = (random.random()*3)
		azarDominador = (random.random()*100)
		if(azarDominado>azarDominador):
			for x in jsonC['features']:
				if((x['properties']['NOMBRE_DPT'] == dominado) and (x['properties']['DOMINADO'] == dominador)):
					vInsu = vInsu + 1
					x['properties']['DOMINADO'] = dominado
					#guardar()
					jsonUltimoT['Insurrecion'] = dominado+" se revelo contra "+dominador+" y gano."
		else:
			jsonUltimoT['Insurrecion'] = dominado+" se revelo contra "+dominador+" y perdio."
	else:
		return


		
def darProbabilidad(territorio):
	prob = 1
	for x in jsonC['features']:
		if(x['properties']['DOMINADO'] == territorio):
			prob = prob + 0.5
	return int(math.floor(prob))

def turno():
	global jsonC
	global i
	global jsonUltimoT
	insurrect = random.random()*100
	if(insurrect>98):
		insurrectM()
	deptoAtaca = elegirPaisAtacar()
	#cercanos = kNN(deptoAtaca)
	cercanos = darFronteras(deptoAtaca)
	deptoDefender = random.choice(cercanos)
	azarAtaque = (random.random()*100)
	azarDefensa = (random.random()*100)
	indice = jsonC['features'].index(deptoAtaca)
	nombreAtaca = jsonC['features'][indice]['properties']['DOMINADO']
	#print("ATACA: "+jsonC['features'][indice]['properties']['DOMINADO'])
	#print("AZAR ATACA: "+str(azarAtaque))
	#print("DEFIENDE: "+deptoDefender[1])
	#print("AZAR DEFIENDE: "+str(azarDefensa))
	defiend = ""
	for x in jsonC['features']:
		if(x['properties']['NOMBRE_DPT']==deptoDefender):
			defiend = x['properties']['DOMINADO']
	probAtaca = int(darProbabilidad(nombreAtaca))
	
	probDefensa = int(darProbabilidad(defiend))
	if(nombreAtaca==defiend):
		i = i - 1
	else:
		if(azarAtaque+probAtaca>azarDefensa+probDefensa):
			for x in jsonC['features']:
				if(x['properties']['NOMBRE_DPT'] == deptoDefender):
					x['properties']['DOMINADO'] = nombreAtaca
					jsonUltimoT['TurnoText'] = nombreAtaca+" ataco prob: "+str(probAtaca)+" a "+deptoDefender+" prob: "+str(probDefensa)+" y gano."
					print(nombreAtaca+" ataco prob: "+str(probAtaca)+" a "+deptoDefender+" prob: "+str(probDefensa)+" y gano.")
					#guardar()
					#print("GANA: "+str(nombreAtaca))
		else:
			print(nombreAtaca+" ataco a "+deptoDefender+" y perdio.")
			jsonUltimoT['TurnoText'] = nombreAtaca+" ataco a "+deptoDefender+" y perdio."
			i=i-1

				
def darStatus():
	global jsonC
	global insurrects
	global vInsu
	for x in jsonC['features']:
		print("DEPTO: "+str(x['properties']['NOMBRE_DPT']))
		print("DOMINA: "+str(x['properties']['DOMINADO']))
	print("INSURRECCIONES: "+str(insurrects))
	print("VALIDAS: "+str(vInsu))

def guardar():
	global jsonC
	print(jsonC['features'][0]['properties'])
	with open('granColombia.geo.json', 'w', encoding='utf8') as f:
		json.dump(jsonC, f)

def ultimoTurno(i):
	global jsonUltimoT
	global jsonC
	global fecha
	jsonUltimoT["Turno"] = i
	jsonUltimoT["Fecha"] = str(fecha)
	ranking = {}
	for x in jsonC['features']:
                if(x['properties']['DOMINADO'] in ranking):
                        ranking[x['properties']['DOMINADO']] = int(ranking[x['properties']['DOMINADO']]) + 1
                else:
                        ranking[x['properties']['DOMINADO']] = 1
                jsonUltimoT['ranking'] = ranking
	guardar()
	with open('data.json', 'w', encoding='utf8') as f:
		json.dump(jsonUltimoT, f)

@app.route("/simular", methods=["GET"])
def simular():
		global i
		global fecha
		print("Inicio turno: ", i)
		print("Fecha: ", fecha)
		jsonF = {}
		with open('data.json', 'r', encoding='utf8') as f:
			jsonF = json.load(f)
		if 'Fecha' in jsonF:
			print(type(jsonF['Fecha']))
			ff = datetime.datetime.strptime(jsonF['Fecha'], '%Y-%m-%d %H:%M:%S.%f')
			print(type(ff))
			fecha = ff +datetime.timedelta(days=1)
		else:
			fecha = datetime.datetime.now()
			
		finJuego = darFinDeJuego()
		
		
			
		while not finJuego:
			turno()
			finJuego = darFinDeJuego()
			i = i + 1
			
		if(finJuego):
			darStatus()
			print(i)
			print("FIN")
			ultimoTurno(i)
			darStatus()
			guardar()
			i = i + 1
			
		print("Fin guardar")
		
		print(finJuego)
		
		print("Fin turno: ", i)
		
		
		return "Turno++"
@app.route("/turno", methods=["GET"])
def hacerTurno():
		global i
		global fecha
		print("Inicio turno: ", i)
		print("Fecha: ", fecha)
		jsonF = {}
		with open('data.json', 'r', encoding='utf8') as f:
			jsonF = json.load(f)
		if 'Fecha' in jsonF:
			print(type(jsonF['Fecha']))
			ff = datetime.datetime.strptime(jsonF['Fecha'], '%Y-%m-%d %H:%M:%S.%f')
			print(type(ff))
			fecha = ff +datetime.timedelta(days=1)
		else:
			fecha = datetime.datetime.now()
		turno()
		print("Fin guardar")
		finJuego = darFinDeJuego()
		i = i + 1
		print("Fin turno: ", i)
		ultimoTurno(i)
		if(finJuego):
			darStatus()
			print(i)
			print("FIN")
		return "Turno++"

@app.route("/mapa", methods=["GET"])
def darMapa():
        with open('granColombia.geo.json', 'r', encoding='utf8') as f:
                return str(json.load(f))
        
@app.route("/data", methods=["GET"])
def darData():
        with open('data.json', 'r', encoding='utf8') as f:
                return str(json.load(f))

if __name__ == '__main__':
    app.run(debug=True)
	
	
	
