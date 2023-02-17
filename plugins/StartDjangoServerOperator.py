from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import subprocess

class StartDjangoServerOperator(BaseOperator):
    @apply_defaults
    def __init__(self, script_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.script_path = script_path

    def execute(self, context):
        subprocess.Popen(['python', self.script_path])
