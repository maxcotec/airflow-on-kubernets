from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

from kubernetes.client import models as k8s

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'retries': 7,
    'retry_delay': timedelta(minutes=5),
    # KubernetesPodOperator Defaults
    'namespace': 'airflow',
    'in_cluster': True,  # if set to true, will look in the cluster, if false, looks for file
    'get_logs': True,
    'is_delete_operator_pod': True
}

dag = DAG('hello_KubePodOp',
          default_args=default_args,
          description='Kubernetes Pod Operator - Demonstration Dag',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20),
          catchup=False)

env_var = [k8s.V1EnvVar(name='FOO', value='foo'), k8s.V1EnvVar(name='BAR', value='bar')]
configmaps = [k8s.V1EnvFromSource(config_map_ref=k8s.V1ConfigMapEnvSource(name='my-configs'))]

ingest_data = KubernetesPodOperator(
            image="localhost:5001/example_app:test1",
            arguments=["ingest-data"],
            env_vars=env_var,
            env_from=configmaps,
            name=f"ingest_data",
            task_id=f"ingest_data",
            retries=5,
            retry_delay=timedelta(minutes=5),
            dag=dag,
        )

load_data = KubernetesPodOperator(
            image="localhost:5001/example_app:test1",
            arguments=["load-data"],
            name=f"load_data",
            task_id=f"load_data",
            retries=5,
            retry_delay=timedelta(minutes=5),
            dag=dag,
        )


ingest_data >> load_data