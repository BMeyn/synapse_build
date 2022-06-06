import pytest
import json
import os
# from src.synapse_build.models import *
from pytest_cases import parametrize_with_cases
from .test_build_client_cases import TestCases_BuildClient
from src.synapse_build.build_client import BuildClient
from operator import itemgetter

def load_test_results(output_dir):
    """
    Load expected test results from fixtures directory
    """
    # load expected config file from fixtures
    with open(os.path.join(output_dir, "test_artifacts.json"), 'r', encoding="utf-8") as f:
        artifacts_json = json.load(f)

    with open(os.path.join(output_dir, "test_parameters.json"), 'r', encoding="utf-8") as f:
        parameters_json = json.load(f)

    return artifacts_json, parameters_json

@parametrize_with_cases("success,inputs,expected", cases=TestCases_BuildClient)
def test_BuildClient(success,inputs,expected):


    client = BuildClient(
        content_version=inputs["content_version"], 
        schema=inputs["schema"], 
        source_workspace=inputs["source_workspace"],
        output_dir=inputs["output_dir"],
        synapse_root=inputs["synapse_root"])

    client.build()
    artifacts_json, parameters_json = load_test_results(inputs["output_dir"])

    expected["artifacts"]["resources"] = sorted(expected["artifacts"]["resources"], key=itemgetter('name')) 
    artifacts_json["resources"] = sorted(artifacts_json["resources"], key=itemgetter('name'))
  
    assert json.dumps(artifacts_json, sort_keys=True) == json.dumps(expected["artifacts"], sort_keys=True)
    assert json.dumps(parameters_json, sort_keys=True) == json.dumps(expected["parameters"], sort_keys=True)

