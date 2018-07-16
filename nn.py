from numpy import genfromtxt
import numpy as np
from scipy import optimize

class NeuralNetwork(object):
    def __init__(self):        
        #Define Hyperparameters
        self.inputLayerSize = 7
        self.hiddenLayerSize = 3
        self.outputLayerSize = 1
        
        #Weights (parameters)
        self.W1 = np.random.randn(self.inputLayerSize,self.hiddenLayerSize)
        self.W2 = np.random.randn(self.hiddenLayerSize,self.outputLayerSize)
        
    def forward(self, X):
        #Propogate inputs though network
        self.z2 = np.dot(X, self.W1)
        self.a2 = self.z2
        self.z3 = np.dot(self.z2, self.W2)
        yHat = self.z3 
        return yHat

    def ReLU(self, x):
        return x * (x > 0)

        
    def sigmoid(self, z):
        #Apply sigmoid activation function to scalar, vector, or matrix
        return 1/(1+np.exp(-z))
    
    def sigmoidPrime(self,z):
        #Gradient of sigmoid
        return self.sigmoid(z)*(1 - self.sigmoid(z))
    
    def costFunction(self, X, y):
        #Compute cost for given X,y, use weights already stored in class.
        self.yHat = self.forward(X)
        J = 0.5*sum((y-self.yHat)**2)
        return J
        
    def costFunctionPrime(self, X, y):
        #Compute derivative with respect to W and W2 for a given X and y:
        self.yHat = self.forward(X)
        
        delta3 = np.multiply(-(y-self.yHat), self.sigmoidPrime(self.z3))
        dJdW2 = np.dot(self.a2.T, delta3)
        
        delta2 = np.dot(delta3, self.W2.T)*self.sigmoidPrime(self.z2)
        dJdW1 = np.dot(X.T, delta2)  
        
        return dJdW1, dJdW2
    
    #Helper Functions for interacting with other classes:
    def getParams(self):
        #Get W1 and W2 unrolled into vector:
        params = np.concatenate((self.W1.ravel(), self.W2.ravel()))
        return params
    
    def setParams(self, params):
        #Set W1 and W2 using single paramater vector.
        W1_start = 0
        W1_end = self.hiddenLayerSize * self.inputLayerSize
        self.W1 = np.reshape(params[W1_start:W1_end], (self.inputLayerSize , self.hiddenLayerSize))
        W2_end = W1_end + self.hiddenLayerSize*self.outputLayerSize
        self.W2 = np.reshape(params[W1_end:W2_end], (self.hiddenLayerSize, self.outputLayerSize))
        
    def computeGradients(self, X, y):
        dJdW1, dJdW2 = self.costFunctionPrime(X, y)
        return np.concatenate((dJdW1.ravel(), dJdW2.ravel()))

def computeNumericalGradient(N, X, y):
        paramsInitial = N.getParams()
        numgrad = np.zeros(paramsInitial.shape)
        perturb = np.zeros(paramsInitial.shape)
        e = 1e-4

        for p in range(len(paramsInitial)):
            #Set perturbation vector
            perturb[p] = e
            N.setParams(paramsInitial + perturb)
            loss2 = N.costFunction(X, y)
            
            N.setParams(paramsInitial - perturb)
            loss1 = N.costFunction(X, y)

            #Compute Numerical Gradient
            numgrad[p] = (loss2 - loss1) / (2*e)

            #Return the value we changed to zero:
            perturb[p] = 0
            
        #Return Params to original value:
        N.setParams(paramsInitial)

        return numgrad 
       

from scipy import optimize


class Trainer(object):
    def __init__(self, N):
        #Make Local reference to network:
        self.N = N
        

    def callbackF(self, params):
        self.N.setParams(params)
        self.J.append(self.N.costFunction(self.X, self.y))   
        

    def costFunctionWrapper(self, params, X, y):
        self.N.setParams(params)
        cost = self.N.costFunction(X, y)
        grad = self.N.computeGradients(X,y)
        print(cost)
        return cost, grad
        

    def train(self, X, y):
        #Make an internal variable for the callback function:
        self.X = X
        self.y = y

        #Make empty list to store costs:
        self.J = []
        
        params0 = self.N.getParams()

        options = {'maxiter': 200, 'disp' : True}
        _res = optimize.minimize(self.costFunctionWrapper, params0, jac=True, method='BFGS', \
                                 args=(X, y), options=options, callback=self.callbackF)

        self.N.setParams(_res.x)
        self.optimizationResults = _res

		

def main():
    training_X = genfromtxt("train_X.csv", delimiter = ",", )	
    training_y = genfromtxt("train_y.csv", delimiter = ",")	
    test = genfromtxt("test.csv", delimiter = ",")
	
	# batch testing took too long, split arrays here
    training_X = training_X.reshape((2000, 7))
    training_y = training_y.reshape((2000, 1))
    test = test.reshape((460, 7))
    
    #training_batches = np.vsplit(training_X, 2)
    #tr_X1 = training_batches[0]
    #tr_X2 = training_batches[1]
	
    #print(tr_X1.shape)
    #print(tr_X2.shape)

    training_batches_y = np.vsplit(training_y, 2)
    #tr_y1 = training_batches_y[0]
    #tr_y2 = training_batches_y[1]

    #print(tr_y1.shape)
    #print(tr_y2.shape)

    NN = NeuralNetwork()
    trainer = Trainer(NN)
    #trainer.train(tr_X1, tr_y1)	
    #trainer.train(tr_X2, tr_y2)
    trainer.train(training_X, training_y)	

	# now that the net is trained, we can test it
    results = NN.forward(test)
    # results = np.asarray(results)
		
	# print this array into the results file
    np.savetxt("results.csv", results, delimiter = ",")
	
main()
