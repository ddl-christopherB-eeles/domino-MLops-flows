"""
DOM-76273 demo flow: Flows custom types serialized via msgpack fail to render.

The bug: when a Flows task passes a custom typed input (dataclass), Flytekit
serializes it via msgpack. The current train-flyte-library only expects
msgpack input. When FLYTE_USE_OLD_DC_FORMAT=true switches Flytekit back to
the legacy JSON/Protobuf Struct format, train-flyte-library cannot decode it
and the task fails to render.

This flow demonstrates both paths in sequence:
  1. Dataclass input task — exercises the buggy msgpack/Struct path
  2. Untyped dict input task — control path, unaffected by the bug
"""

from dataclasses import dataclass
from typing import Any, Dict, List

from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

# Random comment
@dataclass
class ModelMetadata:
    """
    Custom typed input to exercise the msgpack/Struct serialization path
    described in DOM-76273.
    """

    model_name: str
    version: int
    tags: List[str]

# Dummy comment
@workflow
def dom_76273_serialization_demo():
    """
    DOM-76273 demo: runs a dataclass-input task followed by a dict-input task
    in the same flow so the serialization difference is visible side-by-side
    in the execution graph.

    Task 1 (dataclass): Flytekit serializes ModelMetadata via msgpack.
      With FLYTE_USE_OLD_DC_FORMAT=true this switches to JSON/Struct and
      train-flyte-library fails to decode it — the bug.

    Task 2 (dict): Dict inputs use the generic JSON/Struct path and render
      correctly regardless of the flag — the control.
    """
    dataclass_task = DominoJobTask(
        name="DOM-76273 Dataclass Input Task",
        domino_job_config=DominoJobConfig(Command="python dom_76273_dummy_task.py"),
        inputs={"metadata": ModelMetadata},
        outputs={"result": str},
        use_latest=True,
    )
    dataclass_task(
        metadata=ModelMetadata(
            model_name="xgboost",
            version=3,
            tags=["demo", "dom-76273", "dataclass"],
        )
    )

    dict_task = DominoJobTask(
        name="DOM-76273 Untyped Dict Input Task",
        domino_job_config=DominoJobConfig(Command="python dom_76273_dummy_task.py"),
        inputs={"metadata": dict},
        outputs={"result": str},
        use_latest=True,
    )
    dict_task(
        metadata={
            "model_name": "xgboost",
            "version": 3,
            "tags": ["demo", "dom-76273", "untyped-dict"],
        }
    )
