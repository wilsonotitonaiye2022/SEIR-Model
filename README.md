# SEIR-Model
The SEIR model is a compartmental model that describes the dynamics of infectious diseases. The model divides the population into four compartments: Susceptible (S), Exposed (E), Infected (I), and Recovered (R). The model is governed by the following set of differential equations:

st.latex(r'''
\begin{aligned}
\frac{dS}{dt} & = -\beta \frac{S I}{N} \\
\frac{dE}{dt} & = \beta \frac{S I}{N} - \sigma E \\
\frac{dI}{dt} & = \sigma E - \gamma I \\
\frac{dR}{dt} & = \gamma I
\end{aligned}
''')

Where:
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

The model is solved using the following initial conditions:

st.latex(r'''
\begin{aligned}
S(0) & = N - I_0 - R_0 - E_0 \\
E(0) & = E_0 \\
I(0) & = I_0 \\
R(0) & = R_0
\end{aligned}
''')
