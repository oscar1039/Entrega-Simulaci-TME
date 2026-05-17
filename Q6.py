import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.ticker import ScalarFormatter

#Definim els paràmetres:
N = 1000  #Paràmetre que variem
T = 3  #Paràmetre que variem
kB = 1  #Paràmetre adimensional per simplificar
e = 1 #Paràmetre adimensional per simplificar
estats_energia_possibles = [0, e, 10*e] #Utilitzem els nivells d'energia del problema 35, assumim e=1 per simplificar

#Estat inicial:
particules = [random.choice(estats_energia_possibles) for _ in range(N)]
#Definim una llista de partícules en la qual cada partícula té una probabilitat de 1/3 d'estar en cada nivell

historial_energia = []
ocupacions_n0 = []
ocupacions_n1 = []
ocupacions_n2 = []
#Creem llistes per anar guardant les dades de l'energia del sistema i de l'ocupació dels diferents nivells amb el pas del temps

passos_x = []

for i in range(N*100):
  #Definim un nombre de passos de temps elevat per tal que amb qualsevol N, el sistema pugui provar diferents configuracions.
  #1 pas complet consisteix en N*100 iteracions (cada partícula ha fet, de mitjana, 100 passos)
    p = random.randint(0, N-1)
    nou_estat = random.choice(estats_energia_possibles)
    #A cada pas de temps, una partícula aleatòria agafa un nou nivell d'energia (un dels tres, de forma aleatòria)
    #El sistema només accepta aquest canvi d'energia en unes condicions determinades, seguint l'algorisme de Metropolis

    deltaE = nou_estat - particules[p] #Definim l'augment d'energia per veure si compleix les condicions

#Algorisme de Metropolis:
    if deltaE <= 0:
        particules[p] = nou_estat
        #Sempre que el salt d'energia és negatiu, el sistema l'accepta i la partícula agafa el nou estat d'Energia

    else:
        prob = np.exp(-deltaE/T)
        if random.random() < prob:
            particules[p] = nou_estat
        #Si el salt d'energia és positiu, definim una probabilitat prob, basada en el factor de Boltzmann.
        #Generem un número aleatori entre 0 i 1 i el comparem amb prob.
        #Si aquest és més petit que prob, s'accepta el salt d'energia.
        #Si és més gran o igual que prob, no s'accepta el salt i l'estat de la partícula es queda igual.

   #Anem guardant les dades d'energia i d'ocupació dels estats obtingudes en la simulació:
    if i % (N//10) == 0:
      #Per optimitzar el programa, guardem les dades a cada N/10 passos de temps en comptes de guardar-les a cada pas.
        passos_x.append(i) #Els passos en x es guarden per després definir quan comença l'equilibri
        historial_energia.append(sum(particules)) #L'energia del sistema és la suma de l'energia de totes les partícules
        ocupacions_n0.append(particules.count(estats_energia_possibles[0]))
        ocupacions_n1.append(particules.count(estats_energia_possibles[1]))
        ocupacions_n2.append(particules.count(estats_energia_possibles[2]))



inici_equil = int(len(passos_x) * 0.2) #Definim aquest punt com el principi de l'equilibri
pas_inicial = passos_x[inici_equil]
#A partir d'aquest punt es calcularan les mitjanes de l'ocupació i l'energia

#Calculem la mitjana per a cada llista d'ocupacions des de 'inici_equil' fins al final
mitjana_n0 = np.mean(ocupacions_n0[inici_equil:])
mitjana_n1 = np.mean(ocupacions_n1[inici_equil:])
mitjana_n2 = np.mean(ocupacions_n2[inici_equil:])
print(f"Ocupació mitjana E=0:  {mitjana_n0:.2f} partícules")
print(f"Ocupació mitjana E=e:  {mitjana_n1:.2f} partícules")
print(f"Ocupació mitjana E=10e: {mitjana_n2:.2f} partícules")
print(f"Suma mitjanes: {mitjana_n0 + mitjana_n1 + mitjana_n2:.2f}")

#Gràfica de l'ocupació de cada nivell d'energia en funció del temps:
plt.figure(figsize=(6, 5))

plt.plot(passos_x, ocupacions_n0, label=r'Nivell $n_1$ (E=0)', color='#2D0EC9', linewidth=0.8)
plt.plot(passos_x, ocupacions_n1, label=r'Nivell $n_2$ (E=$\epsilon$)', color='#C98B0E', linewidth=0.8)
plt.plot(passos_x, ocupacions_n2, label=r'Nivell $n_3$ (E=10$\epsilon$)', color='#4CC90E', linewidth=0.8)

#Línies de la mitjana:
plt.hlines(mitjana_n0, pas_inicial, passos_x[-1], colors='#2D0EC9', linestyles='--', alpha=0.5,
           label=r'Mitjana $\langle n_1 \rangle$: ' + f'{mitjana_n0:.1f}')
plt.hlines(mitjana_n1, pas_inicial, passos_x[-1], colors='#C98B0E', linestyles='--', alpha=0.5,
           label=r'Mitjana $\langle n_2 \rangle$: ' + f'{mitjana_n1:.1f}')
plt.hlines(mitjana_n2, pas_inicial, passos_x[-1], colors='#4CC90E', linestyles='--', alpha=0.5,
           label=r'Mitjana $\langle n_3 \rangle$: ' + f'{mitjana_n2:.1f}')
plt.xlabel("Temps (iteracions)")
plt.ylabel("Nombre de Partícules")

#Notació científica per la llegenda:
ax = plt.gca()
xfmt = ScalarFormatter(useMathText=True)
xfmt.set_scientific(True)
xfmt.set_powerlimits((-1, 1))
ax.xaxis.set_major_formatter(xfmt)
yfmt = ScalarFormatter(useMathText=True)
yfmt.set_scientific(True)
yfmt.set_powerlimits((-1, 1))
ax.yaxis.set_major_formatter(yfmt)

plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.xlim(0,N*100)
plt.ylim(0,N)
plt.tight_layout()
plt.show()


#Calculem la fluctuació relativa de l'energia del sistema:
dades_energia_equilibri = historial_energia[inici_equil:] #Les dades utilitzades són les dades d'energia del pas 200 fins al final
energia_mitjana = np.mean(dades_energia_equilibri) #Calculem la mitjana
sigma_E = np.std(dades_energia_equilibri) #Calculem la desviació estàndard (fluctuació absoluta)
fluctuacio_relativa = sigma_E / energia_mitjana #Calculem la fluctuació relativa
print(f"Energia mitjana <E>: {energia_mitjana:.2f}")
print(f"Desviació estàndard: {sigma_E:.2f}")
print(f"Fluctuació Relativa: {fluctuacio_relativa:.4f}")

# Gràfica de l'energia del sistema en funció del temps:
plt.figure(figsize=(6, 5))
plt.plot(passos_x, historial_energia, color='#800080', linewidth=0.8, label="Energia instantània")
plt.hlines(energia_mitjana, pas_inicial, passos_x[-1], color='#4B0082', linestyles='--', alpha=0.5,
           label=r'Energia mitjana $\langle E \rangle$: ' + f'{energia_mitjana:.1f}')

plt.xlabel("Temps (iteracions)")
plt.ylabel("Energia Total del Sistema")
plt.xlim(0, N*100)
plt.ylim(0, N*4)

ax = plt.gca()
xfmt = ScalarFormatter(useMathText=True)
xfmt.set_powerlimits((-1, 1))
ax.xaxis.set_major_formatter(xfmt)

yfmt = ScalarFormatter(useMathText=True)
yfmt.set_powerlimits((-1, 1))
ax.yaxis.set_major_formatter(yfmt)

plt.legend(loc='best', fontsize='small')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()