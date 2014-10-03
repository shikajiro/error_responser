from flask import Flask, abort, json, jsonify
app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, error_code, status_code=None, payload=None):
        Exception.__init__(self)
        if error_code in {0, 1, 2, 10, 11, 12, 13, 14}:
            self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        error_json = {
              'error':{
                    'code':self.error_code,
                    'message':"this is error message"
              }
        }
        return error_json

@app.route('/')
def hello_world():
    return 'Hello Error Responser!'

@app.route('/<int:status_code>')
def error_response(status_code):
    print "set status code %d" % (status_code)
    abort(status_code)

@app.route('/<int:status_code>/<int:error_code>')
def error_response_and_error_code(status_code, error_code):
    print "set status code %d, error code %d" % (status_code, error_code)
    raise InvalidUsage(error_code=error_code, status_code=status_code)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_json())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # app.run()
