import os
import json
import jsonschema
import collections

class DeploymentArtifacts(object):
    """Class to represent deployment file for synapse workspace artifacts.
       Resources and parameters can be added to this class. When all artifacts
       are collected the DeploymentArtifacts config can be returned as a json
       object to use it for a synapse workspace deployment.

    """
    def __init__(self, content_version: str, schema: str, source_workspace: str):
        """Initialize the DeploymentArtifacts class

        Args:
            content_version (str): _description_
            schema (str): _description_
            source_workspace (str): _description_
        """
        self.content_version = self.parm_validation(value=content_version, type_=str, name="content_version")
        self.schema = self.parm_validation(value=schema, type_=str, name="schema")
        self.source_workspace =self.parm_validation(value=source_workspace, type_=str, name="source_workspace")

        self.schema_url = f"http://schema.management.azure.com/schemas/{self.schema}/deploymentTemplate.json#"
        self.resources = []
        self.parameters = {
            "workspaceName": {
                "type": "string",
                "metadata": "Workspace name",
                "defaultValue": self.source_workspace
            }
        }
        self.variables = {
            "workspaceId": "[concat('Microsoft.Synapse/workspaces/', parameters('workspaceName'))]"
        }

    def parm_validation(self, value, type_, name):
        if not isinstance(value, type_):
            raise TypeError(f"{name} attribute must be set to an instance of {type_}")
        return value

    def add_resource(self, resource):
        """Add a new synapse artifact resource to the DeploymentArtifacts

        Args:
            resource (dict or list): _description_
        """
        self.resources.append(resource)

    def get_parameter_with_key(self, key):
        for parameter_key, value in self.parameters.items():
            if parameter_key == key:
                return value

    def remove_parameter_with_key(self, key):
        """Remove a parameter from the DeploymentArtifacts

        Args:
            key (string): parameter key that should be removed
        """
        for parameter_key, value in self.parameters.copy().items():
            if parameter_key == key:
                del self.parameters[parameter_key]

    def add_parameters(self, parameter_name, value):
        """Add a paramter to the DeploymentArtifacts

        Args:
            parameter_name (str): The name of the paramters
            value (dict or list or str): The default value for this paramters
        """
        self.parameters.update({
            parameter_name: value
        })

    def dict_update_parameters(self, update_dict):
        self.parameters.update(update_dict)
    
    def add_variables(self, variables):
        self.variables.update(variables)

    def to_json(self):
        return {
            "$schema": self.schema_url,
            "contentVersion": self.content_version,
            "resources": self.resources,
            "parameters": self.parameters,
            "variables": self.variables
        }


class DeploymentParameters(object):
    def __init__(self, content_version, schema, source_workspace):
        self.content_version = content_version
        self.schema = f"https://schema.management.azure.com/schemas/{schema}/deploymentParameters.json#"
        self.parameters = {
            "workspaceName": {"value": source_workspace}
        }

    def add_parameters(self, parameter_name, value):
        self.parameters.update({
            parameter_name: value
        })
    def get_parameter_with_key(self, key):
        for parameter_key, value in self.parameters.items():
            if parameter_key == key:
                return value
    def remove_parameter_with_key(self, key):
        for parameter_key, value in self.parameters.copy().items():
            if parameter_key == key:
                del self.parameters[parameter_key]
    def dict_update_parameters(self, update_dict):
        self.parameters.update(update_dict)

    def to_json(self):
        return {
            "$schema": self.schema,
            "contentVersion": self.content_version,
            "parameters": self.parameters
        }


class ParameterConfig(object):
    def __init__(self, config_path=""): #synapse/template-parameters-definition.json
        self.config_path = config_path
        self.default_config = {
            "Microsoft.Synapse/workspaces/notebooks": {"properties": {"bigDataPool": {"referenceName": "="}}},
            "Microsoft.Synapse/workspaces/sqlscripts": {"properties": {"content": {"currentConnection": {"*": "-"}}}},
            "Microsoft.Synapse/workspaces/pipelines": {"properties": {"activities": [{"typeProperties": {"waitTimeInSeconds": "-::int","headers": "=::object"}}]}},
            "Microsoft.Synapse/workspaces/integrationRuntimes": {"properties": {"typeProperties": {"*": "="}}},
            "Microsoft.Synapse/workspaces/triggers": {"properties": {"typeProperties": {"recurrence": {"*": "=","interval": "=:triggerSuffix:int","frequency": "=:-freq"},"maxConcurrency": "="}}},
            "Microsoft.Synapse/workspaces/linkedServices": {"*": {"properties": {"typeProperties": {"*": "="}}},"AzureDataLakeStore": {"properties": {"typeProperties": {"dataLakeStoreUri": "="}}}},
            "Microsoft.Synapse/workspaces/datasets": {"properties": {"typeProperties": {"*": "="}}}
            }
        self.config = self.load_config()

    def load_config(self):  
        """Load parameter replacement config from files.
           When no config file was found the default parameter
           config is used

        Returns:
            dict: replacement config
        """

        try:
            # load config from json file at config path
            with open(self.config_path, 'r', encoding="utf-8") as f:
                config = json.load(f)
            
            # update the default config with the loaded config
            self.default_config.update(config)
            config = self.default_config

            for key, val in config.copy().items():
                artifact_type = key.split("/")[-1]
                config[artifact_type] = val
                del config[key]
            return config

        except IOError: 
            # when no config file could be found the default
            # config will be used
            config = self.default_config

            for key, val in config.copy().items():
                artifact_type = key.split("/")[-1]
                config[artifact_type] = val
                del config[key]

            return config

    def to_json(self):
        return self.config

    def get_config(self):
        # 3. Get paramter config
        parameter_config  = self.to_json()

        # 5. flatten parameter config
        flatten_config = self._flatten(parameter_config)
        return flatten_config

    def _flatten(self, d, parent_key='', sep='_'):
        '''
        flatten a neasted dictionary with a key path to each value.
        example:
            input:
            sample_dict = {'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y' : 10}}, 'd': [1, 2, 3]}

            result:
                {'a': 1, 'c_a': 2, 'c_b_x': 5, 'd': [1, 2, 3], 'c_b_y': 10}
        '''

        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.abc.MutableMapping):
                items.extend(self._flatten(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.extend(self._flatten(v[0], new_key + "_*", sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def check_if_path_in_config(self, parameter_path, artifact_name, artifact_type):
        config = self.get_config()
        config = {k: v for k, v in config.items() if k.startswith(artifact_type)}

        parameter_path = parameter_path.replace(artifact_name, artifact_type)
        if parameter_path in config.keys():
            return True
        else:
            return False
        # for key, value in config.items():

        #     compare_path = key.split("_")[0] + parameter_path
        #     # remove substring in parameter path
        #     if key == compare_path:
        #         return True
        #     else:
        #         pass