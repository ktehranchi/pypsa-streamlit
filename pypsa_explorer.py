import streamlit as st
from _helpers.network_loader import load_network
from views.system_summary import show_system_summary
from views.temporal_view import show_temporal_view
from views.geospatial_view import show_geospatial_view
from views.config_view import show_config_view

# Set page configuration
st.set_page_config(page_title="PyPSA Network Explorer", layout="wide")

# Sidebar for file selection
st.sidebar.title("⚡ PyPSA Network Explorer")
st.sidebar.write(
    "Upload or specify a PyPSA network file to explore its components and data.",
)

# Option to select file input method
file_input_method = st.sidebar.radio(
    "Select how to load the network:",
    ["Upload NetCDF file", "Load sample network"],
)
network = load_network(file_input_method)

# Main content area - only show if network is loaded
if network is not None:
    # Navigation through different components and views
    st.sidebar.title("Navigation")
    component_options = ["System Summary", "Temporal", "Geospatial", "Metadata"]
    selected_view = st.sidebar.radio("Select view:", component_options)

    match selected_view:
        case "System Summary":
            show_system_summary(network)
        case "Temporal":
            show_temporal_view(network)
        case "Geospatial":
            show_geospatial_view(network)
        case "Metadata":
            show_config_view(network)
else:
    # Instructions when no network is loaded
    st.info("Please select a PyPSA network to explore using the sidebar options.")

    st.markdown(
        """
    ### What is PyPSA?

    **PyPSA (Python for Power System Analysis)** is a free software toolbox for simulating and optimizing modern power systems that include features such as:

    - Conventional generators with unit commitment
    - Variable renewable generation
    - Storage units
    - Sector coupling
    - Mixed AC and DC networks

    ### This Explorer Allows You To:

    - View all network components (buses, lines, generators, etc.)
    - Visualize network topology on a map
    - Analyze time series data for generation and demand
    - Explore energy balances and line utilization
    - Perform custom queries on network data

    ### Getting Started:

    1. Upload a PyPSA network file (.nc format).
    3. Alternatively, load a sample network for demonstration.
    """,
    )
