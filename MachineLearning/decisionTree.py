from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.tree import DecisionTreeClassifier
from random import shuffle,randint
from math import floor,log2
import numpy as np
from sklearn.tree import export_graphviz
from collections import Counter
#split the data into training, validation and test sets randomly using shuffle

trainPercent = .70

def split(data):
    num = len(data)
    
    trainlen = round(num* trainPercent)
    testlen = floor((num -trainlen)/2)
    vallen = num - trainlen - testlen
    
    train = []
    test = []
    val = []
    
    index = list(range(len(data)))
    shuffle(index)
    for i in index: 
        if (len(train)<trainlen):
            train.append(data[i])
        elif (len(val)<vallen):
            val.append(data[i])
        else:
            test.append(data[i])
        
    return np.array(train),np.array(val),np.array(test)
    
#Q2 part a
def load_data():
    
    #loading in file
    allData = open ("patientdata.txt")
    data = allData.readlines()
    allData.close()

    cv = CV()
    
    data = cv.fit_transform(data)
    fitted = data.toarray()
    fitted = np.column_stack((fitted,labels))    
    
    
    training,validation,test = split(fitted)
    trainingLabel = training[:,-1]
    training = training[:,:-1]
    validationLabel = validation[:,-1]
    validation = validation[:,:-1]
    testLabel = test[:,-1]
    test = test[:,:-1]
    return training,validation,test,trainingLabel,validationLabel,testLabel, cv

#for loop modifier, used to control various depth in model creation
def modifier(i):
    return i*450+40

#returns the accuracy of a certain model based on validation data
def accuracyVal(model, valdata, vallabel):
    # predictions from model
    pred = model.predict(valdata)
    total = len(pred)
    correct = 0
    for i in range(len(pred)):
        if vallabel[i] == pred[i]:
            correct += 1
    return float(correct)/total



#returns the model based on various criterion
def model(crit, max_depth, traindata, trainlabel):
    

    model = DecisionTreeClassifier(criterion=crit, max_depth=max_depth)
    model = model.fit(traindata, trainlabel)
    return model

def select_model():
    training,validation,test,trainingLabel,validationLabel,testLabel,cv = load_data()
    
    giniAccuracy = []
    #gini split
    for i in range(5):
        depth = modifier(i)
        tree = model('gini',depth, training,trainingLabel)
        accuracy = accuracyVal(tree,validation,validationLabel)
        giniAccuracy.append((accuracy, depth))
        # use gini split criteria
       
    #info gain
    infoAccuracy = []
    for i in range(5):
        depth = modifier(i)
        tree = model('gini',depth, training,trainingLabel)
        accuracy = accuracyVal(tree,validation,validationLabel)
        infoAccuracy.append((accuracy, depth))
    
    for i in giniAccuracy:
        print("Gini with depth",i[1],"has accuracy",i[0])
    for i in infoAccuracy:
        print("Information gain with depth", i[1],"has accuracy", i[0])

    tree = model('gini',1390,training,trainingLabel)
    f = open("visualization.dot", "w")
    export_graphviz(max_depth = 2,out_file = "visualization.dot",decision_tree = tree)
    f.close()


#Gini with depth 1390 has accuracy 0.7959183673469388 highest
    

        
def entropy(real,fake):
    total = real+fake
    return -((real/total) * log2((real/total)) + (fake/total) * log2((fake/total)))

def pickword(a):
    words = []
    for i in range(7):
        words.append(a.pop(randint(0,len(a)-1)))
    return words

def count_split(data, label, keyword,ind):
    inreal = 0
    infake = 0
    noreal = 0
    nofake = 0
    
    for i in range(len(data)):
        if (int(data[i,ind])==1): #word in headline
            if (int(label[i])==1):
                inreal +=1 #real
            else:
                infake +=1 #fake
        else: #word not in head line
            if (int(label[i])==1):
                noreal +=1 #real
            else:
                nofake +=1 #fake
    return inreal,infake,noreal,nofake

def info_gain(data,label,keyword,keywordind):
    splitcount = Counter(label)
    
    #the split, in headline real, in healine,fake, not in head real, not in head fake
    inReal,inFake,noReal,noFake = count_split(data,label,keyword,keywordind)
    headlineWord = inReal+inFake
    headlineNoWord = noReal+noFake
    
    #entropy of data(whole training set)
    preSplitEntropy = entropy(splitcount[1],splitcount[0])

    #conditional entropy of word in headline
    inHeadlineEntropy = entropy(inReal,inFake)
    
    #conditional entropy of word no in headline
    notInHeadlineEntropy = entropy(noReal,noFake)
    
    #conditional entropy
    total= (splitcount[0]+splitcount[1])
    inHeadlineRatio = headlineWord/total
    notInHeadlineRatio = headlineNoWord/total
    postSplitEntropy = inHeadlineRatio*inHeadlineEntropy + \
    notInHeadlineRatio*notInHeadlineEntropy
    
    return  preSplitEntropy - postSplitEntropy
    
def compute_information_gain():
    training,validation,test,trainingLabel,validationLabel,testLabel,cv =\
    load_data()
     
    
    print("--Top layer from graph--")
    keyword = cv.get_feature_names()[5143]
    result = info_gain(training,trainingLabel,keyword, 5143)
    print("'",keyword,"'", "has information gain of", result)
    
    
    
    print("--a few top words--")
    #keywords = pickword(cv.get_feature_names().copy())
    keywords =['trump','donald','to','in','of','for','hillary']
    for s in keywords:
        result = info_gain(training,trainingLabel,str(s),cv.vocabulary_.get(s))
        
        print("'",s,"'", "has information gain of", result)
        


    
    
    
    
    
    
    
    
    