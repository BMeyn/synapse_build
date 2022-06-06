import json
import os

class TestCases_DeploymentArtifacts():

    def case_1_DeploymentArtifacts_pass_default_config(self):
        success = True
        inputs = {
            "content_version": "1.0.0.0",
            "schema": "2015-01-01",
            "source_workspace": "my-syn-synaps-dev"
        }
        expected = {  
            "$schema": 'http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#',
            "contentVersion": "1.0.0.0",
            "resources": [],
            "parameters":  {      
                "workspaceName": {
                    "type": "string",
                    "metadata": "Workspace name",
                    "defaultValue": "my-syn-synaps-dev"}
            },
            "variables": {
                "workspaceId": "[concat('Microsoft.Synapse/workspaces/', parameters('workspaceName'))]"}
        }
        return success, inputs, expected

    def case_2_DeploymentArtifacts_fail_no_source_workspace(self):
        success = False
        inputs = {
            "content_version":  "1.0.0.0",
            "schema": "2015-01-01",
            "source_workspace": None
        }
        expected = {
            "error": TypeError,
            "message": "source_workspace attribute must be set to an instance of <class 'str'>" 
        }

        return success, inputs, expected

    def case_3_DeploymentArtifacts_fail_no_schema(self):
        success = False
        inputs = {
            "content_version":  "1.0.0.0",
            "schema": None,
            "source_workspace": "test-name"
        }
        expected = {
            "error": TypeError,
            "message": "schema attribute must be set to an instance of <class 'str'>" 
        }

        return success, inputs, expected

    def case_4_DeploymentArtifacts_fail_no_content_version(self):
        success = False
        inputs = {
            "content_version":  None,
            "schema": "2015-01-01",
            "source_workspace": "test-name"
        }
        expected = {
            "error": TypeError,
            "message": "content_version attribute must be set to an instance of <class 'str'>" 
        }

        return success, inputs, expected


class TestCases_DeploymentParameters():

    def case_1_default_config(self):
        inputs =  {
              "content_version": "1.0.0.0",
              "schema": "2015-01-01",
              "source_workspace": "my-syn-synaps-dev"
        }
        expected = {"$schema": 'https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#',"contentVersion": "1.0.0.0","parameters":  {"workspaceName": {"value": "my-syn-synaps-dev"}}}
        return inputs, expected

class TestCases_ParameterConfig():

    def save_config(self, config, directory, file_name):
        """Save test config to file to be used in the test case

        Args:
            config (dict): config object

        Returns:
            str: path to the saved config file
        """
        
        config_path = os.path.join(directory, file_name)
        
        # create tmp directory when not exists
        if not os.path.exists("tmp"):
            os.makedirs("tmp")

        with open(config_path, 'w', encoding="utf-8") as outfile:
            json.dump(config, outfile)

        return config_path

    def case_1_default_config(self):

        # define input config
        # save input config to file
        input_config_path = ""
        # define expected config
        expected = {
            "notebooks": {"properties": {"bigDataPool": {"referenceName": "="}}},
            "sqlscripts": {"properties": {"content": {"currentConnection": {"*": "-"}}}},
            "pipelines": {"properties": {"activities": [{"typeProperties": {"waitTimeInSeconds": "-::int","headers": "=::object"}}]}},
            "integrationRuntimes": {"properties": {"typeProperties": {"*": "="}}},
            "triggers": {"properties": {"typeProperties": {"recurrence": {"*": "=","interval": "=:triggerSuffix:int","frequency": "=:-freq"},"maxConcurrency": "="}}},
            "linkedServices": {"*": {"properties": {"typeProperties": {"*": "="}}},"AzureDataLakeStore": {"properties": {"typeProperties": {"dataLakeStoreUri": "="}}}},
            "datasets": {"properties": {"typeProperties": {"*": "="}}}
            }

        return input_config_path, expected
    
    def case_2_custom_config(self):

        input_config = {
            "Microsoft.Synapse/workspaces/notebooks": {
                    "properties": {}
                },
                "Microsoft.Synapse/workspaces/sqlscripts": {
                "properties": {
                    "content":{
                        "currentConnection":{
                                "*":"="
                            }
                        } 
                    }
                },
                "Microsoft.Synapse/workspaces/pipelines": {
                    "properties": {
                        "activities": [{
                            "typeProperties": {
                            }
                        }],
                    "parameters": {
                        "storage_name": {
                            "type": "=",
                            "defaultValue": "="
                        }
                    }
                    }
                },
                "Microsoft.Synapse/workspaces/integrationRuntimes": {
                    "properties": {
                        "typeProperties": {
                            "*": "="
                        }
                    }
                },
                "Microsoft.Synapse/workspaces/triggers": {
                    "properties": {
                        "typeProperties": {
                            "recurrence": {
                                "*": "=",
                                "interval": "=:triggerSuffix:int",
                                "frequency": "=:-freq"
                            },
                            "maxConcurrency": "="
                        }
                    }
                },
                "Microsoft.Synapse/workspaces/linkedServices": {
                    "*": {
                        "properties": {
                            "typeProperties": {
                                "url": "=",
                                "baseUrl": "=",
                                "functionAppUrl": "="
                            }
                        }
                    },
                    "AzureDataLakeStore": {
                        "properties": {
                            "typeProperties": {
                                "dataLakeStoreUri": "="
                            }
                        }
                    }
                },
                "Microsoft.Synapse/workspaces/datasets": {
                    "properties": {}
                }
            }

        expected = {'notebooks': {'properties': {}}, 'sqlscripts': {'properties': {'content': {'currentConnection': {'*': '='}}}}, 'pipelines': {'properties': {'activities': [{'typeProperties': {}}], 'parameters': {'storage_name': {'type': '=', 'defaultValue': '='}}}}, 'integrationRuntimes': {'properties': {'typeProperties': {'*': '='}}}, 'triggers': {'properties': {'typeProperties': {'recurrence': {'*': '=', 'interval': '=:triggerSuffix:int', 'frequency': '=:-freq'}, 'maxConcurrency': '='}}}, 'linkedServices': {'*': {'properties': {'typeProperties': {'url': '=', 'baseUrl': '=', 'functionAppUrl': '='}}}, 'AzureDataLakeStore': {'properties': {'typeProperties': {'dataLakeStoreUri': '='}}}}, 'datasets': {'properties': {}}}
        inputs = self.save_config(input_config,directory="tmp", file_name="case_2_custom_config.json")
        return inputs, expected