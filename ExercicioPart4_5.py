import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import komm


st.header("Exercicio 5 parte 4")

rng  = np.random.default_rng(seed=6)

komm.global_rng.set(rng)

M  = 16 #ordem da modulaçao 
k  = int(np.log2(M))  # Numero de bits por simbolo
P  = 100e-3    # Potencia Recebida em Watts
N0 = 1e-9      # Densidade espectral de potencia (Ber)
Rb = 8.8667e6  # Taxa de Bits/S
Rs = Rb/k      # Taxa de simbolos[Baud]
Es = P/Rs      # Energia de Simbolo
Eb = Es/k      # Energia de bit
EbN0_db = 10*np.log10(Eb/N0)  # SNR de bit [dB]
Ps = 3 * komm.gaussian_q(np.sqrt(Es/(5*N0)))
Pb_teo = Ps/k      #

Delta = np.sqrt(6*Es/(M-1))

#Simulaçao
N_bits = 100_000
source = komm.DiscreteMemorylessSource(2)
const = komm.QAMConstellation(M,Delta)
labeling = komm.ReflectedRectangularLabeling(k)
awgn = komm.GaussianChannel(noise_power=N0)
b = source.emit(N_bits)
m = labeling.bits_to_indices(b)
u = const.indices_to_symbols(m)
v = awgn.transmit(u)
m_hat = const.closest_indices(v)
b_hat = labeling.indices_to_bits(m_hat)

Pb_sim = np.mean(b != b_hat)

print(Pb_sim)


cols = st.columns(3)

with cols[0]:
    st.metric(
        label="SNR de bit ($E_b/N_0$)",
        value=f"{EbN0_db:.2f} dB"
    )

with cols[1]:
    st.metric(
        label="BER Teórica",
        value=f"{Pb_teo:.3%}"  # BER is usually very small, so scientific notation (.2e) works best
    )    

with cols[2]:
    st.metric(
        label="BER Simulada",
        value=f"{Pb_sim:.3%}"  # Changed variable to what is likely your simulated BER variable
    )
#labeling.matrix

#const.matrix



fig, ax = plt.subplots()
ax.plot(v.real/Delta,v.imag/Delta,"C1.")
ax.plot(const.matrix.real/Delta, const.matrix.imag/Delta,"C0o")
ax.set_xlabel("Re")
ax.set_ylabel("Im")
ax.set_aspect("equal")
ax.grid()  
st.pyplot(fig)
