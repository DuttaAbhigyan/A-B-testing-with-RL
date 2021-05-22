#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 06:01:20 2021

@author: abhigyan
"""

import numpy as np
import scipy as sp




def environment(object):
    
    def __init__(self, t, dim):
        self.t = t
        self.state = np.ones(dim)
        self.stateDim = dim
        self.a=2
        self.b=6
    
    def initializeConsiderationSet(self):
        considerationSet = {}
        for i in range(self.stateDim):
            considerationSet[i] = 0
        return considerationSet
    
    def updatedListing(self, listing, policy):
        listing += np.random.normal(0,policy)
        
    def getProbabilities(self, alpha, policy):
        if policy == 0:
            return alpha
        else:
            
    
    def getNextState(self, customer, listings, policy):
        # Booking
        typeSet = customer.getTypeSet()
        utilities = {}
        alpha = {}
        for i in range(self.stateDim):
            if self.state[i] == 1:
                utilities[i] = np.exp(-np.sum(np.abs(typeSet - updatedListing(listings[i], policy[i]))))
                
        
        # Releasing    


# Each object is a particular group type which is used to generate 'n' number of listings
# of that type.           
class ListingGenrator(object):
    
     def __init__(self, typeSet, t, lam=1):
        self.typeSet = typeSet
        self.t = t
        self.variance = np.ones(t)
        self.lam = lam

    
    def generateTypeProfiles(self, n):
        customers = np.array([])
        for i in range(n):
            customers = np.append(customers, np.random.normal(self.typeSet, self.variance))
        return np.reshape(customers(-1, self.t))
    
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
    
    
    

        
