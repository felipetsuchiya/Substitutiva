from flask import Flask, render_template, request
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    classifier_name = request.form['classifier']
    param1 = float(request.form.get('param1', 5.0))
    param2 = int(request.form.get('param2', 10))
    param3 = int(request.form.get('param3', 0))

    X, y = np.random.rand(100, 2), np.random.choice([0, 1], size=100)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   
    if classifier_name == 'KNN':
        clf = KNeighborsClassifier(n_neighbors=param2)
    elif classifier_name == 'SVM':
        clf = SVC(C=param1)
    elif classifier_name == 'MLP':
        clf = MLPClassifier(hidden_layer_sizes=(param2, param3), max_iter=1000)
    elif classifier_name == 'DT':
        clf = DecisionTreeClassifier(max_depth=param2)
    elif classifier_name == 'RF':
        clf = RandomForestClassifier(n_estimators=param2)
    else:
        return "Invalid classifier selected"

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred, average='macro')

    conf_matrix = metrics.confusion_matrix(y_test, y_pred)
 
    plt.figure(figsize=(5, 5))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.getvalue()).decode()

    return render_template('result.html', classifier=classifier_name, accuracy=accuracy, f1_score=f1_score, img_data=img_data)

if __name__ == '__main__':
    app.run(debug=True)
