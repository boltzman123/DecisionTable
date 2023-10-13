from flask import Flask, jsonify, render_template, request
import numpy as np

app = Flask(__name__)

def wald_criteria(data, action_matrix):
    min_values = np.min(data, axis=1)
    return action_matrix[np.argmax(min_values)][0]

def maxiMax_criteria(data, action_matrix):
    max_values = np.max(data, axis=1)
    return action_matrix[np.argmax(max_values)][0]

def hurwicz_criteria(data, alpha, action_matrix):
    min_values = np.min(data, axis=1)
    max_values = np.max(data, axis=1)
    hurwicz = alpha * min_values + (1 - alpha) * max_values
    return action_matrix[np.argmax(hurwicz)][0]

def laplace_criteria(data, action_matrix):
    means = np.mean(data, axis=1)
    return action_matrix[np.argmax(means)][0]

def savage_criteria(data, action_matrix):
    max_values = np.max(data, axis=0)
    data = np.abs(data - max_values)
    max_values = np.max(data, axis=1)
    return action_matrix[np.argmin(max_values)][0]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json['tableData']
    alpha = float(request.json['alpha'])
    matrix = np.array(data)
    alpha = 0.5

    action_matrix = matrix[1:]
    data = np.array(matrix)
    data_new = data[1:, 1:].astype("int")

    wald = wald_criteria(data_new, action_matrix)
    maxiMax = maxiMax_criteria(data_new, action_matrix)
    hurwicz = hurwicz_criteria(data_new, alpha, action_matrix)
    laplace = laplace_criteria(data_new, action_matrix)
    savage = savage_criteria(data_new, action_matrix)

    result_data = {'Wald Criteria': f"{wald}",
                    'MaxiMax Criteria': f"{maxiMax}",
                    'Hurwicz Criteria': f"{hurwicz}",
                    'Laplace Criteria': f"{laplace}",
                    'Savage Criteria': f"{savage}"
                    }

    return jsonify(result_data)


if __name__ == "__main__":
    app.run(debug=True)
