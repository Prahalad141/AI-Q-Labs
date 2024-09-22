import streamlit as st
import requests
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector, plot_state_city, plot_state_hinton
from qiskit.quantum_info import Statevector, DensityMatrix
import matplotlib.pyplot as plt
import imageio
import os
from qiskit_aer import AerSimulator
import numpy as np
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Add custom CSS for white transparent box
st.markdown("""
    <style>
    .content-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def get_access_token():
    api_key = 'your api key'  # Replace with your IBM Cloud API key
    authenticator = IAMAuthenticator(api_key)
    access_token = authenticator.token_manager.get_token()
    return access_token

def get_generated_response(algorithm_name, visualization_type):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    
    prompt = f"Generate a quantum circuit for the algorithm: {algorithm_name} with visualization type: {visualization_type}."
    
    body = {
        "input": f"""{prompt}""",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "repetition_penalty": 1.05
        },
        "model_id": "ibm/granite-13b-chat-v2",
        "project_id": "f21d24eb-028e-4a62-ba68-0e6d907e031d"
    }

    access_token = get_access_token()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    return response.json()  # Return the full JSON response

def display_algorithm_info(algorithm_name):
    st.subheader(f"Information about {algorithm_name}")
    
    info = {
        "Quantum Teleportation": {
            "definition": "Quantum teleportation is a method of transferring quantum information from one qubit to another.",
            "features": "Instantaneous transfer of quantum states, requires entanglement.",
            "advantages": "Can transmit quantum information over long distances without physically moving particles.",
            "disadvantages": "Requires a classical communication channel, not faster than the speed of light."
        },
        "Grover's Search Algorithm": {
            "definition": "Grover's algorithm provides a quadratic speedup for unstructured search problems.",
            "features": "Effective for searching unsorted databases.",
            "advantages": "Offers a speedup for large database searches compared to classical methods.",
            "disadvantages": "Not exponentially faster; requires a high-quality quantum computer."
        },
        "Deutsch-Josza Algorithm": {
            "definition": "A quantum algorithm that solves the Deutsch problem with fewer queries.",
            "features": "Exponential speedup over classical counterparts.",
            "advantages": "Solves the problem in one query.",
            "disadvantages": "Only applicable to a specific type of problem."
        },
        "Shor's Algorithm": {
            "definition": "An algorithm for integer factorization that runs in polynomial time.",
            "features": "Exponential speedup for factoring large numbers.",
            "advantages": "Impacts cryptography by threatening RSA encryption.",
            "disadvantages": "Requires a large number of qubits."
        },
        "Quantum Fourier Transform": {
            "definition": "A quantum version of the discrete Fourier transform.",
            "features": "Used in many quantum algorithms.",
            "advantages": "Can be exponentially faster than classical counterparts.",
            "disadvantages": "Complex implementation."
        },
    }

    if algorithm_name in info:
        st.write(f"**Definition**: {info[algorithm_name]['definition']}")
        st.write(f"**Features**: {info[algorithm_name]['features']}")
        st.write(f"**Advantages**: {info[algorithm_name]['advantages']}")
        st.write(f"**Disadvantages**: {info[algorithm_name]['disadvantages']}")
    else:
        st.write("Information for this algorithm is not available.")

def create_quantum_circuit(algorithm_name):
    qc = QuantumCircuit(5, 5)  # Set a default number of qubits
    if algorithm_name == "Quantum Teleportation":
        qc.h(0)
        qc.cx(0, 1)
        qc.cx(1, 2)
        qc.measure([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    elif algorithm_name == "Grover's Search Algorithm":
        qc.h([0, 1, 2])
        qc.cx(0, 1)
        qc.cx(1, 2)
        qc.x(2)
        qc.h(2)
        qc.cx(0, 2)
        qc.h(2)
        qc.measure([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    elif algorithm_name == "Deutsch-Josza Algorithm":
        qc.h(0)
        qc.h(1)
        qc.cx(0, 1)
        qc.h(0)
        qc.measure(0, 0)
    elif algorithm_name == "Shor's Algorithm":
        # Add Shor's specific gates (for simplicity, keeping it basic)
        qc.h([0, 1, 2, 3])
        qc.measure(range(4), range(4))
    elif algorithm_name == "Quantum Fourier Transform":
        # Add QFT gates (simplified)
        qc.h([0, 1, 2])
        qc.measure(range(3), range(3))
    else:
        st.error("Selected algorithm not implemented.")
    return qc

def simulate_quantum_algorithm(qc, visualization_type, rotation_angles):
    try:
        with st.spinner('Simulating quantum algorithm...'):
            simulator = AerSimulator()
            transpiled_circuit = transpile(qc, simulator)
            result = simulator.run(transpiled_circuit).result()
            counts = result.get_counts()

            if visualization_type == "Probability Amplitude":
                hist = plot_histogram(counts)
                st.pyplot(hist)

            elif visualization_type == "Bloch Sphere":
                state = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
                bloch_sphere = plot_bloch_multivector(state)
                ax = bloch_sphere.gca()
                ax.view_init(elev=rotation_angles[0], azim=rotation_angles[1])
                st.pyplot(bloch_sphere)

            elif visualization_type == "State City":
                state = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
                state_city = plot_state_city(state)
                st.pyplot(state_city)

            elif visualization_type == "Density Matrix":
                density_matrix = counts_to_density_matrix(counts, qc.num_qubits)
                hinton = plot_state_hinton(density_matrix)
                st.pyplot(hinton)

        st.success('Simulation completed successfully!')

    except Exception as e:
        st.error(f"An error occurred during simulation: {e}")

def counts_to_density_matrix(counts, num_qubits):
    num_states = 2 ** num_qubits
    density_matrix = np.zeros((num_states, num_states), dtype=complex)
    total_counts = sum(counts.values())
    probabilities = {k: v / total_counts for k, v in counts.items()}
    
    for key, prob in probabilities.items():
        i = int(key, 2)
        density_matrix[i, i] = prob
    
    return DensityMatrix(density_matrix)

def show():
    st.title("Quantum Algorithm Simulation")

    page = st.sidebar.radio("Select Page", ["Information", "Quantum Algorithm Functionality"])

    if page == "Information":
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("""
        This feature leverages cutting-edge technologies to provide an interactive platform for exploring quantum algorithms through visualizations and simulations.
        ## Main Features
        - **Quantum Circuit Creation**: Users can design custom quantum circuits by specifying the algorithm.
        - **Visualization Options**: The feature supports multiple visualization types, enabling users to gain insights into quantum states and operations.
        - **Example Algorithms**: The feature includes predefined examples of popular quantum algorithms.
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Quantum Algorithm Functionality":
        st.sidebar.header("Quantum Algorithm Configuration")

        top_5_algorithms = [
            "Quantum Teleportation",
            "Grover's Search Algorithm",
            "Deutsch-Josza Algorithm",
            "Shor's Algorithm",
            "Quantum Fourier Transform",
        ]
        
        algorithm_name = st.sidebar.selectbox("Select Quantum Algorithm", top_5_algorithms + ["Other Algorithms Coming Soon"])
        visualization_type = st.sidebar.selectbox("Select Visualization Type", ["Probability Amplitude", "Bloch Sphere", "State City"])

        elevation = st.sidebar.slider("Elevation Angle (Bloch Sphere)", min_value=0, max_value=180, value=30)
        azimuth = st.sidebar.slider("Azimuth Angle (Bloch Sphere)", min_value=0, max_value=360, value=30)

        if st.sidebar.button("Run Selected Algorithm"):
            if algorithm_name == "Other Algorithms Coming Soon":
                st.warning("Stay tuned for more algorithms!")
            else:
                display_algorithm_info(algorithm_name)
                try:
                    # Get generated response from API
                    generated_code = get_generated_response(algorithm_name, visualization_type)
                    st.code(generated_code, language='python')
                    
                    # Create the quantum circuit based on the selected algorithm
                    qc = create_quantum_circuit(algorithm_name)
                    if qc:
                        st.write("### Quantum Circuit")
                        st.write(qc.draw(output='mpl'))
                        simulate_quantum_algorithm(qc, visualization_type, (elevation, azimuth))
                except Exception as e:
                    st.error(f"An error occurred while generating the algorithm: {e}")

if __name__ == "__main__":
    show()
