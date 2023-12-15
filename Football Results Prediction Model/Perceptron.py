import numpy as np
import pandas as pd
#read data from file
data = pd.read_csv('Stats.csv')

#convert result values to ints
data.loc[data['Result'] == "W", 'Result'] = 1
data.loc[data['Result'] == "D", 'Result'] = 0
data.loc[data['Result'] == "L", 'Result'] = -1

#choose parameters to train model (from all matches in season)
params = np.array(data[['SoT%','xG']])

#define perceptron algo
def averaged_perceptron(data, labels, params={}, hook=None):
    # if T not in params, default to 100
    T = params.get('T', 100)
    d, n = data.shape
    print(d)
    theta = np.zeros((n,1))
    theta_0 = np.zeros(1)
    ths = np.zeros((n,1))
    th0s = np.zeros(1)
    print("d = {}, n = {}, theta shape = {}, theta_0 shape = {}".format(d,n,theta.shape,theta_0.shape))
  
    for t in range(T):     
      for i in range(d):
        y = labels[0,i]
        print(y,t)

        x = data[i,:]

        a = np.dot(x,theta)+theta_0
        #print("a = {}".format(a))
        positive = np.sign(y*a)
        if positive <=0: # update the thetas
          theta[:,0] = theta[:,0]+ y*x
          theta_0 = theta_0 + y
        
        ths += theta
        th0s += theta_0
        
          
    #print("shape x = {}, y = {}, theta = {}, theta_0 = {}".format(x.shape,y.shape,theta.shape,theta_0.shape))
    print(f"theta = {ths/(n*T)} , theta_0 = {th0s/(n*T)}")
    #return model in form of (Theta.T + Theta_0)
    return (ths/(n*T),th0s/(n*T))

#create labels (all match results so far in season)
test_labels = np.array([data.Result])
print(test_labels)
averaged_perceptron(params,test_labels,{'T':22})