import numpy as np
import pandas as pd
import pickle
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder

def main():
    input_data_file = "../dataset/2.0_cases_cleaned.csv.gz"
    data = pd.read_csv(input_data_file)
    to_encode = ['sex', 'province', 'country', 'outcome']
    le = LabelEncoder()
    for i in range(len(to_encode)):
        data[to_encode[i]] = le.fit_transform(data[to_encode[i]].astype(str))    
    target = pd.Series(data['outcome'].to_numpy())        
    
    X_train_inputfile = "../dataset/2.1_X_train.csv.gz"
    X_valid_inputfile = "../dataset/2.1_X_valid.csv.gz"
    y_train_inputfile = "../dataset/2.1_y_train.csv.gz"
    y_valid_inputfile = "../dataset/2.1_y_valid.csv.gz"

    X_train = pd.read_csv(X_train_inputfile)
    X_valid = pd.read_csv(X_valid_inputfile)
    y_train = pd.read_csv(y_train_inputfile).transpose().values[0]
    y_valid = pd.read_csv(y_valid_inputfile).transpose().values[0]

    # classify with ADABoost
    ada_model = make_pipeline(
        AdaBoostClassifier(
            n_estimators = 20, 
            learning_rate = 0.8, 
            algorithm = 'SAMME'
        )
    )
    ada_model.fit(X_train, y_train)
    
    print("Validation score (ADA, train):", ada_model.score(X_train, y_train))
    print("Validation score (ADA, test):", ada_model.score(X_valid, y_valid))
    
    scores = cross_val_score(ada_model, data, target, cv=5)
    print("Cross validation avg score (ADA): %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    
    

if __name__ == '__main__':
    main()