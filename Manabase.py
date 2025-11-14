import streamlit as st
import pandas as pd
from scipy import stats
import numpy as np
from streamlit import column_config
from streamlit.file_util import streamlit_write

st.set_page_config(layout="wide")

approx = 10
def appr(l):
    return np.int_(l*approx)/approx

st.title("Quelques chiffres")

# Mulligan et deck

on = 1

cul3, cul4 = st.columns(2)
with cul3:
    deck = st.number_input("Nombre de cartes dans votre deck :", min_value=1, step=1, value=99)
with cul4:
    nbland = st.number_input("Nombre de terrains :", min_value=0, step=1, value=41)

probaland = np.zeros(8)
rv = stats.hypergeom(M=deck, n=nbland, N=7)
for i in range(8):
    probaland[i] = rv.pmf(i)

affichdfland = pd.DataFrame({"Nombre de lands :":[0,1,2,3,4,5,6,7],"Probabilité d'en avoir X en main":appr(probaland*100)})

cul1, cul2 = st.columns(2)
with cul1:
    st.dataframe(affichdfland,hide_index=True)

mull=[(0,0)]*4
with cul2:
    st.write("Nombre de terrains gardés dans une main :")
    mull[0] = st.slider("Mulligan 7 :",min_value=0, max_value=7, step=1, value=(2,4))
    mull[1] = st.slider("Mulligan 6 :",min_value=0, max_value=7, step=1, value=(2,5))
    mull[2] = st.slider("Mulligan 5 :",min_value=0, max_value=7, step=1, value=(2,6))
    mull[3] = st.slider("Mulligan 4 :",min_value=0, max_value=7, step=1, value=(0,7))
    st.write("Les mains à 3 cartes sont considérées gardées.")

probamull = np.zeros(5)
for i in range(4):
    probamull[i] = np.sum(probaland[mull[i][0]:mull[i][1]+1])
probamull[4] = 1
affichmull = appr(probamull*100)

probamullcond = np.zeros(5)
for i in range(5):
    probamullcond[i] = probamull[i]*(1-np.sum(probamullcond[0:i]))
affichmullcond = appr(probamullcond*100)
dfmull = pd.DataFrame({"Mulligan :":[7,6,5,4,3],"Probabilité de garder :":affichmull,"Probabilité conditionelle de garder :":affichmullcond})

st.dataframe(dfmull,hide_index=True)

# Landdrop

play = st.radio("Es-tu sur le Play?",["Play", "Draw"])

landdepart = probaland * probamullcond[4]
for i in range(4):
    for j in range(mull[i][0],mull[i][1]+1):
        landdepart[j] += probaland[j] * probamullcond[i] / probamull[i]
def piocheland(l,handsize):
    ll = np.copy(l)
    for i in range(handsize+1):
        ll[i] = l[i]*(deck-handsize-nbland+i)/(deck-handsize) + l[i-1]*(nbland-i+1)/(deck-handsize)
    return ll

landmain = np.zeros((11,19))
landmain[0] = np.concatenate((landdepart,np.zeros(11)))
for i in range(1,11):
    landmain[i] = piocheland(landmain[i-1],7+i)


landdropplay = np.zeros((10,11))
landdropplay[0][0] = landmain[0][0]
landdropplay[0][1] = np.sum(landmain[0][1:])
for i in range(1,10):
    landdropplay[i] = np.concatenate((landmain[i][0:i+1], [np.sum(landmain[i][i+1:])], np.zeros(9-i)))

landdropdraw = np.zeros((10,11))
landdropdraw[0][0] = landmain[1][0]
landdropdraw[0][1] = np.sum(landmain[1][1:])
for i in range(1,10):
    landdropdraw[i] = np.concatenate((landmain[i+1][0:i+1], [np.sum(landmain[i+1][i+1:])], np.zeros(9-i)))

landdrop = landdropplay if play=="Play" else landdropdraw

affichlanddrop = np.concatenate(([["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"],["9"],["10"]],appr(landdrop*100)),axis=1)

dflanddrop = pd.DataFrame(affichlanddrop,columns=["Tour \ Terrains",0,1,2,3,4,5,6,7,8,9,10])
with st.expander("Probabilité d'avoir X terrains au tour Y"):
    st.dataframe(dflanddrop,hide_index=True)

landdropcum = appr((np.flip(np.cumsum(np.flip(landdrop,axis=1),axis=1),axis=1))*100)
affichlanddropcum = np.concatenate(([["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"],["9"],["10"]],landdropcum),axis=1)

dflanddropcum = pd.DataFrame(affichlanddropcum,columns=["Tour \ Terrains",0,1,2,3,4,5,6,7,8,9,10])
with st.expander("Probabilité d'avoir au moins X terrains au tour Y"):
    st.dataframe(dflanddropcum,hide_index=True)

affichlandmain = np.concatenate(([["7"],["8"],["9"],["10"],["11"],["12"],["13"],["14"],["15"],["16"],["17"]],appr(landmain*100)),axis=1)
dflandmain = pd.DataFrame(affichlandmain,columns=["Cartes \ Terrains",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
with st.expander("Nombre de terrains en mains :"):
    st.dataframe(dflandmain,hide_index=True)
