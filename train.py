from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np
from sklearn.impute import SimpleImputer

# fetch dataset 
heart_disease = fetch_ucirepo(id=45) 
#data = pd.read_csv('data\\heart.csv')
  
# data (as pandas dataframes) 
X = heart_disease.data.features
y = heart_disease.data.targets

# Binarize the target variable
y = (y > 0).astype(int)

# Handle missing values by imputing with the mean
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = LogisticRegression(max_iter=10000)
model.fit(X_train, y_train)

# Save the model to a file
joblib.dump(model, 'model.joblib')

print("Model trained and saved as model.joblib")