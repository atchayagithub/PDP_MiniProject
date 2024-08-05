from flask import Flask, render_template, request
from reports import *

app = Flask(__name__)


@app.route("/")
def manager_home():
    return render_template('manager_home.html')

@app.route("/generate_data", methods=["POST", "GET"])
def generate_data():

    id_no = request.form["student_id"]
    option = request.form["report"]
    report = Report(id_no)
    if(option == "simple"):
        generated_txt = report.generate()
    elif(option == "detailed"):
        report.change_stratergy(Complete_Details)
        generated_txt = report.generate()
    else:
        report.change_stratergy(Every_Details)
        generated_txt = report.generate()

    return render_template("display_generated_report.html", generated_txt=generated_txt)


if(__name__ == "__main__"):
    app.run(debug=True)