import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import komm

st.header("Exercicio2")

## Simulacao de u
ti , tf = -0.1,0.1
dt = 1e-6 ## Passso do tempo em segundos

t = np.arange(ti,tf,step=dt)  # Eixo do tempo (s)
fa = st.slider(label='taxa de amostragem $f_a$',min_value=50,max_value=10,value=400,format='%d amostras/s')
#mensagem sinal
Ta = 1/fa
st.write(f"Intervalo de amostragem : $T_a = {1000*Ta:.2f} ms$")
x_t = 2 + 600*np.sinc(200*t) + 8*np.cos(2*np.pi*50*t)


#amostragem
x_n = komm.sampling_rate_compress(x_t, int(Ta/dt))
n = np.arange(0,x_n.size,step=1)

# Reconstrucao (Interpolaçao) Whittaker--shanon
x_hat_t = np.zeros_like(x_t)
for i in n:
    x_hat_t += x_n[i] * np.sinc((t -i*Ta - ti)/Ta)


fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t/1e-3, x_t, "C0", label="$x(t)$")
ax.plot(t/1e-3, x_hat_t, "C1", label="$\\hat{x}(t)$")
ax.plot((n*Ta + ti)/1e-3, x_n, "C2o")
ax.set_xlabel("$t$ [ms]")
ax.set_ylim(-300,800)
ax.legend()
ax.grid()
st.pyplot(fig)




