import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Titel van de app
st.title('Archery Simulator')
st.write('Simuleer de baan van een pijl bij verschillende afschiethoeken en krachten.')

# Invoerparameters
angle = st.slider('Afschiethoek (graden)', 0, 90, 45)
force = st.slider('Spankracht (N)', 10, 100, 50)
mass = st.slider('Gewicht van het projectiel (kg)', 0.01, 0.5, 0.05)
air_resistance = st.checkbox('Luchtweerstand inschakelen')

# Constante waarden
g = 9.81  # m/s²
Cd = 0.47  # luchtweerstandscoëfficiënt voor een pijl
density = 1.225  # kg/m³
area = 0.001  # m² (frontrale oppervlakte pijl)
dt = 0.01  # tijdsstap

# Berekening van de beginsnelheid
v0 = force / mass
v0_kmh = v0 * 3.6  # m/s naar km/u

st.write(f'Beginsnelheid: {v0:.2f} m/s ({v0_kmh:.2f} km/u)')

# Berekening van de baan van de pijl
def simulate_trajectory(angle, v0, mass, air_resistance):
    theta = np.radians(angle)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)
    x, y = 0, 0
    x_points, y_points = [x], [y]

    while y >= 0:
        if air_resistance:
            v = np.sqrt(vx**2 + vy**2)
            ax = -0.5 * Cd * density * area * v * vx / mass
            ay = -g - 0.5 * Cd * density * area * v * vy / mass
        else:
            ax = 0
            ay = -g

        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        x_points.append(x)
        y_points.append(y)

    return x_points, y_points

# Traject berekenen
x_points, y_points = simulate_trajectory(angle, v0, mass, air_resistance)

# Grafiek tekenen
fig, ax = plt.subplots()
ax.plot(x_points, y_points, label=f'Hoek: {angle}°, Kracht: {force}N, Gewicht: {mass}kg')
ax.set_title('Traject van de pijl')
ax.set_xlabel('Afstand (m)')
ax.set_ylabel('Hoogte (m)')
ax.legend()

# Grafiek weergeven
st.pyplot(fig)
