# -*- coding:utf-8 -*-
from flask import Flask, request
from globalfunction import *
from conf import *
app = Flask(__name__)

# Set the secret key to some random bytes.
app.secret_key = SECRET_KEY_APP

@app.route('/push_qcm', methods=['POST'])
def push_qcm():

    if request.method == 'POST':

        if request.form.get('secret_shared_key') == SECRET_SHARED_KEY and not request.form.get('xml_correction') is None and not request.form.get('name_qcm') is None:

            path_qcm = PATH_QCM_CORRECTION + request.form.get('name_qcm') + ".xml"
            file = open(path_qcm, "w")
            file.write(request.form.get('xml_correction'))
            file.close()

            return "True", 200

        return "False", 500

    return "False", 405


@app.route('/delete_qcm', methods=['POST'])
def delete_qcm():
    if request.method == 'POST':

        if request.form.get('secret_shared_key') == SECRET_SHARED_KEY and not request.form.get('name_qcm') is None:

            name_qcm = request.form.get('name_qcm') + ".xml"
            remove_file(PATH_QCM_CORRECTION, name_qcm)

            return "True", 200

        return "False", 500

    return "False", 405




@app.route('/correction_qcm', methods=['GET','POST'])
def corrector():
    if request.method == 'POST':

        if request.args.get('ref') is None:
            return redirect("http://localhost:5000/home")

        ## Correction
        note = 0
        qcm = request.args['ref'] + ".xml"
        path_qcm = PATH_QCM_CORRECTION + qcm
        tree = etree.parse(path_qcm)

        for number in tree.xpath("/QCMCorrection/correction/question/@num"):
            radio_value = "question_" + number + "_awswer"
            #print(radio_value)
            xurl = "/QCMCorrection/correction/question[@num=" + number + "]/@id"
            if request.form.get(radio_value) == tree.xpath(xurl)[0]:
                note += 1

        html = "<h3>Tu as " + str(note) + " sur " + str(number) +"<h3>Go <a href='http://" + ADDRESS_SERVER_QCM + ":" + PORT_SERVER_QCM + "/home'>home</a>"
        return html

    return "False", 405

if __name__ == '__main__':
    app.run(host=BIND_ADDRESS, port=BIND_PORT, debug=True)
