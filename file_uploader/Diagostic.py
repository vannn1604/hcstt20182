import csv
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import random
import numpy as np

# Load data tu CSV file
def load_data(filename):
    lines = csv.reader(open(filename, "r", encoding='utf8'))
    dataset = list(lines)
    dataset2 = []
    for i in range(1,len(dataset)):
        del dataset[i][0]
        for j in range(len(dataset[i])):
            dataset[i][j] = float(dataset[i][j])
        if dataset[i][len(dataset[i])-1] != 1.0:
            dataset[i][len(dataset[i])-1] = 0.0
        dataset2.append(dataset[i])

    return dataset2

def get_data_label(dataset):
    data = []
    label = []
    for x in dataset:
        data.append(x[:178])
        label.append(x[-1])

    return data, label

def main():
    dataset = load_data('data.csv')
    dataSet, labelSet = get_data_label(dataset)

    X_train, X_test, y_train, y_test = train_test_split(dataSet, labelSet)
    print('Data size {0} \nTraining Size={1} \nTest Size={2}'.format(len(dataset), len(X_train), len(X_test)))
    # print(X_train)
    # print("------------------------------------")
    # print(y_train)
    clf = GaussianNB()
    # y_train = y_train.reshape(y_train.size, 1)
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)

    print('Accuracy : {0}%'.format(score*100))

    # diagnosic
    # dt = dataset[random.randint(0,len(dataset))]
    dt = X_test[random.randint(0,len(X_test))]
    # print("--------------\nBộ lấy ra chẩn đoán")
    # print(dt)
    # del dt[-1]
    data_chuan_doan2 = []
    data_chuan_doan2.append(dt)
    # print(data_chuan_doan2[0][177])
    kq = clf.predict(data_chuan_doan2)
    kq = int(kq[0])
    # print((X_test[0]))
    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    # print((dataset[0]))
    # print(kq)
    # print(type(kq))
    if(kq > 0):
        print("-------------------\nMắc bệnh \n")
    else:
        print("-------------\nKhông mắc bệnh \n")

if __name__ == "__main__":
    main()