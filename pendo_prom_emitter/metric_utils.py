from prometheus_client import Gauge


def define_gauge_metric(registry, metric_obj):
    """Define a gauge metric."""
    labels_map = metric_obj.get("labels", {})
    labels = labels_map.keys()
    gauge = Gauge(
        name=metric_obj.get("metric_name"),
        documentation=metric_obj.get("description"),
        registry=registry,
        labelnames=labels,
    )
    return gauge, labels_map
