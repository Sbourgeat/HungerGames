# Run this code to get the results of the sim


import behaviour
import numpy as np
import scipy as sp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics
import time
from time import sleep
from tqdm import tqdm



#
N = 1360/2
mu_cognition = 0.5 # alpha
mu_speed = 50 # cm.sec-1
mu_fecundity = 10

sigma_cognition = .1
sigma_speed = 10
sigma_fecundity = 1

cognition = np.random.normal(mu_cognition, sigma_cognition, N)

#count, bins, ignored = plt.hist(cognition, 30, density=True)



# droso speed = 205 cm.sec-1  or 180 cm.sec-1
#https://cob.silverchair-cdn.com/cob/content_public/journal/jeb/44/3/10.1242_jeb.44.3.567/1/567.pdf?Expires=1635860935&Signature=HFs16xtRhtx7D-cYEgjB7o9Szmw0FY0aY0cULTqY1NHIN4tZODANDy~SJEHxH6HLm7nQEunYsk1003ExFDXKs6CKbfcFIwXyVeFtOiN8QHM~a7WHZt2BH7Ywb6xQSB56nmFjZpvl~G6qkrju2IKd21jsCM5ln8dwWw4rxiCmWTQ1jU1bPpKfZZdYjzpfMeZwyFIY4K628mQfZxAWXXekoQaPeXgR1izDY5YC~eJynh5i~GTxC9p3zJ84wA1mQxRBSmdCw7ihQVpGWHygJ8fmOMLWJgv~CpQQj5g6LFzm8hyolri0qNqiZn8H-bTUzD5v~n8o8ShvhwOiaJM2qkX9zg__&Key-Pair-Id=APKAIE5G5CRDK6RD3PGA
# https://digitalcommons.usm.maine.edu/cgi/viewcontent.cgi?referer=https://www.google.com/&httpsredir=1&article=1094&context=etd

speed = np.random.normal(mu_speed, sigma_speed, N)

#count, bins, ignored = plt.hist(speed, 30, density=True)



fecundity = np.random.normal(mu_fecundity, sigma_fecundity, N)

#count, bins, ignored = plt.hist(fecundity, 30, density=True)



# Speed is in cm.sec-1, tShift and nTot are in sec
# FLy ait speed 15 mm/sec https://elifesciences.org/articles/65878


N = 1360/2

mu_cognition = 50 #mm


sigma_cognition = 5

cognition2 = np.random.normal(mu_cognition, sigma_cognition, N)

#count, bins, ignored = plt.hist(cognition2, 30, density=True)



def biase (dist):
    biais = [1,1,1,1] # no bias here
    nb = np.random.choice([1,2])
    pos = np.random.choice([0,1,2,3],nb)
    B = np.random.choice(dist)
    for i in pos:
        biais[i]=B
    return biais
    

mu_biases = 50
sigma_biases = 5
N = 1360

Biases = np.random.normal(mu_biases, sigma_biases, N)

#count, bins, ignored = plt.hist(Biases, 30, density=True)




def combination():
    cog = np.random.choice(cognition)
    cog2 = np.random.choice(cognition2)
    spe = np.random.choice(speed)
    fec = np.random.choice(fecundity)
    b = biase(Biases) 
    return [cog,cog2, spe, fec, b]


C = []
for i in range(N):
    C.append(combination())








#for i in range(5):
#    bar.update(i+1)
#    sleep(0.1)
#bar.finish()


Res = dict()
Res['Cognition'] = []
Res['Cognition_distance'] = []
Res['Speed'] = []
Res['Fecundity'] = []
Res['Time On Food'] = []
Res['Victory'] = []
Res['Biases'] = []
Res['Trial'] = []


shift = 60*30   # sec
totTime = 60*60*5     # sec
#cognition = 5 # units

I = 0
start_time = time.time()

l =len(C)
#l=2


for i in tqdm(range(l)) :
    sleep(0.000001)
    #if I % 5  == 0: 
        #print('i = {}'.format(I), "Time spent =", time.time() - start_time, "sec")
    I+=1
    Res['Cognition'].append(C[i][0])
    Res['Cognition_distance'].append(C[i][1])
    Res['Speed'].append(C[i][2])
    Res['Fecundity'].append(C[i][3])
    Res['Biases'].append(C[i][4])
    #print('Simulation with parameters: Cognition = ', 5, ' alpha=', i[0], ' speed=',i[1])
    R = []
    Vic = []
    Tr = []
    for ii in range(1):
        Fly = behaviour.fly(speed = C[i][2], cognition = C[i][1], tshift = shift  ,nTot = totTime ,alpha = C[i][0], bias = C[i][4], dt = 1/1000)
        Main_res = Fly.sim()
        #Main_res = main(C[i][2],C[i][1],shift,totTime,C[i][0],C[i][4]) #main(speed, cognition, tShift,nTot,alpha, bias)
        R.append(Main_res[0])
        Vic.append(Main_res[1])
        Tr.append(Main_res[2])
        
    x = statistics.mean(R)
    xx = statistics.mean(Vic)
    xxx = statistics.mean(Tr)
    
        
    Res['Time On Food'].append(x)
    Res['Victory'].append(xx)
    Res['Trial'].append(xxx)
    

        
    
    #if I == 10 :
    #    break
    #else : I+=1
    



df = pd.DataFrame(Res)


df_bias=[]
for i in range(len(df)):
    df_bias.append(sum(df['Biases'][i])) 
    
df['sum_biases']= df_bias

df_COG=[]
for i in range(len(df)):
    df_COG.append(df['Cognition'][i] + df['Cognition_distance'][i]) 
    
df['sum_cognition']= df_COG


print("Saving the results")
df.to_csv("Res.csv",index=False)


    
    



