import pypsa
import streamlit as st


def load_network(file_input_method, uploaded_file=None, file_path=None):
    network = None

    match file_input_method:
        case "Upload NetCDF file":
            uploaded_file = st.sidebar.file_uploader(
                "Upload a PyPSA network file (.nc)",
                type=["nc"],
            )
            if uploaded_file:
                try:
                    # Save the uploaded file temporarily
                    with open("temp_network.nc", "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Load the network from the saved file
                    network = pypsa.Network("temp_network.nc")
                    st.sidebar.success("Network loaded successfully!")
                except Exception as e:
                    st.sidebar.error(f"Error loading network: {e}")

        case "Load sample network":
            options = ["ac_dc_meshed", "scigrid_de", "storage_hvdc"]
            # Let user select which sample network to load
            selected_example = st.sidebar.selectbox("Select sample network", options)

            try:
                match selected_example:
                    case "ac_dc_meshed":
                        network = pypsa.examples.ac_dc_meshed()
                    case "scigrid_de":
                        # breakpoint()
                        network = pypsa.examples.scigrid_de()
                    case "storage_hvdc":
                        network = pypsa.examples.storage_hvdc()
                    case _:
                        st.sidebar.error(f"Unknown sample network: {selected_example}")
                        return None
            except Exception as e:
                st.sidebar.error(f"Error loading sample network: {e}")

        case _:
            st.sidebar.error(f"Unknown file input method: {file_input_method}")

    if network is not None:
        network.generators["x"] = network.generators.bus.map(network.buses.x)
        network.generators["y"] = network.generators.bus.map(network.buses.y)

    return network
