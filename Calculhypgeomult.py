import streamlit as st
import pandas as pd
from scipy import stats
import numpy as np
from streamlit import column_config
from streamlit.file_util import streamlit_write

st.title("Calculateur hypergéométrique multrivarié")

st.set_page_config(layout="wide")


cul1, cul2 = st.columns(2)
with cul1:
    deck = st.number_input("Nombre de cartes de votre deck", min_value=7, max_value=99, step=1, value=99)
with cul2:
    main = st.number_input("Nombre de cartes en main", min_value=1, max_value=deck, step=1, value=7)

if 'c' not in st.session_state:
    st.session_state['c'] = 1

K = [0]*(st.session_state.c+1)
Kbegin = [0]*st.session_state.c
Kend = [1]*st.session_state.c
Kcul = [(0,0)]*st.session_state.c

for i in range(st.session_state.c):
    Kcul[i] = st.columns(2)
    with Kcul[i][0]:
        K[i] = st.number_input("Nombre d'éléments dans le {nom}e ensemble".format(nom=i+1),1,99,1,1)
    with Kcul[i][1]:
        (Kbegin[i],Kend[i]) = st.slider("Nombre d'éléments désiré dans le {nom}e ensemble".format(nom=i+1), min_value=1, max_value=min(K[i],main), step=1, value=(0,1))

but1, but2 = st.columns(2)

with but1:
    if st.button("Ajouter un ensemble") :
        st.session_state.c +=1
        st.rerun()

with but2:
    if st.button("Retirer un ensemble") and st.session_state.c > 1:
        st.session_state.c -= 1
        st.rerun()

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
