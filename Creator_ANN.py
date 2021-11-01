#Rede Neural
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import linear_model
from math import sqrt
import pandas as pd
import numpy as np
import pickle

#csv file with all cases and consumption results
csv = 'C:/Users/LabEEE_3-7/Desktop/Tiago/resultados_completo.csv'
#csv file to predict IFSC consumption
csv_ifsc = 'C:/Users/LabEEE_3-7/Desktop/Tiago/IFSC.csv'
dataframe = pd.read_csv(csv)
ifsc = pd.read_csv(csv_ifsc)
#loc variables in dataframe
X = dataframe.loc[:, ['TipoCobertura', 'TipoParede', 'AbsortanciaCobertura', 'AbsortanciaParede','FatorSolar',  'TransmitanciaVidri', 'DPI', 'Turno', 'ocupacao', 'Sombreamento',
'SistemaClimatizacao', 'COP/IDRS',' CDH']].copy()

#loc outputs in dataframe
z = dataframe.loc[:, ['Output']].copy()
#Encode varibles to work with qualitative variables, converting to dummies (0 and 1)
X_encoded = pd.get_dummies(X, columns = ['Turno', 'SistemaClimatizacao'])
print(X_encoded)


y = np.ravel(z)
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size = 0.2, train_size = 0.8, random_state = 2101)


scaler = preprocessing.StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
x_ifsc_scaled = scaler.transform(ifsc)


'''
#Prameter grid to search best parameters to ANN run
param_grid = [
    {'alpha': [1e-05, 1e-04, 1e-03],
     'hidden_layer_sizes': [(19,),(20,),(21,)],
    'learning_rate_init': [1e-03, 1e-02, 1e-01, 1]},
]

optimal_params = GridSearchCV(
    ANN,
    param_grid,
    cv = 3,
    scoring = 'neg_root_mean_squared_error',
    verbose=2
 )

optimal_params.fit(X_train_scaled, y_train)
print(optimal_params.best_params_)
'''

#Create the ANN model with parameters from grid search
#ALWAYS REMEMBER TO CHECK THE PARAMETERS BEFORE RUN THE ANN MODEL
ANN = MLPRegressor(random_state = 2101, alpha = 0.0001, hidden_layer_sizes = (21), learning_rate_init = 0.01)
ANN.fit(X_train_scaled, y_train)
y_pred = ANN.predict(X_test_scaled)
ifsc_pred = ANN.predict(x_ifsc_scaled)
print(ifsc_pred)



#Save model
filename = 'modelo_ANN.sav'
pickle.dump(ANN, open(filename, 'wb'))

# The mean squared error
print('Mean squared error: %.2f'
      % mean_squared_error(y_test, y_pred))
# The root mean squared error
print('Root mean squared error: %.2f'
      % sqrt(mean_squared_error(y_test, y_pred)))
# The mean absolute error
print('Mean absolute error: %.2f'
      % (mean_absolute_error(y_test, y_pred)))
# The coefficient of determination
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))
