import streamlit as st
import Qna
import q1
import al1
import r1

# Add custom CSS for white transparent box
st.markdown("""
    <style>
    .content-box {
        background-color: linear-gradient(to top, #accbee%200%,%20#e7f0fd%20100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Ensure user_name is initialized in session state
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = "Guest"  # Default value or handle login

# Set up session state to track if 'Get Started' is clicked
if 'get_started' not in st.session_state:
    st.session_state['get_started'] = False  # Default: Get Started not clicked

# Initialize page state if not already done
if 'page' not in st.session_state:
    st.session_state['page'] = 'Dashboard'  # Default to dashboard

# Function to redirect to a specific page
def redirect_to_page(page_name):
    st.session_state['page'] = page_name  # Update the page in session state

# Function to display the dashboard content
# Function to display the dashboard content
def show_dashboard():
    # Start of transparent box for the entire dashboard content
    st.markdown('<div class="content-box">', unsafe_allow_html=True)

    st.title("Home")
    st.write('''Welcome to AI-Q Labs Built By AiQuantic 1.0
             Introduction to AI-Q Labs

Welcome to AI-Q Labs, developed by AiQuantic 1.0. This innovative platform combines the power of quantum computing with cutting-edge AI technologies to make quantum simulations accessible and interactive. 
            Built using Streamlit for rapid app development, the app leverages IBM Watsonx.ai featuring IBM Granite for advanced AI and machine learning capabilities.
            Utilizing Qiskit and python, it allows users to simulate and visualize complex quantum circuits effortlessly. 
            With integrated NLP features, users can engage with the platform through intuitive natural language queries.
              Join us on this exciting journey into the world of quantum computing!''')

    # Start of transparent box for features
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.subheader("Features of AI-Q Labs")
    
    features = {
        "Quantum Circuit Simulations": [
            "Visualize and experiment with quantum circuits.",
            "explore the visualizations of qubits and gates with different types of visualizations techniques"
        ],
        "Quantum Algorithms": [
            "Explore the real-time simulations of quantum algorithms.",
            "explore the visualizations of algorithms in different types of visualizations techniques"
        ]
    }

    for feature, points in features.items():
        st.write(f"### {feature}")
        for point in points:
            st.write(f"- {point}")
    
    st.markdown('</div>', unsafe_allow_html=True)  # End of transparent box for features
    st.markdown('</div>', unsafe_allow_html=True)  # End of the main transparent box



# Function to display the respective page content
def show():
    # Sidebar navigation menu
    with st.sidebar:
        st.header("Navigation")

        # Home button to redirect back to the dashboard
        if st.button("Home", key="home_button"):
            redirect_to_page('Dashboard')  # Redirect to Dashboard

        if st.button("Quantum Circuit Simulation", key="q1_button"):
            redirect_to_page("Quantum circuit simulation")
        if st.button("Quantum Algorithms", key="al1_button"):
            redirect_to_page("Quantum algorithms simulation")

    # Top-right profile button
    st.markdown('<div style="position: absolute; top: 15px; right: 15px;">', unsafe_allow_html=True)
    st.button(f"Profile: {st.session_state['user_name']}", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Render the selected page
    if st.session_state['page'] == 'Dashboard':
        show_dashboard()
    elif st.session_state['page'] == "Quantum circuit simulation":
        q1.show()
    elif st.session_state['page'] == "Quantum algorithms simulation":
        al1.show()
    

# Main function to handle the Get Started button and Home page
def main():
    st.title("Welcome to AI-Q Labs")

    # If Get Started is clicked, set the session state
    if st.button("Get Started"):
        st.session_state['get_started'] = True
        st.session_state['page'] = 'Dashboard'

    # Call the main show function to render the appropriate page
    show()

# Run the main function
if __name__ == "__main__":
    main()
