# -*- coding:utf-8 -*-
from flask import Flask, request, Response
from globalfunction import *
from conf import *
app = Flask(__name__)

# Set the secret key to some random bytes.
app.secret_key = SECRET_KEY_APP

@app.route('/authentication', methods=['POST'])
def authentication():

    if request.method == 'POST':

        if request.form.get('secret_shared_key') == SECRET_SHARED_KEY and not request.form.get('username') is None:

            list_info_user = request_session(request.form.get('username'))

            if not list_info_user :

                xml = '<util><result>False</result><info>L utilisateur n existe pas !</info></util>'
                return Response(xml, mimetype='text/xml')

            else :

                xml = "<util>"
                xml = xml + "<result>True</result>"
                xml = xml + "<nom>" + list_info_user[0] + "</nom>"
                xml = xml + "<grade>" + list_info_user[2] + "</grade>"
                xml = xml + "<formation>" + list_info_user[1] + "</formation>"
                xml = xml + "<listmatiere>"

                for matiere in list_info_user[3]:
                    xml = xml + "<matiere>" + matiere + "</matiere>"
                xml = xml + "</listmatiere>"
                xml = xml + "</util>"

                return Response(xml, mimetype='text/xml')

        xml = '<util><result>False</result><info>secret_shared_key not existe or username is None</info></util>'
        return Response(xml, mimetype='text/xml')

    xml = '<util><result>False</result><info>Is not a POST request</info></util>'
    return Response(xml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
