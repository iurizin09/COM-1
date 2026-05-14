import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import komm


st.header("Exericicio 1 parte 4")

const = komm.Constellation([4j, -2 + 2j, 2 +2j, 1 +1j, -2j])


st.metric(
    label="Media $\mu_s$",
    value=const.mean()[0],


)

st.metric(
    label="Energia Media $E_s$",
    value=f"{const.mean_energy():.2f}",

)

Rs = 50e3   # Taxa de simbolos [baud]
Ts = 1/Rs   # Intervalo de simbolo [s]
sps = 500   # amostras por simbolo [sample/symple]
dt = Ts/sps # Passo de simulaçao [s]

fc = st.slider(
    label="Frequencia de portadora $f_c$",
    min_value=100e3,
    max_value=1e6,
    value=200e3

)

pulse = komm.RectangularPulse()

A   = np.sqrt(1/Ts)
p_t = pulse.taps(sps) * A
m_n = np.array([0,1,1,4,3])
u_n = const.indices_to_symbols(m_n)
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
sbola_t = komm.convolve(p_t, u_t) * dt
t = np.arange(sbola_t.size) * dt 
s_t = sbola_t * np.exp(1j*np.pi*fc * t)

tabs = st.tabs(["Retangular", "Polar" , "Banda Passante"])


with tabs [0]:
    fig, ax = plt.subplots(2,1)
    t = np.arange(sbola_t.size) * dt
    ax[0].plot(t/1e-6, np.real(sbola_t/A))
    ax[0].set_xlabel("$t$ [us]")
    ax[0].set_ylabel("$x(t)$")
    ax[0].set_ylim(-2.5, 2.5)
    ax[0].grid()
    ax[1].plot(t/1e-6, np.real(sbola_t/A))
    ax[1].set_xlabel("$t$ [us]")
    ax[1].set_ylabel("$x(t)$")
    ax[1].set_ylim(-4.5, 4.5)
    ax[1].grid()
    fig.tight_layout()
    st.pyplot(fig)
    pass

with tabs [1]:
    fig, ax = plt.subplots(2,1)
    t = np.arange(sbola_t.size) * dt
    ax[0].plot(t/1e-6, np.abs(sbola_t/A))
    ax[0].set_xlabel("$t$ [us]")
    ax[0].set_ylabel("$x(t)$")
    ax[0].set_ylim(0.4, 4.5)
    ax[0].grid()
    ax[1].plot(t/1e-6, np.angle(sbola_t/A) * (180/np.pi))
    ax[1].set_xlabel("$t$ [us]")
    ax[1].set_ylabel("$x(t)$")
    ax[1].set_ylim(-190, 190)
    ax[1].set_yticks([-180,-135,-90,-45,0,45,90,135,190])
    ax[1].grid()
    fig.tight_layout()
    st.pyplot(fig)
    pass

with tabs [2]:

    fig, ax = plt.subplots()
    ax.plot(t/1e-6, s_t/A)
    ax.set_xlabel("$t$ [us]")
    ax.set_ylabel("$s(t)$")
    ax.set_ylim(-4.5, 4.5)
    ax.grid()
    fig.tight_layout()
    st.pyplot(fig)
    pass
