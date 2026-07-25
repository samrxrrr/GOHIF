from pathlib import Path
import yaml

from gae.workflow.models import Workflow

from gae.cli.main import main


class WorkflowRunner:

    def run(self, workflow_file: str):

        data = yaml.safe_load(
            Path(workflow_file).read_text()
        )

        workflow = Workflow.model_validate(data)

        print(f"Workflow: {workflow.name}")

        for manifest in workflow.manifests:

            print("-" * 60)

            print("Running:", manifest)

            main([manifest])
