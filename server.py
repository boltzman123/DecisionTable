from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)


def wald_criteria(data, action_matrix):
   min_values = np.min(data, axis=1)
   return action_matrix[np.argmax(min_values)][0]

def maxiMax_criteria(data, action_matrix):
    max_values = np.max(data, axis=1)
    return action_matrix[np.argmax(max_values)][0]

def hurwicz_criteria(data, alpha, action_matrix):
    min_values = np.min(data, axis=1)
    max_values = np.max(data, axis=1)
    hurwicz = alpha*min_values + (1 - alpha)*max_values
    return action_matrix[np.argmax(hurwicz)][0]

def laplace_criteria(data, action_matrix):
    means = np.mean(data, axis=1)
    return action_matrix[np.argmax(means)][0]

def savage_criteria(data, action_matrix):
    max_values = np.max(data, axis=0)
    data = np.abs(data - max_values)
    max_values = np.max(data, axis=1)   
    return action_matrix[np.argmin(max_values)][0]

    



@app.route('/api/submit-table', methods=['POST'])
def submit_table():
    try:
        data = request.get_json()
        matrix = np.array(data["tableData"])
        alpha = data["alpha"]
        
        action_matrix = matrix[1:]
        data = np.array(matrix)
        dataNew = data[1:, 1:].astype("int")
        
        wald = wald_criteria(dataNew, action_matrix)
        maxiMax = maxiMax_criteria(dataNew, action_matrix)
        hurwicz = hurwicz_criteria(dataNew, alpha, action_matrix)
        laplace = laplace_criteria(dataNew, action_matrix)
        savage = savage_criteria(dataNew, action_matrix)
        
        return jsonify({'Wald Criteria': f"{wald}",
                        'MaxiMax Criteria': f"{maxiMax}",
                        'Hurwicz Criteria': f"{hurwicz}",
                        'Laplace Criteria': f"{laplace}",
                        'Savage Criteria': f"{savage}"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
