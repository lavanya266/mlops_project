from flask import Flask, render_template, request
from model_func import preprocess_scale, model_load
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        y = ''
        task_content = request.form['content']
        if task_content != '':
            X = task_content.split(',')
            X = [float(i) for i in X]
            if len(X) == 5:
                model = model_load("model/model.pkl")
                y = model.predict(preprocess_scale([X]))
        return render_template('index.html', result=y)
    else:
        return render_template('index.html', result='')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
