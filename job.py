from pendo_prom_emitter.aggregation import execute_aggregation
from pendo_prom_emitter.config import Config


print(f"NAMESPACE={Config.NAMESPACE} - EXECUTE_NAMESPACE={Config.EXECUTE_NAMESPACE}")  # noqa: E501

if Config.NAMESPACE == Config.EXECUTE_NAMESPACE:
    execute_aggregation()
