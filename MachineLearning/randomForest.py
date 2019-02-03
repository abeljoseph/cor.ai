import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split


results_test = {}
results_train = {}
list_algos=[]

def prdict_date(algo_name,X_train,y_train,X_test,y_test,atype='',verbose=0):
    algo_name.fit(X_train, y_train)
    Y_pred = algo_name.predict(X_test)
    acc_train = round(algo_name.score(X_train, y_train) * 100, 2)
    acc_val = round(algo_name.score(X_test, y_test) * 100, 2)
    
    results_test[str(algo_name)[0:str(algo_name).find('(')]+'_'+str(atype)] = acc_val
    results_train[str(algo_name)[0:str(algo_name).find('(')]+'_'+str(atype)] = acc_train
    list_algos.append(str(algo_name)[0:str(algo_name).find('(')])
    if verbose ==0:
        print("acc train: " + str(acc_train))
        print("acc test: "+ str(acc_val))
    else:
        return Y_pred
def tester():   
    df = pd.read_csv('patientData.csv')
    cat_vars = ['SEX','FAMILYHISTORY','SMOKERLAST5YRS'] #dummy variables
    data = df
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
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size =0.10,random_state =0)
    random_forest = RandomForestClassifier(n_estimators=50, random_state = 0)
    return prdict_date(random_forest,X_train,y_train,X_test,y_test,1)

def MLmodule(d):
    pal = d['palpitations']
    bmi = d['bmi']
    bpm = d['heartRate']
    age = d['age']
    sexF = 1
    sexM = 0
    if (d["sex"] or d['sex'] =="True"):
        sexM,sexF = sexF,sexM
    activity = d['exercise']
    famN  = 1
    famY = 0
    if (d['family-history'] or d['family-history'] =="True"):
        famN,famY = famY,famN
    smokeN = 1
    smokeY = 0
    cho = d['cholesterol']
    if (d['smoker'] or d['smoker'] =="True"):
        smokeN,smokeY = smokeY,smokeN
    x = pd.DataFrame({'PALPITATIONSPERDAY':[pal],'BMI':[bmi],'CHOLESTEROL':[cho],
                      'AVGHEARTBEATSPERMIN':[bpm],'AGE':[age],
                      'EXERCISEMINPERWEEK':[activity], 'SEX_F':[sexF],
                      'SEX_M':[sexM],'FAMILYHISTORY_N':[famN],
                      'FAMILYHISTORY_Y':[famY],'SMOKERLAST5YRS_N':[smokeN],
                      'SMOKERLAST5YRS_Y':[smokeY]})
    return (forest(x)[0]==1)
def forest(x):
    
    
    
    df = pd.read_csv('patientTraining.csv')
    cat_vars = ['SEX','FAMILYHISTORY','SMOKERLAST5YRS'] #dummy variables
    data = df
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
    
    
    
    #X_train,X_test,y_train,y_test = train_test_split(X,y,test_size =0.10,random_state =0)
    random_forest = RandomForestClassifier(n_estimators=50, random_state = 0)
    return prdict_date(random_forest,X,y,x,[1],verbose = 1)