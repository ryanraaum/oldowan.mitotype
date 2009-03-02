"""This is the oldowan.mitotype package."""

import os
version_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION'))
version = version_file.read().strip()
version_file.close()

__all__ = ['network'] 

try:
    from oldowan.mitotype.network import read_network_csv
    from oldowan.mitotype.network import network_haplotypes
except:
    from network import read_network_csv
    from network import network_haplotypes
