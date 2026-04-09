import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import komm


st.header("Parte 2 : Root-raised cosine")

rng = np.random.default_rng(seed=6)

#Parametros

Rs = 1.0       # Taxa de Simbolos [baud]
Ts = 1/Rs      # Intervalo de Simbolo
sps = 50       # Amostras por simbolo
dt  = Ts/sps   # Passo de S



ɑ  = st.slider(
    label="Factor de rollof ",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
)

pulse  = komm.RootRaisedCosinePulse(rolloff=ɑ)

u_n = rng.choice([-3,-1,1,3],size=400)

p_t = pulse.taps(samples_per_symbol=sps,span=(-16,16))

u_t = komm.sampling_rate_expand(u_n,factor=sps) / dt

x_t = komm.convolve(p_t,u_t) * dt

tabs = st.tabs(["Pulso","Sinal PAM transmitido"])

with tabs[0]:
    fig, ax = plt.subplots(1,2,figsize=(4, 3))
    ts = np.linspace(-16*Ts,16*Ts,num=1000)
    ax[0].plot(ts,pulse.waveform(ts/Ts),label="$p(t)$")
    ax[0].set_xlabel("$x$ [V]")
    ax[0].grid()

    fs = np.linspace(-1.5*Ts,1.5*Ts,num=1000)
    ax[1].plot(fs,pulse.spectrum(fs/Ts),label="$P(f)$")
    ax[1].set_xlabel("$f$")
    ax[1].set_ylim(-0.1,1.1)
    ax[1].grid()
    st.pyplot(fig)

with tabs[1]:
    fig, ax = plt.subplots(figsize=(6, 3))
    ts = np.arange(x_t.size) * dt
    values = st.slider(
        label="Select Arange",
        min_value= ts[0],
        max_value=ts[-1],
        value=(25.0,75.0)
    )
    ax.plot(ts,x_t,label="$x(t)$")
    ax.set_xlabel("$t$")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
