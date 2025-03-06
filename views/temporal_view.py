import streamlit as st
import plotly.express as px
import pandas as pd

def show_temporal_view(network):
    st.header("Temporal View")
    
    # Select which type of time series to explore
    ts_component_type = st.selectbox(
        "Select time series component:",
        ["Generators", "Loads", "Storage Units", "Lines", "Buses"]
    )
    
    # Handle different component types
    if ts_component_type == "Generators" and hasattr(network, "generators_t"):
        # Select which generator time series to view
        ts_attribute = st.selectbox(
            "Select time series attribute:",
            ["p", "q", "p_max_pu", "p_min_pu"]
        )
        
        attr_name = f"{ts_attribute}"
        if hasattr(network.generators_t, attr_name) and len(getattr(network.generators_t, attr_name)) > 0:
            ts_df = getattr(network.generators_t, attr_name)
            
            # Ensure all columns have the same length
            ts_df = ts_df.dropna(axis=1, how='all')
            
            # Select specific generators or aggregate
            if len(ts_df.columns) > 1:
                # Offer option to view individual generators or aggregated
                view_option = st.radio(
                    "View option:",
                    ["Individual generators", "Aggregate by type", "Sum all generators"]
                )
                
                if view_option == "Individual generators":
                    # Select which generators to plot
                    selected_gens = st.multiselect(
                        "Select generators to plot:",
                        ts_df.columns,
                        default=[ts_df.columns[0]]
                    )
                    
                    if selected_gens:
                        # Ensure selected generators have consistent lengths
                        ts_df = ts_df[selected_gens].dropna()
                        
                        # Plot the selected generators
                        fig = px.line(
                            ts_df,
                            x=ts_df.index,
                            y=selected_gens,
                            title=f"Generator {attr_name} time series"
                        )
                        st.plotly_chart(fig)
                    else:
                        st.info("Please select at least one generator to plot.")
                
                elif view_option == "Aggregate by type":
                    # Get generator types
                    if "carrier" in network.generators.columns:
                        # Group generators by type
                        carrier_groups = {}
                        for gen in ts_df.columns:
                            if gen in network.generators.index:
                                carrier = network.generators.loc[gen, "carrier"]
                                if carrier not in carrier_groups:
                                    carrier_groups[carrier] = []
                                carrier_groups[carrier].append(gen)
                        
                        # Aggregate each group
                        agg_df = pd.DataFrame(index=ts_df.index)
                        for carrier, gens in carrier_groups.items():
                            agg_df[carrier] = ts_df[gens].sum(axis=1)
                        
                        # Ensure aggregated data has consistent lengths
                        agg_df = agg_df.dropna()
                        
                        # Plot aggregated data
                        fig = px.line(
                            agg_df,
                            x=agg_df.index,
                            y=agg_df.columns,
                            title=f"Generator {attr_name} by type"
                        )
                        st.plotly_chart(fig)
                    else:
                        st.info("Generator type (carrier) information is not available.")
                
                elif view_option == "Sum all generators":
                    # Sum all generators
                    total_series = ts_df.sum(axis=1).dropna()
                    
                    # Plot total
                    fig = px.line(
                        x=total_series.index,
                        y=total_series.values,
                        title=f"Total Generator {attr_name}"
                    )
                    st.plotly_chart(fig)
            else:
                # Only one generator, just plot it
                fig = px.line(
                    ts_df,
                    x=ts_df.index,
                    y=ts_df.columns,
                    title=f"Generator {attr_name} time series"
                )
                st.plotly_chart(fig)
        else:
            st.info(f"No {attr_name} time series data available for generators.")
    
    elif ts_component_type == "Loads" and hasattr(network, "loads_t"):
        # Similar structure for loads
        ts_attribute = st.selectbox(
            "Select time series attribute:",
            ["p", "q"]
        )
        
        attr_name = f"{ts_attribute}"
        if hasattr(network.loads_t, attr_name) and len(getattr(network.loads_t, attr_name)) > 0:
            ts_df = getattr(network.loads_t, attr_name)
            
            # Ensure all columns have the same length
            ts_df = ts_df.dropna(axis=1, how='all')
            
            # Option to view individual loads or total
            view_option = st.radio(
                "View option:",
                ["Individual loads", "Total load"]
            )
            
            if view_option == "Individual loads":
                # Select which loads to plot
                selected_loads = st.multiselect(
                    "Select loads to plot:",
                    ts_df.columns,
                    default=[ts_df.columns[0]] if len(ts_df.columns) > 0 else []
                )
                
                if selected_loads:
                    # Ensure selected loads have consistent lengths
                    ts_df = ts_df[selected_loads].dropna()
                    
                    # Plot the selected loads
                    fig = px.line(
                        ts_df,
                        x=ts_df.index,
                        y=selected_loads,
                        title=f"Load {attr_name} time series"
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("Please select at least one load to plot.")
            else:
                # Sum all loads
                total_series = ts_df.sum(axis=1).dropna()
                    
                # Plot total
                fig = px.line(
                    x=total_series.index,
                    y=total_series.values,
                    title=f"Total Load {attr_name}"
                )
                st.plotly_chart(fig)
        else:
            st.info(f"No {attr_name} time series data available for loads.")
    
    # Similar blocks could be added for other component types
    
    else:
        st.info(f"No time series data available for {ts_component_type}.")
