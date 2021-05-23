#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 06:01:20 2021

@author: abhigyan
"""

import numpy as np
import random


# The environment object. This controls the entire interactions between all participants.
# Callable functions are: getState() -> Returns the current state
#                         takeAction() -> pass a policy or basically the interventions and the
#                                         environment will take the next action and return the 
#                                         rewards or profit obtained
# This is the general RL setting where there is a black-box and we ge to see only the next state
# and rewards after taking an action. The time constant has to be adjusted via the lambda and tau
# Also note that all the random part of A/B testing like formation of consideration set
# interaction between a customer and listing takes place here.
#
# The input arguments to __init__ are as follows:
#
# listings --> Dictionary containing all the listings
# customers --> List containing the customer objects
# dim --> dimension of the type profiles
# alpha --> alpha from the probability choice model i.e the Bernoulli probability associated with 
#           forming the consideration set, a 2D matrix where rows denote listing group type and 
#           columns denote customer group type
# interventionEffectAlpha --> a 2D matrix which decides how to change the alpha when an intervention
#                             is applied. Basically, it scales the alpha by a factor greater than or 
#                             less than 1 (and positive). A 2D matrix where rows denote listing group type and 
#                             columns denote customer group type
#interventionEffectUtility --> a 2D matrix which decides how to change the utility when an intervention
#                             is applied. Basically, it scales the utility by a factor greater than or 
#                             less than 1 (and positive). A 2D matrix where rows denote listing group type and 
#                             columns denote customer group type
#epsilon --> probability associated with customer not buying anything

def environment(object):
    
    def __init__(self, listings, customers, dim, alpha, interventionEffectUtility, interventionEffectAlpha,
                 epsilon):
        self.listings = listings
        self.customers = customers
        self.dim = dim
        self.alpha = alpha
        self.interventionEffectUtility = interventionEffectUtility
        self.interventionEffectAlpha = interventionEffectAlpha
        self.epsilon = epsilon
        
        # Create 2 state descriptions, one dynamic and updates at each time step
        # and indicates whether a listing is vaialable or not by 1,0 respectively
        # The other simply contains the types of all listings
        self.state = {}
        self.stateListings = {}
        
        # One is used to store the amount of time a listing will remain booked
        # Another actually tracks how much time has passed of a listing booked by a customer
        self.bookingTimeTracker = {}
        self.bookedTimeTracker = {}
        
        # Initialize the values appropriately
        for i in range(len(listings)):
            self.state[i]={}
            self.stateListings[i] = {}
            self.bookingTimeTracker[i] = {}
            for j in range(len(listings[i])):
                self.stateListings[i][j] = listings[i][j]
                self.state[i][j]=1
                self.bookingTimeTracker[i][j] = 0
                self.bookedTimeTracker[i][j] =-1

    
    # Caclulates the utility which depends on the particular customer type and 
    # listing type. If intervention is applied the utiltiy is scaled according
    # to the preference term.
    def calculateUtility(self, customerType, listingType, policy, preference):
        utility = np.exp(-np.sum(np.abs(customerType-listingType)))
        if policy==1:
            utility = utility*preference
        return utility
    
    
    def updateState(self, index):
        self.state[index[0]][index[1]] -= 1
        
    
    # Performs random sampling according to the choice model of the customer and returns the choice
    def getChoice(self, customerTypeProfile, customerGroup, policy):
        considerationSet = []
        choiceProbabilities = np.array([])
        
        # Form the consideration set and calculated the associated probabilities
        for i in self.state.keys():
            for j in self.state[i].keys():
                # If a listing is available then..
                if self.state[i][j] == 1:
                    considerationSet.append((i,j))
                    if policy[i][j] == 1:
                        alpha = self.alpha[i][customerGroup] * self.interventionEffectAlpha[i][customerGroup]
                    utility = self.calculateUtility(customerTypeProfile, self.stateListings[i][j], 
                                                    policy[i][j], self.interventionEffectUtility[i][customerGroup])
                    choiceProbabilities = np.append(choiceProbabilities, alpha*utility)
        
        choiceProbabilities =  np.append(choiceProbabilities, self.epsilon)
        choiceProbabilities = choiceProbabilities/np.sum(choiceProbabilities)
        considerationSet.append((-1,-1))
        
        # Randomly sample to get the choice
        choice = np.random.choice(considerationSet, p=choiceProbabilities)
        return choice
        
    
    # Take one step action,, takes in policy and returns profit
    def takeAction(self, policy):
        
        # Create a set of arriving customers for the current time step
        arrivingCustomers = []
        for i in range(len(self.customers)):
            arrivingCustomers.append(self.customers[i].getSample())
            self.customers[i].generateTypeProfiles(arrivingCustomers[i])
        
        # Randomly shuffle the customer set
        order = []
        for i in range(self.dim):
            order += [arrivingCustomers[i]]*i
        random.shuffle(order)
        
        # Pick a customer and send her to the platform
        counter = np.zeros(self.dim)
        profit = 0
        for i in order:
            temp=self.customers[i].getTypeProfiles()
            customerTypeProfile = temp[counter[i]]
            counter[i] += 1
            choice = self.getChoice(customerTypeProfile, policy)
            # If the customer decides to buy from the platform
            if choice[0] != -1:
                # Mark the listing is unavailable
                self.state[choice[0]][choice[1]] -= 1
                # Get the profit associated with the listing
                profit += self.listings[choice[0]].profit()[choice[1]]
                # Calculate the time for which the listing will reman booked
                self.bookingTimeTracker[choice[0]][choice[1]] = np.random.exponential(self.customer[choice[0]].getTau())
                self.bookedTimeTracker[choice[0]][choice[1]] += 1
                
        # Add a time step to each booked listing and Check whether to release any listing
        for i in self.state.keys():
            for j in self.state[i].keys():
                if self.state[i][j] == 0:
                    self.bookedTimeTracker[i][j] += 1
                    if self.bookedTimeTracker[i][j] > self.bookingTimeTracker[i][j]:
                        self.state[i][j] += 1
                        self.bookingTimeTracker[i][j] = 0
                        self.bookedTimeTracker[i][j] = -1
        
        return profit
            
    # Returns the current state
    def getState(self):
        return self.state
    
    
       




# Each object is a particular group type which is used to generate 'n' number of listings
# of that type.           
class ListingGenerator(object):
    
    def __init__(self, typeSet, t, tau=1, n=5, p=10):
        self.typeSet = typeSet
        self.t = t
        self.variance = np.eye(t)
        self.tau = tau
        self.n = n
        self.p = p
        self.listings = np.array([])
        self.profits = np.array([])
       
        for i in range(n):
            self.listings = np.append(self.listings, np.random.normal(self.typeSet, self.variance))
            self.profits = np.append(self.profits, np.random.normal(self.p, 1))
        self.listings = np.reshape(self.listings, (-1, self.t))
        #return np.reshape(self.listings), self.profits
    
    def getTypeProfiles(self):
        return self.listings
    
    def getTypeSet(self):
        return self.typeSet
    
    def getTau(self):
        return self.tau
    
    def getProfit(self):
        return self.profit
            

# Each object is a particular group type which is used to generate 'n' number of customers
# of that type.        
        
class CustomerGenerator(object):
    
    # typeSet: This is a general n-dim vector which will be used to generate the values
    # a customer will place in each listing. The values generated are from random normal distribution. 
    # The values in the  typeSet will serve as the mean for drawing from a normal distribution with
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
        self.customers = np.array([])
        for i in range(n):
            self.customers = np.append(self.customers, np.random.normal(self.typeSet, self.variance))
        return np.reshape(self.customers, (-1, self.t))
    
    def getTypeProfiles(self):
        return self.customers
    
    def getTypeSet(self):
        return self.typeSet
    


# NOTE: We are dealing with example cases here

# Create 3 different group types of customers and their associated rates of arrival
c1 = np.array([6,7,3])      # Create group type of listings with the mean of the types of the group type
lam1 = 3                    # Customer arrival constant
c2 = np.array([4,2,3])
lam2 = 2
c3 = np.array([10,11,12])
lam3 = 5
dim_c = 3    


# Example cutomer and listing objects: 
# Create 4 different group types of listings and their associated release from bookimg
# costants and also the number of them available for booking initially. We also initiliaze
# the mean of the profits obtained from each booking

l1 = np.array([2,3,3])      # Create group type of listings with the mean of the types of the group type
tau1 = 2        # The release of booking constant
n1 = 8          # Number of listings of the particular group type available
p1 = 20         # Mean of the profit associated with the particular group type

l2 = np.array([4,5,3])
tau2 = 3
n2 = 8
p2 = 30

l3 = np.array([9,8,6])  
tau3 = 4
n3 = 8
p3 = 10

l4 = np.array([11,12,10])    
tau4 = 5
n4 = 8
p4 = 15

dim_l = 3      # Dimension of the type array of the group type

# Create customer objects
customer1 = CustomerGenerator(c1, dim_c, lam1)
customer2 = CustomerGenerator(c2, dim_c, lam2)
customer3 = CustomerGenerator(c3, dim_c, lam3)


# Create customer objects
listing1 = ListingGenerator(l1, dim_l, tau1, n1, p1)
listing2 = ListingGenerator(l2, dim_l, tau2, n2, p2)
listing3 = ListingGenerator(l3, dim_l, tau3, n3, p3)
listing4 = ListingGenerator(l4, dim_l, tau4, n4, p4)


customerList = [customer1, customer2, customer3]
listingDic = {}
listingDic[0] = listing1.getTypeProfiles()
listingDic[1] = listing2.getTypeProfiles()
listingDic[2] = listing3.getTypeProfiles()
listingDic[3] = listing4.getTypeProfiles()

dim = 3



        
