import streamlit as st

def session_states():
    defaults = {
        #für devices
        "edit_device_id":None, 

        #für users
        "users_edit_user_id": None, 
        "users_search_result":None, 

        #für die angezeigten nachrichten
        "flash_message" : None,
        "flash_type": None, 
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def flash(message: str, msg_type: str = "success"):
    #speichert eine message im session state
    #success als default dass es nicht immer angegeben werden muss
    st.session_state["flash_message"] = message
    st.session_state["flash_type"] = msg_type

def flash_anzeigen():

    #beim rerun wird die message die gespeichert wurde gelesen und ausgegeben 

    message = st.session_state.get("flash_message")
    msg_type = st.session_state.get("flash_type")

    if message: 
        if msg_type == "success":
            st.success(message)
        elif msg_type == "error":
            st.error(message)
        else: 
            st.info(message)
        
        #nach dem anzeigen wieder auf None setzen
        st.session_state["flash_message"] = None
        st.session_state["flash_type"] = None
