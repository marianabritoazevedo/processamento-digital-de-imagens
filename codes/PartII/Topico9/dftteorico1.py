import numpy as np
import matplotlib.pyplot as plt

tam = 256
periodos = 4

# Gerando a senoide semelhante à presente na imagem
x = np.linspace(1, 2*np.pi, tam)
y = 127 * np.sin(2 * np.pi * periodos * x) + 128

# Cálculo da DFT para a senoide
dft_resultado = np.fft.fft(y)

# Frequências correspondentes à DFT
frequencias = np.fft.fftfreq(len(y))

# Plote do sinal e do cálculo da DFT
plt.figure(figsize=(8, 6))
plt.subplot(2, 1, 1)
plt.plot(x, y)
plt.title('Sinal da senoide')
plt.xlabel('Frequência')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.stem(frequencias, np.abs(dft_resultado))
plt.title('Parte Real da Transformada de Fourier')
plt.xlabel('Frequência')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
