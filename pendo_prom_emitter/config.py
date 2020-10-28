"""Configuration loader for application."""
import logging
import os

from prometheus_client import CollectorRegistry

LOG = logging.getLogger(__name__)
REGISTRY = CollectorRegistry()


# pylint: disable=too-few-public-methods,simplifiable-if-expression
class Config:
    """Configuration for app."""

    NAMESPACE = os.getenv("NAMESPACE")
    PROMETHEUS_PUSH_GATEWAY = os.getenv("PROMETHEUS_PUSH_GATEWAY")
    PROMETHEUS_METRICS_MAP = os.getenv("PROMETHEUS_METRICS_MAP")

    PENDO_INTEGRATION_KEY = os.getenv("PENDO_INTEGRATION_KEY")
    PENDO_AGGREGATION_QUERY = os.getenv("PENDO_AGGREGATION_QUERY")
    PENDO_AGGREGATION_FILTER = os.getenv("PENDO_AGGREGATION_FILTER")
