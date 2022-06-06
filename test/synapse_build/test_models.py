import pytest
from src.synapse_build.models import *
from pytest_cases import parametrize_with_cases
from .test_models_cases import TestCases_DeploymentArtifacts, TestCases_DeploymentParameters,TestCases_ParameterConfig


@parametrize_with_cases("success,inputs,expected", cases=TestCases_DeploymentArtifacts)
def test_DeploymentArtifacts(success,inputs,expected):
    
    if success:
        # test for successful run
        deployment_artifacts = DeploymentArtifacts(
            content_version=inputs["content_version"],
            schema=inputs["schema"],
            source_workspace=inputs["source_workspace"] )
        assert deployment_artifacts.to_json() == expected
        
    elif not success:        
        
        # test error handling
        with pytest.raises(expected["error"], match=expected["message"]):
            deployment_artifacts = DeploymentArtifacts(
                content_version=inputs["content_version"],
                schema=inputs["schema"],
                source_workspace=inputs["source_workspace"] )

@parametrize_with_cases("inputs,expected", cases=TestCases_DeploymentParameters)
def test_DeploymentParameters(inputs, expected):

    deployment_parameters = DeploymentParameters(
        content_version=inputs["content_version"] ,
        schema=inputs["schema"],
        source_workspace=inputs["source_workspace"] )

    assert deployment_parameters.to_json() == expected


@parametrize_with_cases("inputs,expected", cases=TestCases_ParameterConfig)
def test_ParameterConfig(inputs, expected):

    # initialize ParameterConfig
    config = ParameterConfig(config_path=inputs)

    print(config.to_json())

    assert config.to_json() == expected