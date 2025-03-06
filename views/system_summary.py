import streamlit as st
import pandas as pd
import plotly.express as px

def show_system_summary(network):
    st.header("System Summary")
    
    # Summary of network components
    components_summary = {
        "Component": ["Generators", "Buses", "Lines", "Links", "Loads", "Storage Units", "Stores", "Transformers"],
        "Count": [
            len(network.generators), 
            len(network.buses), 
            len(network.lines),
            len(network.links),
            len(network.loads), 
            len(network.storage_units),
            len(network.stores),
            len(network.transformers),
        ]
    }
    
    # Display network metadata
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Network Components")
        st.dataframe(pd.DataFrame(components_summary))
    
    with col2:
        st.subheader("Network Attributes")
        # Get network attributes
        snapshots = network.snapshots
        investment_periods = network.investment_periods
        st.write(f"**Number of snapshots:** {len(snapshots)}")
        st.write(f"**Investment periods:** {investment_periods}")
        if hasattr(network, 'name') and network.name:
            st.write(f"**Network name:** {network.name}")
        
        # Show time range if snapshots are timestamps
        if len(snapshots) > 0:
            st.write(f"**Time range:** {snapshots[0]} to {snapshots[-1]}")

    # Allow user to select which network component to view
    component_type = st.selectbox(
        "Select network component:",
        ["Generators", "Buses", "Lines", "Links", "Loads", "Storage Units", "Stores", "Transformers"],
    )
    
    # Get the corresponding dataframe
    component_dfs = {
        "Buses": network.buses,
        "Lines": network.lines,
        "Generators": network.generators,
        "Loads": network.loads,
        "Storage Units": network.storage_units,
        "Links": network.links,
        "Transformers": network.transformers,
        "Stores": network.stores,
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
        