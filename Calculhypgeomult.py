import streamlit as st
import pandas as pd
from scipy import stats
import numpy as np
from streamlit import column_config
from streamlit.file_util import streamlit_write

st.title("Calculateur hypergéométrique multrivarié")

st.set_page_config(layout="wide")

deck = st.number_input("Nombre de cartes de votre deck", min_value=7, max_value=99, step=1, value=99)
main = st.number_input("Nombre de cartes en main", min_value=1, max_value=deck, step=1, value=7)
c = st.number_input("Nombre d'ensembles à considerer",1,deck,1,1)

K = [0]*(c+1)
Kbegin = [0]*c
Kend = [1]*c

for i in range(c):
    K[i] = st.number_input("Nombre d'éléments dans le {nom}e ensemble".format(nom=i+1),1,99,1,1)
    (Kbegin[i],Kend[i]) = st.slider("Nombre d'éléments désiré dans le {nom}e ensemble".format(nom=i+1), min_value=1, max_value=min(K[i],main), step=1, value=(0,1))

autre = deck - np.sum(K)
st.write("Nombre d'autres carte du deck :",autre)
K[-1] = autre

P = stats.multivariate_hypergeom(m=K, n=main)

proba = P.pmf(np.concatenate((Kbegin,[main - np.sum(Kbegin)])))
Klist = np.copy(Kbegin)

def suivant(l,lmin,lmax):
    ll = np.copy(l)
    k = 0
    while k<len(l) and ll[k] == lmax[k]:
        ll[k] = lmin[k]
        k += 1
    if k < len(l):
        ll[k] += 1
    return ll

def eg(l,ll):
    flag = len(l) == len(ll)
    k = 0
    while flag and k < len(l):
        flag = (ll[k] == l[k])
        k += 1
    return flag

while not eg(Klist,Kend):
    Klist = suivant(Klist,Kbegin,Kend)
    proba += P.pmf(np.concatenate((Klist,[main - np.sum(Klist)])))

st.write("Probabilité :",proba*1000//1/10,"%")
