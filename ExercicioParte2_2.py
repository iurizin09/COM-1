import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Exercício 2")

rng = np.random.default_rng(seed=42)

# Parâmetros
sps = 50        # Amostras por símbolo
Rs = 50e3       # Taxa de símbolos [símbolos/s]
Ts = 1 / Rs     # Intervalo de símbolo [s]
dt = Ts / sps   # Passo de simulação [s]
A = 5.0         # Amplitude de p(t) [V]
Ns = 100        # Número de símbolos de entrada
dur = Ns * Ts   # Duração do sinal x(t) [s]
n_iters = 1000  # Número de realizações

letter = st.radio(
    label="Questão:",
    options=["Letra (a)", "Letra (b)"],
    horizontal=True,
)

if letter == "Letra (a)":
    u_n = rng.choice([-3, -1, 1, 3], size=(n_iters, Ns))
    pulse = komm.RectangularPulse()
    span = (-1, 1)
    psd_teo_density = lambda f: 5.0 * A**2 * Ts * np.sinc(Ts*f)**2
else:  # letter == "Letra (b)":
    α_n = rng.normal(loc=0, scale=1, size=(n_iters, Ns+1))
    u_n = α_n[:, 1:] + α_n[:, :-1]
    pulse = komm.SincPulse()
    span = (-16, 16)
    psd_teo_density = lambda f: 4.0 * A**2 * Ts * np.cos(np.pi*Ts*f)**2 * (np.abs(Ts*f) <= 0.5)

# Geração do sinal PAM
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
p_t = A * pulse.taps(samples_per_symbol=sps, span=span)
x_t = komm.convolve(p_t, u_t) * dt

# Densidade espectral de potência
X_f, f = komm.fourier_transform(x_t, time_step=dt)
psd_teo = psd_teo_density(f)
psd_sim = np.mean(np.abs(X_f) ** 2, axis=0) / dur

tabs = st.tabs(["Pulso", "Sinal PAM", "PSD"])

with tabs[0]:
    t = np.linspace(-16*Ts, 16*Ts, num=1000)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-6, A * pulse.waveform(t/Ts))
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$p(t)$ [V]")
    ax.set_ylim(-1.5, 5.5)
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    t = np.arange(x_t[0].size) * dt
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-3, x_t[0])
    ax.set_xlabel("$t$ [ms]")
    ax.set_ylabel("$x(t)$ [V]")
    ax.grid()
    st.pyplot(fig)

with tabs[2]:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(f/1e3, psd_sim, "C0", label="Simulado")
    ax.plot(f/1e3, psd_teo, "C1--", label="Teórico")
    ax.set_xlabel("$f$ [kHz]")
    ax.set_ylabel("$S_x(f)$ [V²/Hz]")
    ax.set_xlim(-2*Rs/1e3, 2*Rs/1e3)
    ax.grid()
    ax.legend()
    st.pyplot(fig)
