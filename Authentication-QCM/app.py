# -*- coding:utf-8 -*-
from flask import Flask, request, Response
from globalfunction import *
from conf import *
app = Flask(__name__)

# Set the secret key to some random bytes.
app.secret_key = SECRET_KEY_APP
app.config['SERVER_NAME'] = "127.0.0.1:5001"

@app.route('/authentication', methods=['GET','POST'])
def authentication():

    if request.method == 'POST':
        print(request.form.get('secret_shared_key'))
        print(request.form.get('username'))
        if request.form.get('secret_shared_key') == SECRET_SHARED_KEY and not request.form.get('username') is None:
            list_info_user = request_session(request.form.get('username'))
            print(list_info_user)

            if not list_info_user :
                xml = '<result>False</<result>'
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
                print(xml)
                return Response(xml, mimetype='text/xml')

        xml = '<result>False</result>'
        return Response(xml, mimetype='text/xml')

    xml = '<result>False</result>'
    return Response(xml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True)
