import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# df = pd.read_csv("data.csv")
# df = df.dropna()
# df = df.iloc[:, 1:]
# df.to_csv('cleanedDataset.csv', index = False, header = True)

df = pd.read_csv("cleanedDataset.csv")

headers = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "ApplicantIncome", 
           "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area"]

X_test = pd.DataFrame(np.array([["Male", "Yes", 1, "Graduate", "No", 4583, 1508.0, 128.0, 360.0, 1.0, "Rural"]]),
                      columns=headers) #no

categoricalHeaders = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"]

X = df.iloc[:, :-1]
columnTransformer = ColumnTransformer([('encoder', OneHotEncoder(), categoricalHeaders)], remainder='passthrough')
X = np.array(columnTransformer.fit_transform(X))
X_test = np.array(columnTransformer.transform(X_test))

y = df["Loan_Status"].map({'Y': 1, 'N': 0})

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)
X_test = sc.transform(X_test)

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X, y)

y_pred = classifier.predict(X_test)
print(y_pred)
