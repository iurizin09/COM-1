import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Exercício 4")

Rs = 50e3    # Taxa de Simbolos 
Ts = 1/Rs    # Intervalo de Simbolo [s]
sps = 100    # Amostras / Simbolo  [Samples/sygnal]
dt = Ts /sps # Passo de simulaçao [s]
A = np.sqrt(1/Ts) # Amplitude do Pulso
N0 = 1e-3

pulse = komm.RectangularPulse()

p_t  = A*pulse.taps(sps) #Pulso Tx
q_t  = np.flip(p_t) # Pulso Rx
awgn = komm.GaussianChannel(noise_power=N0/2 / dt)


u_n  = np.array([-1.0,+1.0,1.0,-3.0]) # Sequencia 
u_t  = komm.sampling_rate_expand(u_n, factor=sps) / dt
x_t  = komm.convolve(p_t,u_t) * dt
y_t  = awgn.transmit(x_t) # Ausencia de Ruido

v_t  = komm.convolve(y_t,q_t) * dt #Sinal na Saida do filtro casado
 
v_n  = komm.sampling_rate_compress(v_t,factor=sps)
 

tabs = st.tabs(["Pulso PAM $x(t)$", "Pulos equivalente $h(t)$","Sinal v(t)"])



with tabs[0]:
    fig, ax = plt.subplots(figsize=(6, 3))
    ts = np.arange(x_t.size) * dt

    ax.plot(ts/1e6, x_t/A)
    ax.plot(ts/1e6, y_t/A)

    ax.set_xlabel("$t$[s]")
    ax.set_ylabel("$x(t)$/A [V]")
    ax.set_ylim(-3.5, 3.5)
    ax.grid()

    st.pyplot(fig)
with tabs[1]:
    h_t = komm.convolve(p_t,q_t) * dt
    fig, ax = plt.subplots(figsize=(6, 3))
    ts = np.arange(h_t.size)  * dt
    ax.plot(ts/1e-6, h_t)
    ax.set_xlabel("$t$[s]")
    ax.set_ylabel("$h(t)$/A [V]")
    ax.grid()
    st.pyplot(fig)
pass


with tabs[2]:
    fig, ax = plt.subplots(figsize=(6, 3))
    ts = np.arange(v_t.size) * dt
    ts0 = np.arange(v_n.size) * Ts
    ax.plot(ts0/1e6, v_n, "C2o")
    ax.plot(ts/1e6, v_t, "C2-")
    ax.set_xlabel("$t$[s]")
    ax.set_ylabel("$v(t)$/A [V]")
    ax.grid()
    st.pyplot(fig)
    pass
