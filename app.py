from flask import Flask, abort, request, jsonify
import json


app = Flask(__name__)

appointments = []


@app.route('/setappointment/', methods=['POST'])
def set_appointment():
    if request.method == 'POST':
        customer = {}
        name = request.args['name']
        time = request.args['time']
        number = request.args['number']
        customer['id'] = len(appointments) + 1
        customer['name'] = name
        customer['time'] = time
        customer['number'] = number
        customer['isComplete'] = False
        customer['workApproved'] = False
        customer['price'] = None
        customer['techName'] = 'Rebel Tech'
        customer['hasArrived'] = False
        customer['issue'] = 'Doesnt work'
        customer['custComment'] = 'Fix it'
        customer['techComment'] = 'Fixing your car'
        appointments.append(json.dumps(customer))
        return json.dumps(customer)


@app.route('/getappointment/<int:task_id>', methods=['GET'])
def get_appointment(task_id):
    if request.method == 'GET':
        return appointments[task_id]


if __name__ == '__main__':
    app.run()
