from model_func import mlflow_run, model_save
import mlflow
from sklearn.linear_model import SGDRegressor
from sklearn.svm import SVR

'''
The following 3 lines may be used is one does not want to run mlflow server. In such a case the code will run correctly, 
but MLFlow UI will not be available
'''
#import os
#os.makedirs("/mlruns", exist_ok=True)
#mlflow.set_tracking_uri("file:///mlruns")

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Integraion experiment")

#Defining hyperparameters

sgd_params = {
    "max_iter": 1000,
    "loss": "squared_error",
    "penalty": "l2",
    "eta0": 0.01,
    "tol": 1e-3,
    "random_state": 42,
}

svr_params = {
    "kernel":'rbf',
    "degree":3,
}

deg = [2, 3, 4, 5]

scores = list()
infos = list()

sgd = SGDRegressor(**sgd_params)

info_sgd, r2 = mlflow_run(sgd, "sgd_regressor", "model/data/elementary.csv", sgd_params)
scores.append(r2)
infos.append(info_sgd)

for i in deg:
    svr_params["degree"] = i
    svr = SVR(**svr_params)
    info_svr, r2 = mlflow_run(svr, "svr_regressor with degree {}".format(str(i)), "model/data/elementary.csv", svr_params)
    scores.append(r2)
    infos.append(info_svr)

#getting uri of the best model and saving it
uri_of_model = infos[scores.index(max(scores))].model_uri

loaded_model = mlflow.pyfunc.load_model(uri_of_model)

model_save(loaded_model, "model/model.pkl")
