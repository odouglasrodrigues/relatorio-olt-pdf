from inspect import ClosureVars
from turtle import color
import matplotlib.pyplot as plt

faixa = ['Ótimo', 'Bom', 'Ruim']
renda = [11, 20, 29]
cor = ['#05F131', '#EAA706', '#F31616']
borda = ['255,255,0', '255,255,0', '255,255,0']
explode = (0.09, 0.02, 0.02)


plt.pie(renda, labels=faixa, colors=cor, autopct=lambda v: f"{sum(renda)*v/100:.0f} ONUs",
        explode=explode, wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True})

plt.legend(['-13 à -22', '-22 à -26', '-26 à -33'], loc=3)
plt.title(" Quantidade de ONU x Qualidade de sinal - PON X/X ", fontsize=15)
plt.axis('equal')


plt.show()
