from flask import Flask, redirect, render_template, request, make_response, url_for
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic
from config import CONFIG
import uuid
import database as db
import dnszone as dns
import datetime

now = str(datetime.datetime.now())[:-7]

dns = dns.DnsZone("clim.test", "127.0.0.1")
id = str(uuid.uuid1())
user_id = ""
user_name = ""

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'your secret string', report_errors=False)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout', methods=["GET", 'POST'])
def logout():
    return redirect(url_for('index'))

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    global user_id, user_name
    # We need response object for the WerkzeugAdapter.
    response = make_response()
    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
            user_name += result.user.name
            user_id += result.user.id

            if db.oauth.read_id(result.user.id):
                return render_template('login2.html', result=result)

            db.oauth.create(provider_name, result.user.name, result.user.id, result.user.email, id, None, now, None, None, None)

        # The rest happens inside the template.
        return render_template('login.html', result=result)

    # Don't forget to return the response.
    return response

@app.route('/dns/choose', methods=["GET", "POST"])
def choose():
    choice = request.form['choose']
    if choice == "create":
        return render_template('create_record.html')
    elif choice == "change":
        return render_template('change_record.html')
    elif choice == "delete":
        return render_template('delete_record.html')

@app.route('/dns/created', methods=['POST', 'GET'])
def created():
    fqdn_create = request.form['fqdn']
    ip_create = request.form['ip']

    if db.oauth.read_fqdn(user_id, fqdn_create):
        return render_template('record_exist.html', fqdn=fqdn_create)
    
    elif not db.oauth.read_fqdn(user_id, fqdn_create):
        try:
            dns.add_address(fqdn_create, ip_create)
            db.oauth.update_fqdn(user_id, fqdn_create)
            db.oauth.update_time_creation_record(user_id, now)
            return render_template('record_created.html', fqdn=fqdn_create, ip=ip_create)
        except:
            return render_template("forgot_ip.html")
    
    return render_template('error.html')
    
@app.route('/dns/changed', methods=['GET', 'POST'])
def changed():
    fqdn_change = request.form['fqdn']
    ip_change = request.form['ip']
    
    if db.oauth.read_fqdn(user_id, fqdn_change):
        db.oauth.update_time_update_record(user_id, now)
        dns.update_address(fqdn_change, ip_change)
        return render_template('record_changed.html', fqdn=fqdn_change, ip=ip_change)

    elif not db.oauth.read_fqdn(user_id, fqdn_change):
        return render_template('no_record.html', fqdn=fqdn_change)

    return render_template('error.html')

@app.route('/dns/deleted', methods=['GET', 'POST'])
def deleted():
    fqdn_delete = request.form['fqdn']
    
    if not db.oauth.read_fqdn(user_id, fqdn_delete):
            return render_template('no_record.html', fqdn=fqdn_delete)

    elif db.oauth.read_fqdn(user_id, fqdn_delete):
        dns.clear_address(fqdn_delete)
        db.oauth.delete_fqdn(user_id, fqdn_delete)
        db.oauth.update_time_deleted_record(user_id, now)
        return render_template('record_deleted.html', fqdn=fqdn_delete)


    return render_template('error.html')

# Run the app on port 5000 on all interfaces, accepting only HTTPS connections
if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host='172.31.1.5', port=5000)