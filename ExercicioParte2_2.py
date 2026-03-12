import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import komm

rng = np.random.default_rng(seed=6)


st.header("Exercício 2")

# Parâmetros
Rs = 50e3       # Taxa de símbolos [símbolos/s = baud]
Ts = 1 / Rs     # Intervalo de símbolo [s]
sps = 100       # Amostras por símbolo
dt = Ts / sps   # Passo de simulação [s]
A = 10.0        # Amplitude de p(t) [V]
Ns = 100
n_iters = 1000  #N de realizaçoes

pulse = komm.RectangularPulse()  # Retangule NRZ
psd_teo = lambda f: 5* A**2 * Ts * np.sinc(Ts*f) 

# Entrada
u_n = rng.choice([-3,-1,1,3],size=(n_iters,Ns))     

# Geração do sinal PAM
p_t = A * pulse.taps(sps)
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
x_t = np.array([np.convolve(p_t, u) * dt for u in u_t])

tabs = st.tabs(["Pulso","Sinal PAM","Densidade Espectral de Potencia"])

with tabs[0]:
    t = np.linspace(-10*Ts,10*Ts, num=1000)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-6, A * pulse.waveform(t / Ts))
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$p(t)$")
   # ax.set_xticks(np.arange(0, 22, 2))
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    fig, ax = plt.subplots(figsize=(6, 3))
    ts = np.arange(x_t[0].size)*dt
    ax.plot(ts/1e3,x_t[0])
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$x(t)$")
    #ax.set_ylim(-5, 5)
    ax.grid()
    st.pyplot(fig)

with tabs[2]:
    f = np.linspace(-4*Rs,4*Rs,num=1000)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(f/1e3,psd_teo(f))
    ax.set_xlabel("$f$ [kHz]")
    ax.set_ylabel("$S_x(f)$ [w/Hz]")
    ax.grid()
    st.pyplot(fig)