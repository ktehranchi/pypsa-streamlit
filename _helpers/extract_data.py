import pypsa

def extract_data(network: pypsa.Network):
    stats = network.statistics()
    return stats