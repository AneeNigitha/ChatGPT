# setup_st.py

import streamlit as st

# 1. Set up the page styling using a column layout
def set_design():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("logo.png", use_column_width=True) # Load an image in from your directly and center it in the middle

    st.markdown("<p style='text-align: center; font-size: 16px;'><b>[YOUR TITLE HERE]</b></p>", unsafe_allow_html=True)

# 2. Initialize session state variables (illustrative list, not complete)
def initialize_session_state():
# Can be used to guide the chatbot through pre-defined stages / steps
if 'current_stage_index' not in st.session_state:
    st.session_state['current_stage_index'] = 0
# Can be used to make the chatbot end the convo or perform an action when some limit is reached
if 'message_count' not in st.session_state:
    st.session_state['message_count'] = 0
# Initializes the model_name session state variable
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = ""
# Initializes the temperature session state variable
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = []

# 3. Initialize your sidebar
def sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { 
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True) # Optional HTML which hides the sidebar in your app upon load
    
    st.markdown('#') # Adds an empty space
    global logo_placeholder
    logo_placeholder = st.sidebar.empty() 
    static_logo()
    st.sidebar.markdown("""
    <h1 style='color: black; font-size: 28px;'>CoPilot Configuration</h1>
    """, unsafe_allow_html=True)

# 4. Setup clear button on the sidebar. Known bug that initial message disappears after first input post-clear
def clear_button():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    # Clear the conversation
    if clear_button:
        # Clear the conversation
        st.session_state['history'] = []
        st.session_state['initial_message'] = get_initial_message()
        st.session_state['messages'] = [
            {"role": "system", "content": st.session_state['initial_message']}
        ]
        with st.chat_message("assistant", avatar=bruce) as chat:
            st.markdown(st.session_state['initial_message'])
        st.session_state['current_stage_index'] = 0
        st.session_state['message_count'] = 0
        st.session_state['messages_per_stage'] = {stage: 0 for stage in stages}
        st.session_state['completed'] = False

# 5. Setup download_convo function to track the conversation for download functionality
def download_convo():
    if 'messages' in st.session_state and len(st.session_state['messages']) > 0:
        full_conversation = "\n".join([
            f"\n{'-'*20}\n"
            f"Role: {msg['role']}\n"
            f"{'-'*20}\n"
            f"{msg['content']}\n"
            for msg in st.session_state['messages']
        ])
        return full_conversation
    else:
        st.warning("There aren't enough messages in the conversation to download it. Please refresh the page")
        return ""

# 6. Setup download button
def download_button():
    full_conversation = download_convo()  # Get the full_conversation string
    st.sidebar.download_button(
        label="Download conversation",
        data=full_conversation,
        file_name='conversation.txt',
        mime='text/plain'
    )

#7.  This function is designed to capture the user's preferences for how the chatbot should respond. Possibilities here are endless!
def get_user_config():
    # Define a few AI models the user can choose from.
    model_options = {
        "GPT-3.5 Turbo (16K tokens)": "gpt-3.5-turbo-16k-0613", # Recommended as it has a 16K token limit, much higher than the other two. This allows longer 'memory recall'.
        "GPT-3.5 Turbo": "gpt-3.5-turbo", # Fewer token version of above - not recommended
        "GPT-4": "gpt-4" # Latest model from OpenAI. Recommended for complex chatbots, though has a lower token limit.
    }

    # Display button choices in the sidebar of the app for the user to pick their desired model from the ones just defined.
    st.sidebar.markdown("<b style='color: darkgreen;'>Choose a GPT model:</b>", unsafe_allow_html=True) # HTML for beautifying the label, not necessary
    # Create the radio button. Label is hidden (since we have HTMl label), it defaults to the first option (turbo 16k) of the model_options above.
    model_name = st.sidebar.radio("", list(model_options.keys()), index=0, label_visibility="collapsed") 

    # Display button choices for the user to pick a validation mode. My implementation of this function changes the 'rigor' of the idea validation.
    st.sidebar.markdown("<b style='color: darkgreen;'>Choose a validation mode:</b>", unsafe_allow_html=True)
    mode = st.sidebar.radio("", ("Standard", "Tough", "Easy"), index=0, label_visibility="collapsed")

    # Display a slider option for the user to choose 'temperature' or randomness of the chatbot responses. Higher values are recommended for creative chatbots.
    st.sidebar.markdown("<b style='color: darkgreen;'>Choose a temperature (randomness):</b>", unsafe_allow_html=True)
    temperature = st.sidebar.slider("", min_value=0.1, max_value=1.0, value=0.3, step=0.1, label_visibility="collapsed")

    # Save the user choices to the Streamlit 'memory'. These choices are saved and will affect the chatbot unless changed.
    st.session_state['model_name'] = model_options[model_name]
    st.session_state['temperature'] = temperature
    st.session_state['mode'] = mode