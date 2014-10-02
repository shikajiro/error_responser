from flask import Flask, abort, json, jsonify
app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, msg_code, status_code=None, payload=None):
        Exception.__init__(self)
        if msg_code in {1, 2, 10, 11, 12, 13, 14}:
            self.msg_code = msg_code
        else:
            self.msg_code = 0
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        error_json = {
              'error':{
                    'code':self.msg_code,
                    'message':"this is error message"
              }
        }
        return error_json

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/<int:error_code>/<int:msg_code>')
def error_response(error_code, msg_code):
    print "set error code %d" % (error_code)
    raise InvalidUsage(msg_code=msg_code, status_code=error_code)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_json())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
