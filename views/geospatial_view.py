import streamlit as st
import plotly.express as px

def show_geospatial_view(network):
    st.header("Geospatial View")
    
    # Allow user to select which network component to view
    component_type = st.selectbox(
        "Select network component:",
        ["Buses", "Lines", "Generators", "Loads", "Storage Units", "Links", "Transformers"]
    )
    
    # Get the corresponding dataframe
    component_dfs = {
        "Buses": network.buses,
        "Lines": network.lines,
        "Generators": network.generators,
        "Loads": network.loads,
        "Storage Units": network.storage_units,
        "Links": network.links,
        "Transformers": network.transformers
    }
    
    df = component_dfs[component_type]
    
    if len(df) == 0:
        st.info(f"No {component_type.lower()} found in this network.")
    else:
        # Show dataframe with pagination
        st.subheader(f"{component_type} Data")
        st.dataframe(df)
        
        # Show the component on a map if coordinates are available
        if component_type == "Buses" and "x" in df.columns and "y" in df.columns:
            st.subheader("Bus Locations")
            
            fig = px.scatter_mapbox(
                df.reset_index(), 
                lat="y", 
                lon="x", 
                hover_name=df.index,
                zoom=3,
                height=500
            )
            fig.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig)
        
        # Additional component specific analysis
        if component_type == "Generators" and len(network.generators) > 0:
            st.subheader("Generator Capacity by Type")
            
            # Group generators by carrier/type
            if "carrier" in network.generators.columns:
                gen_by_carrier = network.generators.groupby("carrier").sum()
                
                if "p_nom" in gen_by_carrier.columns:
                    fig = px.pie(
                        gen_by_carrier.reset_index(), 
                        values="p_nom", 
                        names="carrier",
                        title="Installed Capacity by Generator Type"
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("Generator capacity (p_nom) information is not available.")
            else:
                st.info("Generator type information is not available.")
