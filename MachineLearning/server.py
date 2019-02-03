from randomForest import MLmodule as ML
import random
import json

from flask import Flask, request
app = Flask(__name__)

# VALIDATION: will be taken care of in the front ends
# def validArgs(req):
#     if ('palp' in request.args) and ('chol' in request.args) and ('bmi' in request.args) and ########

@app.route('/')
def checkIfAtRisk():
    ht = float(request.args.get('height')) / 100   # height in meters
    wt = float(request.args.get('weight'))

    # Create dictionary
    patientData = {
        "palpitations": int(request.args.get('palpitations')),       # number of heart palpitations per minute
        "cholesterol": int(request.args.get('chol')),                # cholesterol level (combined)
        "bmi": int(wt/(ht * ht)),                                    # BMI computed based on height and weight
        "heartRate": int(request.args.get('heartRate')),
        "age": int(request.args.get('age')),
        "sex": request.args.get('sex'),
        "family-history": request.args.get('family-history'),
        "smoker": request.args.get('smoking-5'),
        "exercise": int(request.args.get('exercise'))
    }

    isAtRisk = ML(patientData)
    return str(isAtRisk)

@app.route('/fitbit', methods=['POST', 'GET'])
def getFitbitData():    # We need: minsExercise, palpitations, avgHeartrate
    randNum = random.randint(1,4)
    if (randNum == 1):
        with open('activity1.json') as f: data = json.load(f)
    elif (randNum == 2):
        with open('activity2.json') as f: data = json.load(f)
    else: # (randNum == 3)
        with open('activity3.json') as f: data = json.load(f)          

    fairlyActive = data['summary']['fairlyActiveMinutes']
    lightlyActive = data['summary']['lightlyActiveMinutes']
    veryActive = data['summary']['veryActiveMinutes']

    minsExercise = str(fairlyActive + lightlyActive + veryActive)
    heartRate = str(data['summary']['avgHeartRate'])
    heartPalpitations = str(data['summary']['heartPalpitations'])

    mystring = minsExercise + "," + heartRate + "," + heartPalpitations

    return mystring