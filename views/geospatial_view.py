import streamlit as st
import plotly.express as px
import pydeck as pdk
import logging
import random


def show_geospatial_view(network):
    st.header("Geospatial View")

    # Allow user to select which network component to view
    component_type = st.selectbox(
        "Select network component:",
        [
            "Buses",
            "Lines",
            "Generators",
            "Loads",
            "Storage Units",
            "Links",
            "Transformers",
        ],
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
                height=500,
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
                        title="Installed Capacity by Generator Type",
                    )
                    st.plotly_chart(fig)
                else:
                    st.info("Generator capacity (p_nom) information is not available.")
            else:
                st.info("Generator type information is not available.")

        # Add a PyDeck map for visualization
        if "x" in df.columns and "y" in df.columns:
            st.subheader("Map Visualization")

            map_data = df.rename(columns={"x": "lon", "y": "lat"})

            # Add p_nom for elevation if available, otherwise use a constant value
            if "p_nom" in map_data.columns:
                logging.info("Using p_nom for elevation")
                map_data["elevation"] = map_data["p_nom"]
                max_elevation = max(
                    1,
                    map_data["elevation"].max(),
                )  # Avoid division by zero
                map_data["elevation_normalized"] = (
                    map_data["elevation"] / max_elevation * 1000
                )
            else:
                map_data["elevation_normalized"] = 100  # Default elevation

            # Convert latitude and longitude to a format pydeck can use
            map_data = map_data.reset_index()

            # Define color mapping based on carrier type
            def get_carrier_color(carrier):
                """Return RGB color based on carrier type"""
                carrier_colors = {
                    "nuclear": [10, 230, 120],
                    "onwind": [52, 152, 219],
                    "solar": [241, 196, 15],
                    "hydro": [41, 128, 185],
                    "gas": [230, 126, 34],
                    "CCGT": [127, 140, 141],
                    "OCGT": [117, 130, 141],
                    "coal": [17, 10, 161],
                    "oil": [192, 57, 43],
                    "biomass": [39, 174, 96],
                    "geothermal": [142, 68, 173],
                }
                carrier_str = str(carrier).lower()
                if carrier_str in carrier_colors:
                    return carrier_colors[carrier_str]
                else:
                    # Generate a random color for unknown carrier types
                    # Using seed based on carrier name for consistency
                    random.seed(carrier_str)
                    return [
                        random.randint(50, 250),
                        random.randint(50, 250),
                        random.randint(50, 250),
                    ]

            # Check if carrier column exists and apply colors
            if "carrier" in map_data.columns:
                map_data["color"] = map_data["carrier"].apply(get_carrier_color)
                get_color = "color"
            else:
                get_color = [255, 140, 0]

            st.pydeck_chart(
                pdk.Deck(
                    map_style=None,
                    initial_view_state=pdk.ViewState(
                        latitude=map_data["lat"].mean(),
                        longitude=map_data["lon"].mean(),
                        zoom=5,
                        pitch=50,
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=map_data,
                            pickable=True,
                            opacity=0.8,
                            stroked=True,
                            filled=True,
                            radius_scale=30,
                            radius_min_pixels=1,
                            radius_max_pixels=100,
                            line_width_min_pixels=1,
                            get_position=["lon", "lat"],
                            get_radius="elevation_normalized",
                            get_fill_color=get_color,
                            get_line_color=[0, 0, 0],
                        ),
                    ],
                ),
            )
