from django.shortcuts import render
from django.db import models
from django.http import HttpResponse
from .forms import UploadFileForm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

def pre(filename):
	dataset = pd.read_csv(filename)
	dataset.isnull().sum()
	d1 = dataset.iloc[:,1:178][dataset['y']==1]
	d2 = dataset.iloc[:,1:178][dataset['y']==2]
	d3 = dataset.iloc[:,1:178][dataset['y']==3]
	d4 = dataset.iloc[:,1:178][dataset['y']==4]
	d5 = dataset.iloc[:,1:178][dataset['y']==5]
	dataset['y'] = dataset['y'].replace([5], [0]).ravel()
	dataset['y'] = dataset['y'].replace([3], [0]).ravel()
	dataset['y'] = dataset['y'].replace([4], [0]).ravel()
	dataset['y'] = dataset['y'].replace([2], [0]).ravel()
	X = dataset.iloc[:, 1:178].values
	y = dataset.iloc[:, 179].values
	return X, y

def fileUploaderView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # d1_avg, d2_avg, d3_avg, d4_avg, d5_avg = [], [], [], [], []
        # for i in range(0,177):
        # 	d1_avg.append(d1.iloc[:,i].sum()/177)
        # 	d2_avg.append(d2.iloc[:,i].sum()/177)
        # 	d3_avg.append(d3.iloc[:,i].sum()/177)
        # 	d4_avg.append(d4.iloc[:,i].sum()/177)
        # 	d5_avg.append(d5.iloc[:,i].sum()/177)
        # d12_dif, d13_dif, d14_dif, d15_dif = [], [], [], []
        # for d1s, d2s in zip(d1_avg, d2_avg):
        # 	d12_dif.append(d1s-d2s)
        # for d1s, d3s in zip(d1_avg, d3_avg):
        # 	d13_dif.append(d1s-d3s)
        # for d1s, d4s in zip(d1_avg, d4_avg):
        # 	d14_dif.append(d1s-d4s)
        # for d1s, d5s in zip(d1_avg, d5_avg):
        # 	d15_dif.append(d1s-d5s)
        # d_ind = []
        # for d12 in d12_dif:
        # 	if d12 > 150:
        # 		d_ind.append(d12_dif.index(d12))
        # d3_ind = []
        # for d13 in d13_dif:
        # 	if d13 > 150 and d13_dif.index(d13) not in d_ind:
        # 		d_ind.append(d13_dif.index(d13))
        # d4_ind = []
        # for d14 in d14_dif:
        # 	if d14 > 150 and d14_dif.index(d14) not in d_ind:
        # 		d_ind.append(d14_dif.index(d14))
        # d5_ind = []
        # for d15 in d15_dif:
        # 	if d15 > 150 and d15_dif.index(d15) not in d_ind:
        # 		d_ind.append(d15_dif.index(d15))
        # X_top_ind = dataset.iloc[:, d_ind].values
        X, y = pre("data.csv")
        from sklearn.model_selection import train_test_split
        # X_train, X_test, y_train, y_test = train_test_split(X_top_ind, y, test_size = 0.3, random_state = 0)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        from sklearn.decomposition import KernelPCA
        kpca = KernelPCA(n_components = 2, kernel = 'rbf')
        X_train = kpca.fit_transform(X_train)
        X_test = kpca.transform(X_test)
        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))
        from sklearn.metrics import roc_auc_score
        roc_auc = roc_auc_score(y_test, predictions)
        print("Area Under the Receiver Operating Characteristic Curve: %.2f%%" % roc_auc)
        if form.is_valid():
            outFile = open("addFile.csv", "wb")
            upFile = request.FILES['file']
            if not upFile.multiple_chunks():
            	outFile.write(upFile.read())
            else:
            	for chunk in upFile.chunks():
            		outFile.write(chunk)
            outFile.close()
            X2, y2 = pre("addFile.csv")
            X2 = sc.transform(X2)
            X2 = kpca.transform(X2)
            y2_pred = classifier.predict(X2)
            if(y2_pred[0] == 1):
            	return render(request, 'fileUploaderTemplate2.html', {'form':form})
            else:
            	return render(request, 'fileUploaderTemplate3.html', {'form':form})
        else:
            return HttpResponse("<h2>File uploaded successful!</h2>")
        # if form.is_valid():
        #     upload(request.FILES['file'])
        #     return HttpResponse("<h2>File uploaded successful!</h2>")
        # else:
        #     return HttpResponse("<h2>File uploaded not successful!</h2>")
 
    form = UploadFileForm()
    return render(request, 'fileUploaderTemplate.html', {'form':form})
  
# def upload(f): 
#     file = open(f.name, 'wb+') 
#     for chunk in f.chunks():
#         file.write(chunk)