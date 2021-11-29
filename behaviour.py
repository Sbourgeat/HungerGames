"""
This module allows the simulation of a fruit fly inside a virtual 3D arena based on research conducted at Jaksic lab EPFL.
The code was created by Samuel Bourgeat, PhD student at EPFL.

The class fly contains a reinforcment learning model and the script needed to simulate the behaviour of a fly in sim().

To make the module work, one need to provide the following attributes :
Attributes
    ----------
    speed : float
        The speed of the fly
    cognition : float
        Cognition value of the fly
    tshift : float
        Time before food shifts from sector
    nTot : float
        Total duration of the experiment
    alpha : float
        Learning rate
    bias : list
        Vector of the biases
    v : list
        Vector of learning strength
    Lambda : int
        Maximum learning strength. Default = 1.

Class
    -------
    fly


"""




import numpy as np
from pylab import show
from math import sqrt
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import math
import random

class fly:
    """
    Simulate Drosophila behaviour in the hunger games set up.


    Attributes
    ----------
    speed : float
        The speed of the fly
    cognition : float
        Cognition value of the fly
    tshift : float
        Time before food shifts from sector
    nTot : float
        Total duration of the experiment
    alpha : float
        Learning rate
    bias : list
        Vector of the biases
    v : list
        Vector of learning strength
    Lambda : int
        Maximum learning strength. Default = 1.

    Methods
    -------
    sim()
        simulate the behaviour of the fly
    RL()
        compute reinforcment learning model

    """
    
    def __init__(self, speed: float, cognition: float, tshift: float, nTot: float, alpha: float, bias: list) -> None:
        self.speed = speed
        self.cognition = cognition
        self.tshift = tshift
        self.nTot = nTot
        self.alpha = alpha
        self.bias = bias
        #self.v = v
        #self.Lambda = Lambda
        




    def RL (v, alpha, Lambda = 1):
        val = sum(v)
        #print('Val =', val)
        pred_err = Lambda - val
        val_change = alpha * pred_err
        v = v[-1] + val_change
        #print(v)
        return v


    def sim(self) -> list:


        speed = self.speed
        cognition = self.cognition
        tshift = self.tshift
        nTot = self.nTot
        alpah = self.alpha
        bias = self.bias

        #fig = plt.figure(figsize=(10,10),dpi=500)
        #ax = fig.add_subplot(1, 1, 1,projection='3d')
        #ax.set_xlim(120)
        #ax.set_ylim(120)
        #ax.set_zlim(160)
        #plt.title('The Hunger Game')
        #ax.set_xlabel('x')
        #ax.set_ylabel('y')
        #ax.set_zlabel('z')
        #ax.scatter(80,0,40, 'ro')
        #ax.scatter(20,0,40, 'ro')
        #ax.scatter(80,0,100, 'ro')
        #ax.scatter(20,0,100, 'ro')    
        
        e1 = [80,0,40]
        e2 = [20,0,40]
        e3 = [80,0,100]
        e4 = [20,0,100]
        
        xlims = [0,120]
        ylims = [0,120]
        zlims = [0,160]
        
        
        dt = 1/60 #msec
        shift = int(tshift)# *(1+speed))
        n = int((nTot) *(1/dt)) # sec
        nShift = n/shift
        tempoShift = [(i+1)*shift for i in range(int(nShift))]
        Consumption = 0
        Strength = [0.00001]
        Strength_biase = [0.00001]
        trial = 0
        trial_B = 0
        T = 0
        #Strength1 = [0]
        #Strength2 = [0]
        #Strength3 = [0]
        #Strength4 = [0]
        
        trial = 0 # nb of attemps to learn the association
        
        speed = speed
        
        
        
        N_cognition = cognition * Strength[-1]
        N_bias1 = bias[0] * Strength_biase[-1]
        N_bias2 = bias[1] * Strength_biase[-1]
        N_bias3 = bias[2] * Strength_biase[-1]
        N_bias4 = bias[3] * Strength_biase[-1]
        #Lambda = cognition
        
        V = 0
        
        I = [0]
        
        X= []
        Y= []
        Z= []
        
        Food = [0,1,0,0] #Where's the food at t = 0
        #print(Food)
        Sector = 0 # Sector at t = 0
        E = []
        for sec in range(4):
            E.append(random.sample([e1,e2,e3,e4],4))
        entrance1 = E[0][0]
        entrance2 = E[0][1]
        entrance3 = E[0][2]
        entrance4 = E[0][3]
        
        #print(E)
        
        
        for i in range(n):
            #print(i)
            #print(X,Y,Z)
            if i == 0:
                x0 = 100
                y0 = 100
                z0 = 80
                X.append(x0)
                Y.append(y0)
                Z.append(z0)
                
            
            elif i !=0 :
                if Food[Sector] == 1:
                    #print(Sector, Food)
                    Consumption +=1
                    X.append(X[i-1])
                    Y.append(Y[i-1])
                    Z.append(Z[i-1])
            
                elif Food[Sector] == 0 :
                    D1 = math.sqrt((entrance1[0] - X[i-1])**2 + (entrance1[1] - Y[i-1])**2 + (entrance1[2] - Z[i-1])**2)
                    D2 = math.sqrt((entrance2[0] - X[i-1])**2 + (entrance2[1] - Y[i-1])**2 + (entrance2[2] - Z[i-1])**2)
                    D3 = math.sqrt((entrance3[0] - X[i-1])**2 + (entrance3[1] - Y[i-1])**2 + (entrance3[2] - Z[i-1])**2)
                    D4 = math.sqrt((entrance4[0] - X[i-1])**2 + (entrance4[1] - Y[i-1])**2 + (entrance4[2] - Z[i-1])**2)
                
                    if D1 <= N_cognition + (N_bias1 * (1-Strength[-1])) or D2 <= N_cognition + (N_bias2 * (1-Strength[-1])):
                        #print('Good job',i)
                        #print("trial at t=", i)
                        trial +=1
                        Strength.append(RL([Strength[trial-1]], alpha))
                        N_cognition = cognition * (Strength[-1])
                        #print('The learning strength is now:', Strength[-1],' cognition is: ', cognition)
                        V+=1
                        T+=1
                        X.append(x0)
                        Y.append(y0)
                        Z.append(z0)
                        I.append(i)
                            #X = [x0]
                            #Y = [y0]
                            #Z = [z0]
                        if Sector < 3 :
                            Sector +=1
                            entrance1 = E[Sector-1][0]
                            entrance2 = E[Sector-1][1]
                            entrance3 = E[Sector-1][2]
                            entrance4 = E[Sector-1][3]
                        else :
                            Sector = 1
                            entrance1 = E[Sector-1][0]
                            entrance2 = E[Sector-1][1]
                            entrance3 = E[Sector-1][2]
                            entrance4 = E[Sector-1][3]
                    
                        #print('New sector = ', Sector)
                
            
                    elif D3<= 10 + (N_bias3 * (1-Strength[-1]) * (1 - Strength_biase[-1])) or D4 <= 10 + (N_bias4 * (1-Strength[-1]) * (1 - Strength_biase[-1])):
                        #print('Dommage!',i)
                        trial_B +=1
                        #print("trial at t=", i)
                        Strength_biase.append(RL([Strength_biase[trial_B-1]], alpha))
                        N_Biase3 = bias[2] * (Strength_biase[-1])
                        N_Biase4 = bias[3] * (Strength_biase[-1])
                        X.append(x0)
                        Y.append(y0)
                        Z.append(z0)
                        T+=1
                    
                    else:
                
                        xi = X[i-1] + np.random.normal(0,1)* 0.5 # 0.5 is dt
                        yi = Y[i-1] + np.random.normal(0,1)* 0.5
                        zi = Z[i-1] + np.random.normal(0,1)* 0.5
                
                        if xi <= xlims[1] and xi >= xlims[0] and yi <= ylims[1] and yi >= ylims[0] and zi <= zlims[1] and zi >= zlims[0] :
                            X.append(xi)
                            Y.append(yi)
                            Z.append(zi)
                        else:
                        
                            distance = [- X[i-1] + x0, - Y[i-1] + y0, -Z[i-1] + z0]
                            norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2 + distance[2]**2)
                            direction = [distance[0] / norm, distance[1] / norm, distance[2]/norm]
                        #bullet_vector = [direction[0] * math.sqrt(2), direction[1] * math.sqrt(2)]
                            xi = X[i-1] + direction[0] * speed * dt
                            yi = Y[i-1] + direction[1] * speed * dt
                            zi = Z[i-1] + direction[2] * speed * dt
                        #print(xi,yi,zi)
                            X.append(xi)
                            Y.append(yi)
                            Z.append(zi)
                    
                        
                
               # print(xi,yi,zi)
            
                if i in tempoShift :
                    indx  = Food.index(1)
                    if indx >= 3:
                        newindx = 0
                        Food[indx] = 0
                        Food[newindx] = 1
                    else :
                        Food[indx] = 0
                        Food[indx+1] = 1
                    #print('Shift', Food)

                
            
        #print('Last coordinates :',X[-1],Y[-1],Z[-1], len(X))
        #print('Final distances from the entrances :',D1,D2,D3,D4)
        #print('Final Sector =', Sector)
        #print('Consumption time = ', Consumption)
        #print('I =', I)
        
        #ax.plot3D(X, Y, Z, color='black')
        #ax.plot3D(X[0], Y[0], Z[0],'gx') #start in green
        #ax.plot3D(X[-1], Y[-1], Z[-1],'bx') #end in blue
        
        
        #ax.set_title('The DGRP Hunger Games')


        #show()
        Consumption = Consumption/(60*60*60) # correction for time for higher speeds
        print("Consumption,","Victory,","Time", ":")
        return [Consumption,V,T] #Consumption time and number of victory


    if __name__ == "__main__":
        sim(self)








