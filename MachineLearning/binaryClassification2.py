import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import seaborn as sns
from sklearn import metrics

sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

def test():
    data = pd.read_csv('patientData.csv',header = 0)
    data = data.dropna()
    dataLength = data.shape[0]
    
    print(data.shape)
    print(list(data.columns))
    
    #print(data['HEARTFAILURE'].value_counts())
    #sns.countplot(x= 'HEARTFAILURE',data=data,palette='hls')
    '''
    count_no_fail = len(data[data['HEARTFAILURE']==0])
    count_fail = len(data[data['HEARTFAILURE']==1])
    pct_of_no_fail = count_no_fail/(count_no_fail+count_fail)
    print("percentage of no subscription is", pct_of_no_fail*100)
    pct_of_fail = count_fail/(count_no_fail+count_fail)
    print("percentage of subscription", pct_of_fail*100)
    '''
    
    import statsmodels.api as sm
    
    print(data.groupby('HEARTFAILURE').mean())
    
    #logit_model = sm.Logit(y,X)
    
    #matplotlib inline
    
    
    '''
    pd.crosstab(data.SMOKERLAST5YRS,data.HEARTFAILURE).plot(kind ='bar')
    plt.title('smoke and heartfailure')
    plt.xlabel('smoke')
    plt.ylabel("failure")
    plt.savefig('smoke')
    
    data.PALPITATIONSPERDAY.hist()
    plt.title('Histogram of palp')
    plt.xlabel('palp')
    plt.ylabel('failure')
    plt.savefig('palpitations')
    '''
    
    cat_vars = ['SEX','FAMILYHISTORY','SMOKERLAST5YRS']
    for var in cat_vars:
        cat_list = 'var'+'_'+var
        cat_list = pd.get_dummies(data[var],prefix=var)
        data2 = data.join(cat_list)
        data = data2
    cat_vars = ['SEX','FAMILYHISTORY','SMOKERLAST5YRS']
    data_vars= data.columns.values.tolist()
    to_keep = [i for i in data_vars if i not in cat_vars]
    
    dataFinal = data[to_keep]
    
    X = dataFinal.loc[:,dataFinal.columns != 'HEARTFAILURE']
    y = dataFinal.loc[:,dataFinal.columns == 'HEARTFAILURE']
    
    from imblearn.over_sampling import SMOTE
    
    os = SMOTE(random_state =0)
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size =0.15,random_state =0)
    columns = X_train.columns
    
    os_data_X,os_data_y = os.fit_sample(X_train,y_train)
    os_data_X = pd.DataFrame(data = os_data_X,columns = columns)
    os_data_y = pd.DataFrame(data = os_data_y,columns = ['HEARTFAILURE'])
    
    print("length of oversampled data is ",len(os_data_X))
    print("Number of no subscription in oversampled data",len(os_data_y[os_data_y['HEARTFAILURE']==0]))
    print("Number of subscription",len(os_data_y[os_data_y['HEARTFAILURE']==1]))
    print("Proportion of no subscription data in oversampled data is ",len(os_data_y[os_data_y['HEARTFAILURE']==0])/len(os_data_X))
    print("Proportion of subscription data in oversampled data is ",len(os_data_y[os_data_y['HEARTFAILURE']==1])/len(os_data_X))
    data_final_vars = dataFinal.columns.values.tolist()
    
    y = ['HEARTFAILURE']
    X = [i for i in data_final_vars if i not in y]
    
    from sklearn.feature_selection import RFE
    
    logreg = LogisticRegression()
    rfe = RFE(logreg,2)
    rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
#    print(rfe.support_)
 #   print(rfe.ranking_)
  #  print(rfe.estimator_)
    
    
    col = ['PALPITATIONSPERDAY', 'BMI', 'AVGHEARTBEATSPERMIN', 'AGE', 'EXERCISEMINPERWEEK', 'SEX_F', 'SEX_M', 'FAMILYHISTORY_N', 'FAMILYHISTORY_Y', 'SMOKERLAST5YRS_N', 'SMOKERLAST5YRS_Y']
    #col = ['PALPITATIONSPERDAY', 'CHOLESTEROL', 'BMI', 'AVGHEARTBEATSPERMIN', 'AGE', 'EXERCISEMINPERWEEK', 'FAMILYHISTORY_N', 'FAMILYHISTORY_Y', 'SMOKERLAST5YRS_N', 'SMOKERLAST5YRS_Y']
    
    #col = ['BMI', 'SEX_M','SEX_F','AVGHEARTBEATSPERMIN', 'FAMILYHISTORY_N', 'AGE','FAMILYHISTORY_Y', 'SMOKERLAST5YRS_N', 'SMOKERLAST5YRS_Y']
    
    y = os_data_y['HEARTFAILURE']
    X = os_data_X[col] 
    final = sm.Logit(y,X)
    result = final.fit()
    print(result.summary2())
    
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size =0.20,random_state =0)
    
    logreg = LogisticRegression()
    logreg.fit(X_train,y_train)
    y_pred = logreg.predict(X_test)
    print('Accuracy of logistic regression classifier on test set:', format(logreg.score(X, y)))
    print(y_pred)
def predict(x):
    data = pd.read_csv('patientTraining.csv',header = 0)
    data = data.dropna()
    cat_vars = ['SEX','FAMILYHISTORY','SMOKERLAST5YRS']
    for var in cat_vars:
        cat_list = 'var'+'_'+var
        cat_list = pd.get_dummies(data[var],prefix=var)
        data2 = data.join(cat_list)
        data = data2
    cat_vars = ['SEX','FAMILYHISTORY','SMOKERLAST5YRS']
    data_vars= data.columns.values.tolist()
    to_keep = [i for i in data_vars if i not in cat_vars]
    
    dataFinal = data[to_keep]
    
    X = dataFinal.loc[:,dataFinal.columns != 'HEARTFAILURE']
    y = dataFinal.loc[:,dataFinal.columns == 'HEARTFAILURE']
    
    from imblearn.over_sampling import SMOTE
    
    os = SMOTE(sampling_strategy="minority", random_state =0)
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size =0.15,random_state =0)
    columns = X_train.columns
    
    os_data_X,os_data_y = os.fit_resample(X_train,y_train)
    os_data_X = pd.DataFrame(data = os_data_X,columns = columns)
    os_data_y = pd.DataFrame(data = os_data_y,columns = ['HEARTFAILURE'])
    col = ['PALPITATIONSPERDAY', 'BMI', 'AVGHEARTBEATSPERMIN', 'AGE', 'EXERCISEMINPERWEEK', 'SEX_F', 'SEX_M', 'FAMILYHISTORY_N', 'FAMILYHISTORY_Y', 'SMOKERLAST5YRS_N', 'SMOKERLAST5YRS_Y']
    #col = ['PALPITATIONSPERDAY', 'CHOLESTEROL', 'BMI', 'AVGHEARTBEATSPERMIN', 'AGE', 'EXERCISEMINPERWEEK', 'FAMILYHISTORY_N', 'FAMILYHISTORY_Y', 'SMOKERLAST5YRS_N', 'SMOKERLAST5YRS_Y']
    
    #col = ['PALPITATIONSPERDAY', 'CHOLESTEROL', 'BMI', 'AVGHEARTBEATSPERMIN', 'EXERCISEMINPERWEEK', 'FAMILYHISTORY_N', 'FAMILYHISTORY_Y', 'SMOKERLAST5YRS_N', 'SMOKERLAST5YRS_Y']
    
    y = os_data_y['HEARTFAILURE']
    X = os_data_X[col]
    logreg = LogisticRegression()
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size =0.20,random_state =0)

    logreg.fit(X_train,y_train)
    y_pred = logreg.predict(X_test)
    return format(logreg.score(X_train, y_train))
