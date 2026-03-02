import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import komm


st.header("Exercicio 4")

cols = st.columns(2)



D = 0.1 # duraçao do sinal [s]
fa = st.slider(label="Taxa de Amostragem $f_a$",min_value=1e3,max_value=20e3,value=8e3,step=500.0,format="$%g Amostras[s]$")   # Taxa de Amostragem
Ta = 1/fa  # Intervalo de Amostragem
L = st.select_slider(label="$$numero de niveis de quantizaçao",options=[2,4,8,16,32,64,128])      # Numero de Niveis
Delta =2/L # Passo de Quantizacao
dt= 10e-6   # Passo de Simulaçao


#Mensagem 

ts = np.arange(0.0,D,step=dt)   # Eixo do Tempo [s]
x_t = np.sin(2*np.pi*50*ts) # Sinal [V(s)]

quant = komm.UniformQuantizer.mid_riser(L,Delta)  #biblioteca de indice mid ridex_

x_n = komm.sampling_rate_compress(x_t,int(Ta/dt))
ns = np.arange(x_n.size)

y_n = quant.quantize(x_n)
d_n = quant.digitize(x_n)

tabs = st.tabs(["Curva entrada x saida","Sinais","Tabela"])

with tabs[0]: # Curva de entrarn
    pass
    fig, ax = plt.subplots(figsize=(6, 5))
    xs = np.linspace(-10,10,num=1000)
    ys = quant.quantize(xs)
    ax.plot(xs,ys)
    ax.set_xlabel("$x$ [V]")
    ax.set_ylabel("$y$ [V]")
    ax.set_xticks(quant.thresholds)
    ax.set_yticks(quant.levels)
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    pass
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(ts/1e-3, x_t,"C0",label="$x(t)$")
    ax.plot((ns*Ta)/1e-3,x_n,"C2o",label="$x[n]$")
    ax.plot((ns*Ta)/1e-3,y_n,"C1o",label="$y[n]$")
    ax.set_xlabel("$t[ms]$")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

with tabs[2]:
    st.table({"$x[n]$": x_n,
              "$d[n]$": d_n,
              "$y[n]$": y_n})


