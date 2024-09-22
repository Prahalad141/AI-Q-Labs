import streamlit as st
# Set up the page configuration as the very first Streamlit command
st.set_page_config(page_title="AI-Q Labs", layout="wide")
import dashboard
import base64
# Function to get base64 string of images
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load images
gif = get_img_as_base64("an1.gif")
gif2 = get_img_as_base64("b2.jpg")

# Add background styling with your images and gradient
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: linear-gradient(to right, #d7d2cc 0%, #304352 100%); /* New gradient background for main content */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: black; /* Set main text color to black */
}}
[data-testid="stSidebar"] {{
    background-image: linear-gradient(-20deg, #616161 0%, #9bc5c3 100%);  /* Keep sidebar gradient unchanged */
    color: black; /* Set sidebar text color to black */
}}
[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/gif;base64,{gif}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
    right: 2rem;
}}
.transparent-box {{
    background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent white */
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    margin: 20px;
}}
footer {{
    position: relative;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent background */
    padding: 10px 0;
    text-align: center;
}}
h1 {{
    color: black; /* Set main title color to black */
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'auth_option' not in st.session_state:
    st.session_state['auth_option'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = "Guest"  # Default value for guest mode
if 'credentials' not in st.session_state:
    st.session_state['credentials'] = {}  # To store signup credentials
if 'page' not in st.session_state:  # Initialize the 'page' key
    st.session_state['page'] = 'Home'  # Default value

# Signup function - credentials stored for later login use
def signup():
    st.header("Signup")
    username = st.text_input("Username", placeholder="Enter a username")
    password = st.text_input("Password", type="password", placeholder="Enter a password")

    if st.button("Submit"):
        if username and password:
            st.session_state['credentials'][username] = password  # Store credentials
            st.success(f"User {username} signed up successfully!")
            st.session_state['logged_in'] = True
            st.session_state['user_name'] = username
            st.session_state['auth_option'] = None
        else:
            st.error("Please enter both username and password.")

# Login function - validates credentials from signup
def login():
    st.header("Login")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Submit"):
        if username in st.session_state['credentials']:
            if st.session_state['credentials'][username] == password:
                st.success(f"Welcome back, {username}!")
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = username
                st.session_state['auth_option'] = None
            else:
                st.error("Incorrect password. Please try again.")
        else:
            st.error("User not found. Please sign up first.")

# Main content area
def render_main_content():
    if st.session_state['auth_option'] == "Login":
        login()  # Call the login function directly
    elif st.session_state['auth_option'] == "Signup":
        signup()  # Call the signup function directly
    elif st.session_state['logged_in']:
        show_dashboard()  # Show dashboard when logged in
    else:
        # If guest mode or no login/signup, show the main welcome page with Get Started option
        st.markdown("""
        <div class="transparent-box">
            <h1>Welcome to AI-Q Labs</h1>
            <p>A next-generation web application designed to make quantum computing accessible and interactive for everyone.</p>
            <ul class="feature-list">
                <li>Quantum Circuit Simulations: Input and visualize quantum circuits in real-time.</li>
                <li>Quantum Algorithms: Explore and visualize how quantum algorithms work.</li>
            </ul>
        </div>
        
        <div class="transparent-box">
            <h3>Built by:</h3>
            <ul>
                <li><strong>Streamlit</strong>: Fast and intuitive data apps.</li>
                <li><strong>IBM Watsonx.ai</strong>: AI-driven computing platform.</li>
                <li><strong>IBM Granite</strong>: AI and machine learning tools.</li>
                <li><strong>Quantum Computing</strong>: Powered with Qiskit for simulating quantum circuits.</li>
                <li><strong>AI/ML</strong>: Artificial intelligence and machine learning models.</li>
                <li><strong>NLP</strong>: Natural language processing for advanced Q&A functionality.</li>
            </ul>
            <hr>
            <p>Explore the future of computing with quantum circuits, algorithms, and research powered by AI.</p>
                    <p>Sign up or log in to begin your journey into the quantum realm!</p>
        </div>
        """, unsafe_allow_html=True)

# Dashboard function
def show_dashboard():
    # Display a welcome message for both guests and logged-in users
    if st.session_state['logged_in']:
        st.write(f"Welcome, {st.session_state['user_name']}!")
    else:
        st.write(f"Welcome, Guest!")
    
    # Show the actual dashboard content
    dashboard.show()

# Footer buttons for signup and login
def footer_buttons():
    # Use a single column to stack buttons vertically
    st.markdown("""
    <style>
    .footer-button {
        background-color: black;
        color: white;
        font-size: 24px;
        padding: 15px 0; /* Increase vertical padding for larger buttons */
        border-radius: 30px;
        text-align: center;
        display: block; /* Ensure buttons take full width */
        width: 100%; /* Make buttons full-width */
        transition: background-color 0.3s ease;
        cursor: pointer;
        border: none; /* Remove default border */
    }
    .footer-button:hover {
        background-color: #333; /* Change color on hover */
    }
    </style>
    """, unsafe_allow_html=True)

    # Button for Signup
    if st.button("Signup", key="footer_signup", disabled=st.session_state['auth_option'] == "Signup"):
        st.session_state['auth_option'] = "Signup"

    # Button for Login
    if st.button("Login", key="footer_login", disabled=st.session_state['auth_option'] == "Login"):
        st.session_state['auth_option'] = "Login"

# Main control flow
if st.session_state['logged_in']:
    show_dashboard()
else:
    render_main_content()
    footer_buttons()  # Add footer buttons

# Call the sidebar function to display the info
def display_sidebar_info():
    
    st.sidebar.image("logo1.png", use_column_width=True)
   

display_sidebar_info()
