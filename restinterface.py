#!/usr/bin/python
from flask import Flask
from flask_restful import reqparse, Api, Resource
import dnszone as dns
import database


dn = dns.DnsZone("clim.test", "127.0.0.1")

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

parser.add_argument('fqdn')
parser.add_argument('ip')
parser.add_argument("name")
parser.add_argument("token")

class DnsNew(Resource):
    # curl http://172.31.1.5:5001/dns/new -d "name=Narek" -d "token=87da83fe-a7d5-11ec-a4ac-000c298d0891" -d "fqdn=narek.clim.test" -d "ip=0.0.0.0" -X POST
    def post(self):
        args = parser.parse_args()
        n = args['name']
        t = args['token']
        if database.oauth.read_token(n, t):
            f = args['fqdn']
            i = args['ip']
            dn.add_address(f, i)
            return {'status': 'ok'}

        return {'status': "error"}

class DnsName(Resource):
    # curl http://172.31.1.5:5001/dns/name/narek.clim.test -d "name=Narek" -d "token=87da83fe-a7d5-11ec-a4ac-000c298d0891" -X DELETE
    def delete(self, fqdn):
        args = parser.parse_args()
        n = args["name"]
        t = args["token"]
        if database.oauth.read_token(n, t):
            dn.clear_address(fqdn)
            return {'status': 'ok'}

        return {'status': 'error'}

    # curl http://172.31.1.5:5001/dns/name/narek.clim.test -d "name=Narek" -d "token=87da83fe-a7d5-11ec-a4ac-000c298d0891" -d "ip=192.168.1.20" -X PUT
    def put(self, fqdn):
        args = parser.parse_args()
        n = args["name"]
        t = args["token"]
        if database.oauth.read_token(n, t):
            i = args['ip']
            dn.update_address(fqdn, i)
            return {'status': 'ok'}

        return {'status': 'error'}

    # curl http://172.31.1.5:5001/dns/name/narek.clim.test -d "name=Narek" -d "token=87da83fe-a7d5-11ec-a4ac-000c298d0891" -X GET
    def get(self, fqdn):
        args = parser.parse_args()
        n = args["name"]
        t = args["token"]
        if database.oauth.read_token(n, t):
            return dn.check_address(fqdn)

        return {'status': 'error'}

api.add_resource(DnsNew, '/dns/new')
api.add_resource(DnsName, '/dns/name/<fqdn>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
