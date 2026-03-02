import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import komm


st.header("Exercicio 3")

fa = 8.0   # Taxa de Amostragem
Ta = 1/fa  # Intervalo de Amostragem
L = 8      # Numero de Niveis
Delta =2.0 # Passo de Quantizacao
dt= 1e-3   # Passo de Simulaçao


#Mensagem

ts = np.arange(0.0,1,dt)   # Eixo do Tempo [s]
x_t = 5*np.sin(2*np.pi*ts) # Sinal [V(s)]

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


