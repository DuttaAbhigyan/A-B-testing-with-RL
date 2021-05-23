#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 06:01:20 2021

@author: abhigyan
"""

import numpy as np
import scipy as sp


# The environment object. This controls the entire interactions between all participants.
# Callable functions are: getState() -> Returns the current state
#                         takeAction() -> pass a policy or basically the interventions and the
#                                         environment will take the next action and return the 
#                                         rewards or profit obtained
# This is the general RL setting where there is a black-box and we ge to see only the next state
# and rewards after taking an action. The time constant has to be adjusted via the lambda and tau
# Also note that all the random part of A/B testing like formation of consideration set
# interaction between a customer and listing takes place here.

def environment(object):
    
    def __init__(self, interventionEffectUtility, interventionEffectAlpha):
        self.interventionEffectUtility = interventionEffectUtility
        self.interventionEffectAlpha = interventionEffectAlpha
        
    
    def takeAction(self, policy):
        
        
    def getState(self):
        return self.state
    
    
       




# Each object is a particular group type which is used to generate 'n' number of listings
# of that type.           
class ListingGenrator(object):
    
     def __init__(self, typeSet, t, tau=1, n=5, p=10):
        self.typeSet = typeSet
        self.t = t
        self.variance = np.ones(t)
        self.tau = tau
        self.n = n
        self.p = p

    def generateTypeProfiles(self, n):
        self.listings = np.array([])
        self.profits = np.array([])
        for i in range(n):
            self.listings = np.append(self.listings, np.random.normal(self.typeSet, self.variance))
            self.profits = np.append(self.profits, np.random.normal(self.p, 1))
        self.listings = self.listings(-1, self.t)
        return np.reshape(self.listings), self.profits
    
    def getTypeSet(self):
        return self.typeSet
            

# Each object is a particular group type which is used to generate 'n' number of customers
# of that type.        
        
class CustomerGenerator(object):
    
    # typeSet: This is a general n-dim vector which will be used to generate the values
    # a customer will place in each listing. The values are random. The values in the 
    # typeSet will serve as the mean for drawing from a normal distribution with
    # variance 1. (One can change this if she wishes from the function definition below)
    # t: dimension of the typeSet vector
    # lam: The poisson constant with which a customer of this type will be generated
    def __init__(self, typeSet, t, lam=1):
        self.typeSet = typeSet
        self.t = t
        self.variance = np.ones(t)
        self.lam = lam
        
    def getSample(self):
        return np.random.poisson(self.lam)
    
    def generateTypeProfiles(self, n):
        customers = np.array([])
        for i in range(n):
            customers = np.append(customers, np.random.normal(self.typeSet, self.variance))
        return np.reshape(customers(-1, self.t))
    
    def getTypeSet(self):
        return self.typeSet
    


# NOTE: We are dealing with example cases here

# Create 3 different group types of customers and their associated rates of arrival
c1 = np.array([6,7,3])
lam1 = 3
c2 = np.array([4,2,3])
lam2 = 2
c3 = np.array([10,11,12])
lam3 = 5
dim_c = 3    

# Create 4 different group types of listings and their associated release from bookimg
# costants and also the number of them available for booking initially. We also initiliaze
# the mean of the profits obtained from each booking
l1 = np.array([2,3,3])
tau1 = 2
n1 = 8
p1 = 20
l2 = np.array([4,5,3])
tau1 = 3
n2 = 8
p2 = 30
l3 = np.array([9,8,6])  
tau1 = 4
n1 = 8
p3 = 10
l4 = np.array([11,12,10])    
tau1 = 5
n1 = 8
p4 = 15
dim_l = 4

# Create customer objects
customer1 = CustomerGenrator(c1, dim_c, lam1)
customer2 = CustomerGenrator(c2, dim_c, lam2)
customer3 = CustomerGenrator(c3, dim_c, lam3)


# Create customer objects
lisitng1 = LisitngGenrator(l1, dim_l, tau1, n1, p1)
lisitng2 = LisitngGenrator(l2, dim_l, tau2, n2, p2)
lisitng3 = LisitngGenrator(l3, dim_l, tau3, n3, p3)
lisitng4 = LisitngGenrator(l4, dim_l, tau4, n4, p4)



        
