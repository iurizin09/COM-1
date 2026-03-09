import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Exercício 1")

# Parâmetros
Rs = 50e3      # Taxa de símbolos [símbolos/s = baud]
Ts = 1 / Rs    # Intervalo de símbolo [s]
sps = 100      # Amostras por símbolo
dt = Ts / sps  # Passo de simulação [s]
A = 5.0        # Amplitude de p(t) [V]

# Forma de onda do pulso p(t) normalizada (Ts = 1, A = 1)
def pulse_waveform(t):
    return (
        (t - 0.2) / 0.3 * ((0.2 <= t) & (t < 0.5)) +
        (0.8 - t) / 0.3 * ((0.5 <= t) & (t < 0.8))
    )

def pulse_taps(sps):
    n = np.arange(sps) / sps
    return pulse_waveform(n)

# Entrada
u_n = np.array([0.4, -0.1, -0.5, 0.8, -0.2])

# Geração do sinal PAM
p_t = A * pulse_taps(sps)
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
x_t = np.convolve(p_t, u_t) * dt

tabs = st.tabs(["Pulso", "Sinal PAM"])

with tabs[0]:
    t = np.linspace(0, Ts, num=1000)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-6, A * pulse_waveform(t / Ts))
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$p(t)$")
    ax.set_xticks(np.arange(0, 22, 2))
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.arange(x_t.size) * dt / 1e-6, x_t)
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$x(t)$")
    ax.set_ylim(-5, 5)
    ax.grid()
    st.pyplot(fig)
