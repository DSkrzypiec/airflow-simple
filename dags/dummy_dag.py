import datetime
import logging
from random import randint

from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.sensors.base import BaseSensorOperator


class HelloOperator(BaseOperator):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def execute(self, context: dict) -> None:
        logging.info(f'About to say hello from {self.name}!')
        print(f'Hello {self.name}!')


class RandomSensor(BaseSensorOperator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def poke(self, context) -> bool:
        r = randint(3, 15)
        if r <= 13:
            logging.info(f'Got too small number {r}, still wating...')
            return False
        return True


def create_dummy_dag() -> DAG:
    with DAG(
        dag_id='dummy_dag',
        start_date=datetime.datetime(2023, 3, 22),
        schedule_interval="*/5 * * * *",
        catchup=False
    ) as dag:
        dag.doc_md = '''
        I love this DAG <3

        `var.num = 10 + 13`

        **Crap <3**
        '''
        d1 = DummyOperator(task_id='start')
        d2 = DummyOperator(task_id='task1')
        b1 = BashOperator(task_id='bash_ls', bash_command='ls -l')
        hd = HelloOperator(task_id='hello_d', name='Damian')
        random_sens = RandomSensor(task_id='random_wait', poke_interval=1, timeout=20)
        hm = HelloOperator(task_id='hello_m', name='Mark')
        finish = DummyOperator(task_id='finished')

        d1 >> [d2, b1] >> hd >> random_sens >> hm >> finish

        return dag

dummy_dag = create_dummy_dag()
