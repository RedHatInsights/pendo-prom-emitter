import json

import requests
from prometheus_client import push_to_gateway

from .config import Config
from .config import REGISTRY
from .filter_utils import operation_equal
from .filter_utils import operation_in
from .filter_utils import operation_startswith
from .metric_utils import define_gauge_metric


SUPPORTED_OPERATIONS_MAP = {
    "equal": operation_equal,
    "in": operation_in,
    "startswith": operation_startswith,
}  # noqa: E501

METRIC_TYPE_MAP = {"gauge": define_gauge_metric}


def exec_filter(value, filter_spec):
    """Execute filter against value to determine true or false."""
    for operation, test in filter_spec.items():
        op = SUPPORTED_OPERATIONS_MAP.get(operation)
        if not op(value, test):
            return False
    return True


def filter_item(item, filter_obj):
    """Return item if filter matches."""
    if filter_obj is None:
        return item

    for key, filter_specs in filter_obj.items():
        item_val = item.get(key)
        if item_val is None:
            return None
        for filter_spec in filter_specs:
            if not exec_filter(item_val, filter_spec):
                return None
    return item


def define_metric(registry, metrics_map):
    """Define prometheus metrics."""
    metric_dict = {}
    for key, metric_obj in metrics_map.items():
        metric_type = metric_obj.get("type")
        metric_op = METRIC_TYPE_MAP.get(metric_type)
        if metric_op:
            metric, labels_map = metric_op(registry, metric_obj)
            metric_dict[key] = {"metric": metric, "labels_map": labels_map}
    return metric_dict


def execute_aggregation():
    """Run aggregation against pendo API."""

    if Config.PENDO_INTEGRATION_KEY is None:
        print("PENDO_INTEGRATION_KEY must be specified.")
        exit(-1)
    if Config.PENDO_AGGREGATION_QUERY is None:
        print("PENDO_AGGREGATION_QUERY must be specified.")
        exit(-1)

    metrics_map = json.loads(Config.PROMETHEUS_METRICS_MAP)
    metrics = define_metric(REGISTRY, metrics_map)

    url = "https://app.pendo.io/api/v1/aggregation"
    headers = {
        "X-Pendo-Integration-Key": Config.PENDO_INTEGRATION_KEY,
        "Content-Type": "application/json",
    }  # noqa: E501
    response = requests.post(url, data=Config.PENDO_AGGREGATION_QUERY, headers=headers, timeout=60)  # noqa: E501
    agg_filter = None
    if Config.PENDO_AGGREGATION_FILTER:
        agg_filter = json.loads(Config.PENDO_AGGREGATION_FILTER)
    if response.status_code == requests.codes.ok:
        out = response.json()
        results = out.get("results", [])
        for item in results:
            if filter_item(item, agg_filter):
                for metric_name, metric_dict in metrics.items():
                    metric_value = item.get(metric_name)
                    prom_obj = metric_dict.get("metric")
                    labels_map = metric_dict.get("labels_map")
                    prom_labels = {}
                    for label_key, label_ref in labels_map.items():
                        label_value = None
                        if label_key == "namespace":
                            label_value = Config.NAMESPACE
                        else:
                            label_value = item.get(label_ref)
                        if label_value is not None:
                            prom_labels[label_key] = str(label_value)
                    prom_obj.labels(**prom_labels).set(int(metric_value))
                    print(f"{metric_name} - {prom_labels} = {int(metric_value)}")  # noqa: E501
    else:
        print(f"Error occurred during processing: {response.text}")

    if Config.PROMETHEUS_PUSH_GATEWAY:
        push_to_gateway(
            Config.PROMETHEUS_PUSH_GATEWAY,
            job="pendo_metrics",
            registry=REGISTRY,
            timeout=Config.PROMETHEUS_PUSH_GATEWAY_TIMEOUT,
        )
