NSAMPLES=10#The number of samples we receive from each axis of each json
PATH="JsonsCollidos/"#Where are all the jsons?
NJSONS=9#remember the name needs to be the next in the sequence(30,31,34,35,38,39,42....)
#GOLPES=["Gancho","Recto","Crochet","Mixto","Patada circular","Patada giratoria","Patada voladora","Patada gancho"]#The name needs to have 3 characters minimum
#DIRECCIONS=["Ascendente","Frontal","Lateral Dereito","Lateral Esquerdo","Descendente"]
GOLPES=["Crochet","Golpe","Patada"]
DIRECCIONS=["Derecha","Izquierda","Frontal"]
RANDOM_STATE=0#this is for the algorith
MAXITER=1000000
NSA_PW=10  #Numero de mostras coas que facemos a media de potencia
DIMENSIONVIBRATION=5 #This parameter is the number of samples we are going to read in the maximum case(5 samples X axis)
TIMELIMIT=0.1
POTLIMIT=0.05
TIPOFILTRO = "nada"  # "nada","normal","deletevibration","reducepot"
