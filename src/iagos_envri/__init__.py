"""
IAGOS ENVRI-ID Token Introspection Package
==========================================

This package demonstrates ENVRI-ID token introspection by the AERIS SSO system
through downloading and analyzing IAGOS atmospheric data from the SEDOO API.
"""

from .iagos_introspection import downloadOneFlight, getHeader, getHeaderOAuth

__version__ = "1.0.0"
__author__ = "AERIS Data Infrastructure"
__email__ = "support@aeris-data.fr"

__all__ = ["downloadOneFlight", "getHeader", "getHeaderOAuth"]