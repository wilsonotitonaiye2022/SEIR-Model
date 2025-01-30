import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

#streamlit layout
st.set_page_config(layout="wide")

st.title(":chart_with_upwards_trend: SEIR Model :chart_with_downwards_trend:")



with st.sidebar:
    st.header("Parameters")
    population = st.number_input("Enter the total population", 1000, 10000000, 100000)
    beta = st.number_input("Enter the contact rate (beta)", 0.1, 1.0, 0.3)
    sigma = st.number_input("Enter the incubation rate (sigma)", 0.1, 1.0, 1/5.2)
    gamma = st.number_input("Enter the mean recovery rate (gamma)", 0.1, 1.0, 1/10)
    initial_infected = st.number_input("Enter the initial number of infected individuals", 1, 1000, 1)
    initial_recovered = st.number_input("Enter the initial number of recovered individuals", 0, 1000, 0)
    initial_exposed = st.number_input("Enter the initial number of exposed individuals", 0, 1000, 0)
    time = st.number_input("Enter the time interval (days)", 1, 3650, 365)
    run = st.button("Run Model")





st.header("Model Description")
st.write("The SEIR model is a compartmental model that describes the dynamics of infectious diseases. \
            The model divides the population into four compartments: Susceptible (S), Exposed (E), Infected (I),\
            and Recovered (R). The model is governed by the following set of differential equations:")
st.latex(r'''
\begin{aligned}
\frac{dS}{dt} & = -\beta \frac{S I}{N} \\
\frac{dE}{dt} & = \beta \frac{S I}{N} - \sigma E \\
\frac{dI}{dt} & = \sigma E - \gamma I \\
\frac{dR}{dt} & = \gamma I
\end{aligned}
''')


st.write("Where:")
st.latex(r'''
\begin{aligned}
S & = \text{Number of susceptible individuals} \\
E & = \text{Number of exposed individuals} \\
I & = \text{Number of infected individuals} \\
R & = \text{Number of recovered individuals} \\
N & = \text{Total population} \\
\beta & = \text{Contact rate} \\
\sigma & = \text{Incubation rate} \\
\gamma & = \text{Mean recovery rate}
\end{aligned}
''')

st.write("The model is solved using the following initial conditions:")
st.latex(r'''
\begin{aligned}
S(0) & = N - I_0 - R_0 - E_0 \\
E(0) & = E_0 \\
I(0) & = I_0 \\
R(0) & = R_0
\end{aligned}
''')




if run:
    # theotal population we are modeling -  N
    N = population

    # the initial number of infected and recovered individuals in our data
    I0 = initial_infected
    R0 = initial_recovered
    # the initial number of exposed individuals in our data
    E0 = initial_exposed
    # everyone else, S0, is susceptible to infection initially
    S0 = population - initial_infected - initial_exposed - initial_recovered
    # the contact rate, beta, incubation rate, sigma, and mean recovery rate, gamma
    beta, sigma, gamma = beta, sigma, gamma
    # the time points (days) over which we want to predict using our model
    t = np.linspace(0, time, time)
    # making sure the values in t are integers and not floats
    t = np.array(t, dtype=int)

    # the SEIR model differential equations
    def deriv(t, y, N, beta, sigma, gamma):
        S, E, I, R = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    # here we set the initial conditions vector
    y0 = S0, E0, I0, R0
    # and use scipy to solve the system of differential equations
    sol = solve_ivp(deriv, [0, time], y0, args=(N, beta, sigma, gamma), t_eval=t)

    # extract the results
    S, E, I, R = sol.y
    #round the values to the nearest whole number
    S = np.round(S)
    E = np.round(E)
    I = np.round(I)
    R = np.round(R)

    # plot the data on four separate curves for S(t), E(t), I(t) and R(t) using plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptible'))
    fig.add_trace(go.Scatter(x=t, y=E, mode='lines', name='Exposed'))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infected'))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recovered'))
    fig.update_layout(title="SEIR Model Dynamics", xaxis_title="Time (days)", yaxis_title="Population")
    st.plotly_chart(fig)

    st.write('--------------------------------------------------------')
    st.header("Model Results")
    st.write("The peak number of infected individuals, the day the peak occurs, the percentage of the population \
         that is infected at the peak, the percentage of the population that is susceptible at the peak, \
         the percentage of the population that is recovered at the peak, and the percentage of the population \
         that is exposed at the peak are calculated and displayed.")
    
    # Calculate the peak number of infected individuals
    peak = np.max(I)
    st.markdown(f"The peak number of infected individuals is <span style='color:red; font-weight:bold; font-size:30px'>{peak:.0f}</span>.", unsafe_allow_html=True)
    # Calculate the day the peak number of infected individuals occurs
    peak_day = np.argmax(I)
    st.write(f"The peak number of infected individuals occurs on day <span style='color:red; font-weight:bold; font-size:30px'>{peak_day}</span>.", unsafe_allow_html=True)   
    # Calculate the percentage of the population that is infected at the peak
    percent_infected_peak = peak / N * 100
    st.write(f"The percentage of the population that is infected at the peak is <span style='color:red; font-weight:bold; font-size:30px'>{percent_infected_peak:.2f}%</span>.", unsafe_allow_html=True)
    # Calculate the percentage of the population that is susceptible at the peak
    percent_susceptible_peak = np.min(S) / N * 100
    st.write(f"The percentage of the population that is susceptible at the peak is <span style='color:red; font-weight:bold; font-size:30px'>{percent_susceptible_peak:.2f}%</span>.", unsafe_allow_html=True)
    # Calculate the percentage of the population that is recovered at the peak
    percent_recovered_peak = np.max(R) / N * 100
    st.write(f"The percentage of the population that is recovered at the peak is <span style='color:red; font-weight:bold; font-size:30px'>{percent_recovered_peak:.2f}%</span>.", unsafe_allow_html=True)
    # Calculate the percentage of the population that is exposed at the peak
    percent_exposed_peak = np.max(E) / N * 100
    st.write(f"The percentage of the population that is exposed at the peak is <span style='color:red; font-weight:bold; font-size:30px'>{percent_exposed_peak:.2f}%</span>.", unsafe_allow_html=True)
 
    st.write('--------------------------------------------------------')
    st.write("The results are stored in a dataframe and displayed below.\
             The results can be downloaded as a CSV file by clicking on the top right corner of the table and clicking \
             the download icon.")

    # Create a dataframe to store the results for the SEIR model (time points (days)) and 
    # the number of individuals in each compartment (S, E, I, R)
    df = pd.DataFrame({'Time (days)': t, 'Susceptible': S, 'Exposed': E, 'Infected': I, 'Recovered': R})
    with st.expander("Click here to view the results in dataframe", expanded=False):
        st.dataframe(df)



