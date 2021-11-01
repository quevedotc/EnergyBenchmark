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


#loc variables in dataframe. Full threshold
X = dataframe.loc[:, ['TipoCobertura', 'TipoParede', 'AbsortanciaCobertura', 'AbsortanciaParede', 'FatorSolar',  'TransmitanciaVidri', 'DPI', 'Turno', 'ocupacao', 'Sombreamento',
'SistemaClimatizacao', 'COP/IDRS',' CDH']].copy()
z = dataframe.loc[:, ['Output']].copy()

#Loc variables to threshold 0.05 (drop "abs cobertura")
X_005 = dataframe.loc[:, ['TipoCobertura', 'TipoParede', 'AbsortanciaParede', 'FatorSolar',  'TransmitanciaVidri', 'DPI', 'Turno', 'ocupacao', 'Sombreamento',
'SistemaClimatizacao', 'COP/IDRS',' CDH']].copy()

#Loc variables to threshold 0.025 (drop 4 variables: abs cobertura, tipo cobertura, transmitancia vidro, fator solar)
X_025 = dataframe.loc[:, ['TipoParede', 'AbsortanciaParede', 'DPI', 'Turno', 'ocupacao', 'Sombreamento',
'SistemaClimatizacao', 'COP/IDRS',' CDH']].copy()

#Encode varibles to work with qualitative variables, converting to dummies (0 and 1)
#REMEMBER TO CHANGE THE X (X, X_025, X_005) BEFORE RUN. EACH X HAVE UNIQUE BEST PARAMETERS, NEED TO RUN SEARCHGRID FOR EACH X
X_encoded = pd.get_dummies(X_025, columns = ['Turno', 'SistemaClimatizacao'])
print(X_encoded)


y = np.ravel(z)

X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size = 0.2, train_size = 0.8, random_state = 2101)

'''
#Prameter grid to search best parameters to SVM run
print(y)
print(ifsc)

param_grid = [
    {'C': [1,10,100], 'epsilon': [1e-09,1e-08, 1e-07, 1e-06, 1e-05,1e-04], 'kernel': ['linear', 'poly', 'rbf'],'degree': [1,2,3,4,5]},
]

optimal_params = GridSearchCV(
    SVR(),
    param_grid,
    cv = 5,
    scoring = 'neg_root_mean_squared_error',
    verbose=2
 )

optimal_params.fit(X_train_scaled, y_train)
print(optimal_params.best_params_)
'''


#Scaling to run SVM models
scaler = preprocessing.StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
#x_ifsc_scaled = scaler.transform(ifsc)


#Create the SVM model with parameters from grid search
#ALWAYS REMEMBER TO CHECK THE PARAMETERS BEFORE RUN THE SVM MODEL

svm = SVR(kernel='poly', C=100, epsilon = 1e-05, degree = 5)

svm.fit(X_train_scaled, y_train)

y_pred_svm = svm.predict(X_test_scaled)


#predict ENergy from Real case
#y_pred_ifsc = svm.predict(x_ifsc_scaled)


#Save model
filename = 'SVM_025.sav'
pickle.dump(svm, open(filename, 'wb'))


# The mean squared error
print('Mean squared error svm: %.2f'
      % mean_squared_error(y_test, y_pred_svm))

# The root mean squared error
print('Root mean squared error svm: %.2f'
      % sqrt(mean_squared_error(y_test, y_pred_svm)))

# The mean absolute error
print('Mean absolute error svm: %.2f'
      % (mean_absolute_error(y_test, y_pred_svm)))


# The coefficient of determination
print('Coefficient of determination svm: %.2f'
      % r2_score(y_pred_svm, y_test))
print('y_test:', (y_pred_svm))
#print('consumo por m² iFSC:', (y_pred_ifsc))
