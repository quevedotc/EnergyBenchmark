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



print(ifsc)
y = np.ravel(z)
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size = 0.2, train_size = 0.8, random_state = 2101)
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)

#save regression
filename = 'modelo_SregressionV2.sav'
pickle.dump(regr, open(filename, 'wb'))

y_pred_regr = regr.predict(X_test)
ifsc_regr = regr.predict(ifsc)
# The mean squared error
print('Mean squared error: %.2f'
      % mean_squared_error(y_test, y_pred_regr))
# The root mean squared error
print('Root mean squared error: %.2f'
      % sqrt(mean_squared_error(y_test, y_pred_regr)))
# The mean absolute error
print('Mean absolute error: %.2f'
      % (mean_absolute_error(y_test, y_pred_regr)))
# The coefficient of determination
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred_regr))

print("R^2: {}".format(regr.score(X_test, y_test)))
print("Coeficientes: ", regr.coef_)
print(y_pred_regr)
print(ifsc_regr)
