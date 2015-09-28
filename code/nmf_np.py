"""
Non-probabilistic non-negative matrix factorisation, as presented in
"Algorithms for Non-negative Matrix Factorization" (Lee and Seung, 2001).

We change the notation to match ours: R = UV.T instead of V = WH.

The updates are then:
- Uik <- Uik * (sum_j Vjk * Rij / (Ui dot Vj)) / (sum_j Vjk)
- Vjk <- Vjk * (sum_i Uik * Rij / (Ui dot Vj)) / (sum_i Uik)
Or more efficiently using matrix operations:
- Uik <- Uik * (Mi dot [V.k * Ri / (Ui dot V.T)]) / (Mi dot V.k)
- Vjk <- Vjk * (M.j dot [U.k * R.j / (U dot Vj)]) / (M.j dot U.k)
And realising that elements in each column in U and V are independent:
- U.k <- U.k * sum(M * [V.k * (R / (U dot V.T))], axis=1) / sum(M dot V.k, axis=1)
- V.k <- V.k * sum(M * [U.k * (R / (U dot V.T))], axis=0) / sum(M dot U.k, axis=0)

We expect the following arguments:
- R, the matrix
- M, the mask matrix indicating observed values (1) and unobserved ones (0)
- K, the number of latent factors
    
Initialisation can be done by running the initialise(init,tauUV) function. We initialise as follows:
- init_UV = 'ones'       -> U[i,k] = V[j,k] = 1
          = 'random'     -> muU[i,k] ~ U(0,1), muV[j,k] ~ Exp(0,1), 
- tauU[i,k] = tauV[j,k] = 1 if tauUV = {}, else tauU = tauUV['tauU'], tauV = tauUV['tauV']
- alpha_s, beta_s using updates of model

"""

import numpy, math, itertools

class NMF:
    def __init__(self,R,M,K):
        self.R = numpy.array(R,dtype=float)
        self.M = numpy.array(M,dtype=float)
        self.K = K                     
        
        self.metrics = ['MSE','R^2','Rp']
                
        assert len(self.R.shape) == 2, "Input matrix R is not a two-dimensional array, " \
            "but instead %s-dimensional." % len(self.R.shape)
        assert self.R.shape == self.M.shape, "Input matrix R is not of the same size as " \
            "the indicator matrix M: %s and %s respectively." % (self.R.shape,self.M.shape)
            
        (self.I,self.J) = self.R.shape
        
        self.check_empty_rows_columns() 
        
        # For computing the I-div it is better if unknown values are 1's, not 0's
        self.R_excl_unknown = numpy.empty((self.I,self.J))
        for i,j in itertools.product(range(0,self.I),range(0,self.J)):
            self.R_excl_unknown[i,j] = self.R[i,j] if self.M[i,j] else 1.
                 
                 
    # Raise an exception if an entire row or column is empty
    def check_empty_rows_columns(self):
        sums_columns = self.M.sum(axis=0)
        sums_rows = self.M.sum(axis=1)
                    
        # Assert none of the rows or columns are entirely unknown values
        for i,c in enumerate(sums_rows):
            assert c != 0, "Fully unobserved row in R, row %s." % i
        for j,c in enumerate(sums_columns):
            assert c != 0, "Fully unobserved column in R, column %s." % j


    """ Initialise U and V """    
    def initialise(self,init_UV='random'):
        assert init_UV in ['ones','random'], "Unrecognised init option for U,V: %s." % init_UV
        if init_UV == 'ones':
            self.U = numpy.ones((self.I,self.K))
            self.V = numpy.ones((self.J,self.K))
        elif init_UV == 'random':
            self.U = numpy.random.rand(self.I,self.K)
            self.V = numpy.random.rand(self.J,self.K)
    
    
    """ Update U and V for a number of iterations, printing the MSE and divergence each iteration. """
    def run(self,iterations):
        assert hasattr(self,'U') and hasattr(self,'V'), "U and V have not been initialised - please run NMF.initialise() first."        
        
        self.all_performances = {} # for plotting convergence of metrics
        for metric in self.metrics:
            self.all_performances[metric] = []
            
        for it in range(1,iterations+1):
            for k in range(0,self.K):
                self.update_U(k)
            for k in range(0,self.K):
                self.update_V(k)
            
            self.give_update(it)
            

    """ Updates for U and V """    
    def update_U(self,k):
        
        print self.M * (self.V[:,k] * ( self.R / numpy.dot(self.U,self.V.T) ) )
        print self.M * self.V[:,k]
        
        self.U[:,k] = self.U[:,k] * (self.M * (self.V[:,k] * ( self.R / numpy.dot(self.U,self.V.T) ) )).sum(axis=1) / (self.M * self.V[:,k]).sum(axis=1)
        
    def update_V(self,k):
        self.V[:,k] = self.V[:,k] * ( (self.U[:,k] * ( self.R / numpy.dot(self.U,self.V.T) ).T ).T * self.M ).sum(axis=0) / (self.U[:,k] * self.M.T).T.sum(axis=0)
        
        
    ''' Functions for computing MSE, R^2 (coefficient of determination), Rp (Pearson correlation) '''
    def predict(self,M_pred):
        R_pred = numpy.dot(self.U,self.V.T)
        MSE = self.compute_MSE(M_pred,self.R,R_pred)
        R2 = self.compute_R2(M_pred,self.R,R_pred)    
        Rp = self.compute_Rp(M_pred,self.R,R_pred)        
        return {'MSE':MSE,'R^2':R2,'Rp':Rp}        
        
    def compute_MSE(self,M,R,R_pred):
        return (M * (R-R_pred)**2).sum() / float(M.sum())
        
    def compute_R2(self,M,R,R_pred):
        mean = (M*R).sum() / float(M.sum())
        SS_total = float((M*(R-mean)**2).sum())
        SS_res = float((M*(R-R_pred)**2).sum())
        return 1. - SS_res / SS_total if SS_total != 0. else numpy.inf
        
    def compute_Rp(self,M,R,R_pred):
        mean_real = (M*R).sum() / float(M.sum())
        mean_pred = (M*R_pred).sum() / float(M.sum())
        covariance = (M*(R-mean_real)*(R_pred-mean_pred)).sum()
        variance_real = (M*(R-mean_real)**2).sum()
        variance_pred = (M*(R_pred-mean_pred)**2).sum()
        return covariance / float(math.sqrt(variance_real)*math.sqrt(variance_pred))   
        
    def compute_I_div(self):    
        R_pred = numpy.dot(self.U, self.V.T)
        return (self.M * ( self.R_excl_unknown * numpy.log( self.R_excl_unknown / R_pred ) - self.R_excl_unknown + R_pred ) ).sum()        
        
        
    """ Give updates and store performances """
    def give_update(self,iteration):    
        perf = self.predict(self.M)
        i_div = self.compute_I_div()
        
        for metric in self.metrics:
            self.all_performances[metric].append(perf[metric])
               
        print "Iteration %s. I-divergence: %s. MSE: %s. R^2: %s. Rp: %s." % (iteration,i_div,perf['MSE'],perf['R^2'],perf['Rp'])