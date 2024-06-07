import streamlit as st

# Título de la aplicación
st.title("Análisis del Cambio de Combustible en Caldera")

# Parámetros de entrada en la barra lateral
st.sidebar.header("Ingrese los datos básicos")

carbon_pci = st.sidebar.number_input("PCI del carbón (kJ/kg)", value=24000)
carbon_emission_factor = st.sidebar.number_input("Factor de emisión del carbón (kg CO2/kg)", value=2.8)
caldera_capacity_bhp = st.sidebar.number_input("Capacidad de la caldera (BHP)", value=250)
caldera_efficiency_carbon = st.sidebar.number_input("Eficiencia de la caldera con carbón (%)", value=75) / 100
caldera_efficiency_gas = st.sidebar.number_input("Eficiencia de la caldera con gas natural (%)", value=85) / 100
avg_load = st.sidebar.number_input("Carga promedio (%)", value=70) / 100
operational_hours = st.sidebar.number_input("Horas de operación al año", value=6500)
carbon_price_per_ton = st.sidebar.number_input("Precio del carbón ($/ton)", value=400000)
gas_price_per_m3 = st.sidebar.number_input("Precio del gas natural ($/m³)", value=2000)
gas_pci = st.sidebar.number_input("PCI del gas natural (kJ/m³)", value=36000)
gas_emission_factor = st.sidebar.number_input("Factor de emisión del gas natural (kg CO2/m³)", value=1.8)

# Conversión de unidades y cálculos
bhp_to_kw = 9.8095
caldera_capacity_kw = caldera_capacity_bhp * bhp_to_kw
avg_operational_kw = caldera_capacity_kw * avg_load
total_energy_used_kwh = avg_operational_kw * operational_hours
total_energy_used_kj = total_energy_used_kwh * 3600

# Consumo de carbón
energy_by_carbon_kj = total_energy_used_kj / caldera_efficiency_carbon
carbon_consumption_tons = energy_by_carbon_kj / carbon_pci / 1000

# Emisiones de CO2 (carbón)
carbon_emissions_tons = carbon_consumption_tons * carbon_emission_factor

# Consumo de gas natural
energy_by_gas_kj = total_energy_used_kj / caldera_efficiency_gas
gas_consumption_m3 = energy_by_gas_kj / gas_pci

# Emisiones de CO2 (gas natural)
gas_emissions_tons = gas_consumption_m3 * gas_emission_factor / 1000

# Costo del combustible
carbon_cost = carbon_consumption_tons * carbon_price_per_ton
gas_cost = gas_consumption_m3 * gas_price_per_m3

# Diferencia de costos
cost_difference = gas_cost - carbon_cost

# Precio de las emisiones de CO2 para igualar los costos
if cost_difference > 0:
    co2_price_per_ton = cost_difference / (carbon_emissions_tons - gas_emissions_tons)
else:
    co2_price_per_ton = 0

# Mostrar resultados
st.header("Resultados del Análisis")

st.subheader("Consumo y Emisiones con Carbón")
st.write(f"- Consumo anual de carbón: {carbon_consumption_tons:.2f} toneladas")
st.write(f"- Emisiones anuales de CO2: {carbon_emissions_tons:.2f} toneladas")
st.write(f"- Costo anual del carbón: ${carbon_cost:,.2f}")

st.subheader("Consumo y Emisiones con Gas Natural")
st.write(f"- Consumo anual de gas natural: {gas_consumption_m3:.2f} m³")
st.write(f"- Emisiones anuales de CO2: {gas_emissions_tons:.2f} toneladas")
st.write(f"- Costo anual del gas natural: ${gas_cost:,.2f}")

st.subheader("Comparativa y Análisis")
st.write(f"- Reducción anual de emisiones de CO2: {carbon_emissions_tons - gas_emissions_tons:.2f} toneladas")
st.write(f"- Diferencia anual de costos (Gas Natural más caro): ${cost_difference:,.2f}")
st.write(f"- Precio necesario de las emisiones de CO2 para igualar costos: ${co2_price_per_ton:,.2f}/tonelada")
