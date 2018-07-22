from flask import Flask, request
from redis import Redis, RedisError
import os, json, sys

app = Flask(__name__)

def load_keys():
    try:
        r = Redis(host=os.environ['REDIS_SERVER'])
    except:
        sys.stderr.write('Unable to contact redis DB; exiting from load_keys()\n')
        exit()
    r.flushall()
    keys = json.load(open(os.environ['KEY_FILE']))
    for key in keys:
        r.set(key['id']+'_key', key['key'])

def verify_key(id, key, headers):
    return True

@app.route('/set/<string:id>', methods=['POST'])
def set_item(id):
    if '_key' in id:
        return '{"error":"No such endpoint"}'
    try:
        r = Redis(host=os.environ['REDIS_SERVER'])
    except:
        sys.stderr.write('Unable to contact redis server for set\n')
        return '{"error":"Redis Error"}'
    key = r.get(id+'_key')
    if verify_key(id, key, request.headers):
        try:
            r.set(id, request.get_data())
            return '{"success":true}'
        except:
            sys.stderr.write('Unable to set redis key ' + id + '\n')
            return '{"error":"Redis Error"}'
    else:
        sys.stderr.write('Failed to validate provided API key\n')
        return '{"error": "Bad Key"}'

@app.route('/get/<string:id>')
def get_item(id):
    sys.stderr.write('Get request for ' + id + '\n')
    if '_key' in id:
        return '{"error":"No such endpoint"}'
    try:
        r = Redis(host=os.environ['REDIS_SERVER'])
    except:
        sys.stderr.write('Unable to contact redis server for get\n')
        return '{"error":"Redis Error"}'
    key = r.get(id+'_key')
    if verify_key(id, key, request.headers):
        try:
            sys.stderr.write('Getting data from ' + id + '\n')
            result = r.get(id)
            if result is None:
                return '{"error":"No such endpoint"}'
            else:
                return(str(result))
        except RedisError:
            sys.stderr.write('Unable to get redis key ' + id + '\n')
            return '{"error":"Redis Error"}'
    else:
        sys.stderr.write('Failed to validate provided API key\n')
        return '{"error": "Bad Key"}'

if __name__ == '__main__':
    load_keys()
    sys.stderr.write('Starting reflector\n')
    app.run(host='0.0.0.0')
