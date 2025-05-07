
from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

def st_rmd_cm(clinker, gypsum, limestone, trass, finetrass, persen_finetrass, LOI_target, SO3_target, BTL_target):
    Data = np.array([
        [clinker[0], gypsum[0], limestone[0], trass[0]],
        [clinker[1], gypsum[1], limestone[1], trass[1]],
        [clinker[2], gypsum[2], limestone[2], trass[2]],
        [1, 1, 1, 1]
    ])
    invers_data = np.linalg.inv(Data)
    pengali_finetrass = persen_finetrass / 100
    target = np.array([
        LOI_target - finetrass[0] * pengali_finetrass,
        SO3_target - finetrass[1] * pengali_finetrass,
        BTL_target - finetrass[2] * pengali_finetrass,
        1 - pengali_finetrass
    ])
    komposisi_rawmix = np.dot(invers_data, target)
    result = [round(val * 100, 2) for val in komposisi_rawmix]
    result.append(round(persen_finetrass, 2))
    return result

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    def parse_input(name):
        return list(map(float, request.form[name].split(',')))

    clinker = parse_input('clinker')
    gypsum = parse_input('gypsum')
    limestone = parse_input('limestone')
    trass = parse_input('trass')
    finetrass = parse_input('finetrass')
    persen_finetrass = float(request.form['persen_finetrass'])
    LOI_target = float(request.form['LOI_target'])
    SO3_target = float(request.form['SO3_target'])
    BTL_target = float(request.form['BTL_target'])

    result = st_rmd_cm(clinker, gypsum, limestone, trass, finetrass,
                       persen_finetrass, LOI_target, SO3_target, BTL_target)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
