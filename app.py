from flask import Flask, redirect, make_response, request, render_template
import redis
import re
import random

app = Flask(__name__)
# redis config
r = redis.StrictRedis(host='europa.stsosz.io', port=6380, db=0)
# key generation
# character set
kc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# length
kl = 8
# max tries when generating a random key
mt = 80

def jresp(j, val=200):
    resp = make_response(j, val)
    resp.mimetype = 'application/json'
    return resp

@app.route("/json/get/<key>")
def getjson(key):
    paste = r.get('paste:'+key)
    if paste is None:
        return jresp("{\"code\":\"3\", \"msg\":\"A post with that title was not found\"}")
    return jresp("{\"code\":\"0\", \"msg\":\""+key+"\"}")

@app.route("/json/add", methods=['POST'])
def addjson():
    # check if value is in post, if not then assume is GET
    if 'paste' in request.form:
        paste = request.form['paste']
    else:
        return jresp("{\"code\":\"1\", \"msg\":\"No paste given\"}", 400)
    # only try mt amount of times
    for x in range(0, mt):
        key = ''.join(random.choice(kc) for _ in range(kl))
        if r.get('paste:'+key) is None:
            break
        if x==mt:
            # didnt get anywhere, return error
            return jresp("{\"code\":\"2\", \"msg\":\"key could not be generated in sane amount of time\"}", 400)
    r.set('paste:'+key, paste)
    return jresp("{\"code\":\"0\",\"msg\":\""+key+"\"}")

@app.route("/raw/<key>")
def fetchraw(key):
    paste = r.get('paste:'+key)
    if paste is None:
        return render_template('index.html', err="A post with that title was not found")
    resp = make_response(paste)
    resp.mimetype = 'text/plain'
    return resp

@app.route("/<key>")
def fetch(key):
    paste = r.get('paste:'+key)
    if paste is None:
        return render_template('index.html', err="A post with that title was not found")
    return render_template('index.html', content=paste, raw=True, key=key)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')