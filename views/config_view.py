import streamlit as st
import yaml

def show_config_view(network):
    st.title("Network Configuration")
    st.write("Below is the configuration YAML dictionary stored in the network:")

    config_dict = network.meta
    config_yaml = yaml.dump(config_dict, default_flow_style=False)
    
    st.code(config_yaml, language='yaml')
