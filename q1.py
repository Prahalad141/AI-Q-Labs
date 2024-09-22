import streamlit as st
import requests
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector, plot_state_city
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
import imageio
import os
from qiskit_aer import AerSimulator
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def get_access_token():
    api_key = 'your api key'  # Replace with your IBM Cloud API key
    authenticator = IAMAuthenticator(api_key)
    access_token = authenticator.token_manager.get_token()
    return access_token


# Function to get generated code from IBM WatsonX.ai
def get_generated_response(prompt):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    
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
        "Authorization": f"Bearer {access_token}"  # Use the access token here
    }

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
    return response.json()  # Return the full JSON response

# Function to create the quantum circuit based on user inputs
def create_quantum_circuit(num_qubits, gate_operations):
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # Parse and apply gate operations
    operations = gate_operations.split(";")
    for op in operations:
        gate = op.strip().split()
        if gate[0] == "H":  # Hadamard
            qc.h(int(gate[1]))
        elif gate[0] == "CX":  # CNOT
            qc.cx(int(gate[1]), int(gate[2]))
        # Add more gate operations here if needed
    
    # Add a measurement step
    qc.measure(range(num_qubits), range(num_qubits))
    
    return qc

# Function to run and display the simulation with different visualization options
def simulate_quantum_circuit(qc, visualization_type, rotation_angles):
    try:
        with st.spinner('Simulating quantum circuit...'):
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
        
        st.success('Simulation completed successfully!')

    except Exception as e:
        st.error(f"An error occurred during simulation: {e}")

# Function to create a GIF showing the quantum circuit execution
def create_gif(qc, counts):
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)
    images = []
    
    for i in range(10):  # Example: create 10 frames for the GIF
        fig, ax = plt.subplots(figsize=(8, 4))
        qc.draw(output='mpl', ax=ax)
        plt.title(f"Frame {i+1}")
        file_path = f"{temp_dir}/frame_{i}.png"
        plt.savefig(file_path)
        plt.close(fig)
        images.append(imageio.imread(file_path))
    
    gif_path = "quantum_simulation.gif"
    imageio.mimsave(gif_path, images, duration=0.5)
    
    st.image(gif_path, caption="Quantum Circuit Simulation")

# Function to display example quantum circuits and their parameters
def display_example_circuit(example_number, visualization_type, rotation_angles):
    if example_number == 1:
        num_qubits = 2
        gate_operations = "H 0; CX 0 1"
    elif example_number == 2:
        num_qubits = 3
        gate_operations = "H 0; CX 0 1; CX 1 2"
    
    st.write(f"### Example Circuit {example_number} Parameters")
    st.write(f"**Number of Qubits**: {num_qubits}")
    st.write(f"**Gate Operations**: {gate_operations}")
    
    qc = create_quantum_circuit(num_qubits, gate_operations)
    st.write("### Example Quantum Circuit")
    st.write(qc.draw(output='mpl'))
    
    simulate_quantum_circuit(qc, visualization_type, rotation_angles)

# Function to encapsulate the main logic
def show():
    st.title("AI-Q Labs: Quantum Circuit Simulator")

    # A variable to track whether any sidebar button is clicked
    hide_main_content = False
    
    st.sidebar.header("Quantum Circuit Configuration")

    # User inputs for the quantum circuit
    num_qubits = st.sidebar.number_input("Number of Qubits", min_value=1, max_value=5, value=2)
    gate_operations = st.sidebar.text_area("Gate Operations inf the form of OpenQASM (e.g., 'H 0; CX 0 1')")

    # User input for visualization type
    visualization_type = st.sidebar.selectbox("Visualization Type", ["Probability Amplitude", "Bloch Sphere", "State City"])

    # User inputs for Bloch sphere rotation angles
    rotation_elev = st.sidebar.slider("Elevation Angle", min_value=0, max_value=360, value=30)
    rotation_azim = st.sidebar.slider("Azimuth Angle", min_value=0, max_value=360, value=30)

    # Display quantum circuit when button is clicked
    if st.sidebar.button("Generate Quantum Circuit"):
        hide_main_content = True
        prompt = f"give me complete code on quantum circuit simulation with qiskit and python where quantum circuit configuration is as follows: no of qubits: {num_qubits}, gate operations: {gate_operations}, visualization type: {visualization_type}."
        generated_code = get_generated_response(prompt)

        if generated_code:
            qc = create_quantum_circuit(num_qubits, gate_operations)
            st.write("### Quantum Circuit")
            st.write(qc.draw(output='mpl'))

            simulate_quantum_circuit(qc, visualization_type, (rotation_elev, rotation_azim))

            st.code(generated_code, language='python')
        else:
            st.error("Failed to generate quantum circuit from the prompt. Please check your API key and connection.")

    # Display example quantum circuits
    st.sidebar.header("Example Quantum Circuits")
    if st.sidebar.button("Example 1"):
        hide_main_content = True
        display_example_circuit(1, visualization_type, (rotation_elev, rotation_azim))
    if st.sidebar.button("Example 2"):
        hide_main_content = True
        display_example_circuit(2, visualization_type, (rotation_elev, rotation_azim))

    # Display the main content only if no button has been clicked
    if not hide_main_content:
        st.markdown('''Quantum Circuit Simulations: Visualizing and Experimenting with Quantum Circuits
Interactive Building: Users can construct quantum circuits by adding qubits and gates in a user-friendly interface, allowing for real-time experimentation.

Simulation Capabilities: The platform enables users to run simulations of their quantum circuits, observing how qubits interact and evolve through various gate operations.

Types of Visualizations:

- **Probability Amplitude**: This visualization shows the likelihood of each qubit being in a specific state after measurement, helping users understand concepts of superposition and measurement outcomes.
- **Bloch Spheres**: A geometric representation that illustrates qubit states in three-dimensional space, allowing users to visualize the effects of different quantum gates on qubit states, such as rotations and phase changes.
- **State City**: An innovative visualization method that presents quantum states in a city-like layout, making complex interactions more intuitive and engaging.

Enhanced Understanding: By exploring these visualizations, users can grasp the fundamental principles of quantum mechanics, making the learning process both interactive and accessible.

Hands-On Experimentation: The platform encourages users to experiment with different configurations, deepening their comprehension of quantum circuits and algorithms.''')

# Run the show function only if this script is executed directly
if __name__ == "__main__":
    show()
