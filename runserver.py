from meinformoapi import app
app.app.after_request(app.add_cors_headers)
app.app.run(threaded=True, host='0.0.0.0', debug=True)
