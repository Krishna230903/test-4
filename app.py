import streamlit as st
from database import setup_database
from auth import register_user, validate_login

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="OilFlow Logistics",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD CUSTOM CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def login_register_page():
    """Renders the login and registration form."""
    st.html(
        """
        <style>
            .login-container {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 90vh;
            }
            .login-form {
                background: rgba(14, 17, 23, 0.9);
                padding: 3rem;
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                border: 1px solid rgba(255, 255, 255, 0.18);
                width: 100%;
                max-width: 480px;
            }
            .login-form h1 {
                text-align: center;
                color: #00A9FF;
                text-shadow: 0 0 10px rgba(0, 169, 255, 0.5);
            }
        </style>
        <div class="login-container">
            <div class="login-form">
                <h1>OilFlow Logistics 🏭</h1>
            </div>
        </div>
        """
    )

    choice = st.radio("", ["Login", "Register"], horizontal=True, label_visibility="collapsed")

    if choice == "Login":
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            if st.form_submit_button("Login", use_container_width=True):
                user = validate_login(username, password)
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['user_info'] = user
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    elif choice == "Register":
        with st.form("register_form"):
            new_username = st.text_input("Username", placeholder="Choose a username")
            new_password = st.text_input("Password", type="password", placeholder="Choose a password")
            if st.form_submit_button("Register", use_container_width=True):
                if register_user(new_username, new_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists.")


# --- MAIN APP LOGIC ---
def main():
    setup_database()
    load_css('style.css')

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.sidebar.title(f"Welcome, {st.session_state['user_info']['username'].capitalize()}!")
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.switch_page("pages/1_📊_Dashboard.py")
    else:
        login_register_page()


if __name__ == "__main__":
    main()
