from .models import DeploymentArtifacts, DeploymentParameters, ParameterConfig 
import os
from glob import glob
import json
import pprint as pp
import collections

class BuildClient(object):

    def __init__(self, content_version, schema, source_workspace,output_dir, synapse_root):

        self.content_version =  content_version
        self.schema = schema
        self.source_workspace = source_workspace
        self.synapse_root = synapse_root
        self.output_dir=output_dir

        self.DeploymentArtifacts = DeploymentArtifacts(content_version, schema, source_workspace)
        self.DeploymentParameters = DeploymentParameters(content_version, schema, source_workspace)
        self.ParameterConfig = ParameterConfig() #TODO add test with custom config

        # parameter for recursive paramter replacement 
        self.current_artifact_name = ""
        self.current_paramter_name = ""
        self.current_artifact_obj = ""
        self.current_operations = ""
        self.current_levels = ""
        self.current_path = ""
        self.current_artifact_type = ""
        self.current_artifact_type_config = ""

    def find_artifacts(self):
        
        artifact_paths = {}
        synapse_dirs = [x[0] for x in os.walk(self.synapse_root)][1:]
        
        for dir_path in synapse_dirs:
            file_names =  os.listdir(dir_path)
            artifact_paths[dir_path] = [name for name in file_names]

        return artifact_paths

    def load_artifacts_from_file(self, artifact_paths):

        
        artifact_json_objects_dict = {}
        
        # create dict with key of artifact type
        for directory, file_names in artifact_paths.items():
            artfact_type = directory.split("/")[-1] + "s"
            artifact_json_objects_dict[artfact_type] = []

            # for each key (artifact tpye) in dict
            # create a list with all file paths 
            for name in file_names:
                f = open(os.path.join(directory, name))
                artifact_json_object = json.load(f)
                artifact_json_objects_dict[artfact_type].append(artifact_json_object)
        
        return artifact_json_objects_dict

    def flatten(self, d, parent_key='', sep='_'):
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
                items.extend(self.flatten(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.extend(self.flatten(v[0], new_key + "_*", sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _operation_handler(self, key_path, value, operations, artifact_name):
        """
        # TODO: add description
        parms: Is a dictionary with key value pairs where value where extracted 
            from the deployment file. The value should hold the actual value
        """
        #Setting the value of a property as a string indicates that you want to parameterize the property. Use the format <action>:<name>:<stype>.
        #<action> can be one of these characters:
        #    = means keep the current value as the default value for the parameter.
        #    - means don't keep the default value for the parameter.
        #    | is a special case for secrets from Azure Key Vault for connection strings or keys. - not implemented
        # <name> is the name of the parameter. If it's blank, it takes the name of the property. If the value starts with a - character, 
        # the name is shortened. For example, AzureStorage1_properties_typeProperties_connectionString would be shortened to AzureStorage1_connectionString
        # <stype> is the type of parameter. If <stype> is blank, the default type is string. Supported values: string, securestring, int, bool, object,
        #  secureobject and array.
        # read in operations from config file
        action, *other = operations.split(":")
        name = None
        stype = None
        if len(other) == 1:
            name = other[0]
            stype = None
        elif len(other) == 2:
            name = other[0]
            stype = other[1]

        value_dict = {}
        parm_value_dict = {}

        #****** handle actions ******#
        # the actions defines how the parameter values should be handeled
        # A = in the actions means that the current value of a parameter should 
        # be keep as a default values
        if action == "=":
            #if key_path in deployment_file["parameters"].keys():
            #    value_dict["defaultValue"] = deployment_file["parameters"][key_path]["defaultValue"]
            #else:
            value_dict["defaultValue"] = value
            parm_value_dict["value"] = value

        # A - in the actions means that the current value should not be keept
        # no default value is applied
        elif action == "-":
            parm_value_dict["value"] = ""

        #****** handle data types ******#
        # the stype operation parameter defines how data types should be handeled
        # when the parameter is empty the default data type will be a string
        # Supported values: string, securestring, int, bool, object, secureobject and array.
        if stype is None:
            if isinstance(value, str):
                value_dict["type"] = "string"
            elif isinstance(value, dict):
                value_dict["type"] = "object"
            elif isinstance(value, int):
                value_dict["type"] = "int"
        elif stype is not None:
            value_dict["type"] = stype

        #****** handle parameter names ******#
        #If it's blank, it takes the name of the property. 
        # the name defines the name of parameters
        if name == None or name == "":
            key = key_path
        # When the parameters starts with a - the parameter name is shortened. 
        # For example, AzureStorage1_properties_typeProperties_connectionString would be shortened to AzureStorage1_connectionString
        elif name.startswith("-"): 
            key = ''.join([artifact_name, "_", name[1:]])

        elif not name.startswith("-") and name is not None: 
            key_path_without_last = '_'.join(key_path.split("_")[:-1])
            key = ''.join([key_path_without_last, "_", name])
        
        # create dicts that hold all updates of from the operatios
        update_dict_deployment_file = {}
        update_dict_deployment_file[key] = value_dict
        update_dict_parameter_file = {}
        update_dict_parameter_file[key] = parm_value_dict

        return key, update_dict_deployment_file, update_dict_parameter_file


    def _paramter_name_handler(self, levels, first_level):

        if first_level:
            self.current_paramter_name=''.join([self.current_artifact_name, "_", levels[0]])
        else:
            self.current_paramter_name = ''.join([self.current_paramter_name, "_", levels[0]])
        

    def _dependency_find_reference(self, d, _ref_list=[]):
        if isinstance(d,list):
            for i in d:
                _ref_list = self._dependency_find_reference(i, _ref_list)
        elif isinstance(d,dict):
            if "referenceName" in d.keys():
                _ref_list.append(d)
            else:
                for k, v in d.items():
                    _ref_list = self._dependency_find_reference(d[k], _ref_list) 
        return _ref_list

    def _dpendency_handler(self, artifact_obj):

        artifact_obj['dependsOn'] = []
        if "properties" in artifact_obj.keys() and "managedPrivateEndpoints" not in artifact_obj["type"]:
            reference = self._dependency_find_reference(artifact_obj['properties'], _ref_list=[])
        elif "managedPrivateEndpoints" in artifact_obj["type"]:
            network_ref = f"[concat(variables('workspaceId'), '/managedVirtualNetworks/default')]"
            artifact_obj['dependsOn'].append(network_ref)
            
            return artifact_obj
        else:
            return artifact_obj
        if reference is not None:
            for ref in reference:
                if ref["type"] == "IntegrationRuntimeReference":
                    ref_name = ref["referenceName"]
                    integration_runtime_ref = f"[concat(variables('workspaceId'), '/integrationRuntimes/{ref_name}')]"
                    artifact_obj['dependsOn'].append(integration_runtime_ref)
                
                elif ref["type"] == "LinkedServiceReference":
                    ref_name = ref["referenceName"]
                    linked_service_ref = f"[concat(variables('workspaceId'), '/linkedServices/{ref_name}')]"
                    artifact_obj['dependsOn'].append(linked_service_ref)
                
                elif ref["type"] == "PipelineReference":
                    ref_name = ref["referenceName"]
                    pipeline_ref = f"[concat(variables('workspaceId'), '/pipelines/{ref_name}')]"
                    artifact_obj['dependsOn'].append(pipeline_ref)  
                
                elif ref["type"] == "ManagedVirtualNetworkReference":
                    ref_name = ref["referenceName"]
                    network_ref = f"[concat(variables('workspaceId'), '/managedVirtualNetworks/{ref_name}')]"
                    artifact_obj['dependsOn'].append(network_ref)  
                
                elif ref["type"] == "DatasetReference":
                    ref_name = ref["referenceName"]
                    dataset_ref = f"[concat(variables('workspaceId'), '/datasets/{ref_name}')]"
                    artifact_obj['dependsOn'].append(dataset_ref)   
                
                elif ref["type"] == "NotebookReference":
                    if isinstance(ref["referenceName"], dict):
                        pass
                    else:
                        ref_name = ref["referenceName"]
                        dataset_ref = f"[concat(variables('workspaceId'), '/notebooks/{ref_name}')]"
                        artifact_obj['dependsOn'].append(dataset_ref)   
                
                elif ref["type"] == "DataFlowReference":
                    ref_name = ref["referenceName"]
                    dataset_ref = f"[concat(variables('workspaceId'), '/dataflows/{ref_name}')]"
                    artifact_obj['dependsOn'].append(dataset_ref)  
              

        # remove duplicates from dependsOn
        artifact_obj['dependsOn'] = list(dict.fromkeys(artifact_obj['dependsOn']))                   
        return artifact_obj


    def _recursive_replace_values(self, artifact_dict_element, levels):

        # levels is a list of path elements (e.g ["properties", "typeProperties", "recurrence", "*"])
        # for each recursion the first element of the list will be removed (e.g. ["typeProperties", "recurrence", "*"])
        level = levels[0]
        
        # indicator if this is the last level
        # when the last level is reached the operation_handler needs to be applied
        if len(levels) == 1:
            last_level = True
        else:
            last_level = False

        # indicator if this is the first level
        if self.current_paramter_name=="":
            first_level = True
            level_depth = len(levels) 
        else:
            first_level = False
            level_depth = len(levels)

        # indecator if the current level has a wildcard
        # when there is a wildcard in the current level - iterate through all elements
        if level == '*':
            level_has_wildcard = True
        else: 
            level_has_wildcard = False


        # when a * is used in the current level the the underlying paramter replacement config 
        # should be used for all elements below - can be list or dict of keys
        if last_level and level_has_wildcard:
            
            if isinstance(artifact_dict_element, dict):
                start_parameter_name = self.current_paramter_name
                for key in artifact_dict_element.copy().keys():
                    parameter_name = start_parameter_name + "_" + key
                    
                    # TODO: rename function to be more clear
                    if self.ParameterConfig.check_if_path_in_config(parameter_name, self.current_artifact_name, self.current_artifact_type):
                        pass

                    else:
                        # use operations to create paramter name and update dicts
                        new_key, update_dict_deployment_file, update_dict_parameter_file = self._operation_handler(
                            key_path=parameter_name, 
                            value=artifact_dict_element[key], 
                            operations=self.current_operations,
                            artifact_name=self.current_artifact_name)
                        # create parameter and update DeploymentArtifacts and DeploymentParameters
                        artifact_dict_element[key] = f"[parameters('{parameter_name}')]"
                        self.DeploymentArtifacts.dict_update_parameters(update_dict_deployment_file)
                        self.DeploymentParameters.dict_update_parameters(update_dict_parameter_file)

            elif isinstance(artifact_dict_element, list):
                for idx, elm in enumerate(artifact_dict_element):
                    
                    # use operations to create paramter name and update dicts
                    new_key, update_dict_deployment_file, update_dict_parameter_file = self._operation_handler(
                        key_path=self.current_paramter_name, 
                        value=artifact_dict_element[idx], 
                        operations=self.current_operations,
                        artifact_name=self.current_artifact_name)
                    # create parameter and update DeploymentArtifacts and DeploymentParameters
                    artifact_dict_element[idx] = f"[parameters('{self.current_paramter_name}')]"
                    self.DeploymentArtifacts.dict_update_parameters(update_dict_deployment_file)
                    self.DeploymentParameters.dict_update_parameters(update_dict_parameter_file)
        
        if last_level and not level_has_wildcard:
               
            if level in artifact_dict_element.keys():
                    
                self._paramter_name_handler(levels, first_level)


                new_key, update_dict_deployment_file, update_dict_parameter_file = self._operation_handler(
                    key_path=self.current_paramter_name, 
                    value=artifact_dict_element[level], 
                    operations=self.current_operations,
                    artifact_name=self.current_artifact_name)
                
                # check if key value already exists in deployment parameters
                # if isinstance(artifact_dict_element[level], str):
                #     alerady_has_parameter = artifact_dict_element[level].startswith("[parameters('")
                #     if alerady_has_parameter:
                #         existing_parameter_key= artifact_dict_element[level].split("'")[-2]
                #         key_to_overwrite_value = self.DeploymentArtifacts.get_parameter_with_key(existing_parameter_key)

                #         update_dict_deployment_file[new_key] = key_to_overwrite_value
                #         update_dict_parameter_file[new_key] = self.DeploymentParameters.get_parameter_with_key(existing_parameter_key)
                        
                #         self.DeploymentArtifacts.remove_parameter_with_key(existing_parameter_key)
                #         self.DeploymentParameters.remove_parameter_with_key(existing_parameter_key)

                artifact_dict_element[level] = f"[parameters('{new_key}')]"
                self.DeploymentArtifacts.dict_update_parameters(update_dict_deployment_file)
                self.DeploymentParameters.dict_update_parameters(update_dict_parameter_file)
            else:
                pass #TODO: add logging
                
        if not last_level and level_has_wildcard:

            if isinstance(artifact_dict_element, dict):
                for key in artifact_dict_element.keys():
                    levels.insert(0, key)
                    self._paramter_name_handler(levels, first_level)
                    artifact_dict_element[key] = self._recursive_replace_values(artifact_dict_element[key], levels=levels[1:])
                
            elif isinstance(artifact_dict_element, list):
                start_parameter_name = self.current_paramter_name
                for idx, list_element in enumerate(artifact_dict_element):
                    levels = levels[1:]
                    levels.insert(0, str(idx))
                    self._paramter_name_handler(levels, first_level)
                    artifact_dict_element[idx] = self._recursive_replace_values(artifact_dict_element[idx], levels=levels[1:])
                    
                    self.current_paramter_name = start_parameter_name

        if not last_level and not level_has_wildcard:
            if isinstance(artifact_dict_element, dict):
                if level in artifact_dict_element.keys():
                    self._paramter_name_handler(levels, first_level)
                    artifact_dict_element[level] = self._recursive_replace_values(artifact_dict_element[level], levels=levels[1:])
                    
            elif isinstance(artifact_dict_element, list):
                for idx, list_element in enumerate(artifact_dict_element):
                    levels.insert(0, str(idx))
                    self._paramter_name_handler(levels, first_level)
                    artifact_dict_element[idx] = self._recursive_replace_values(artifact_dict_element[idx], levels=levels[1:])
                    
   
        return artifact_dict_element


    def _replacement_handler(self, artifact_objects, replacement_config):
        """Function to start recursive replacement
        """

        for config_type, artifacts in artifact_objects.items():
            for artifact in artifacts:
                self.current_artifact_name = artifact["name"]
                # replace artifact name with a paramters name
                #if not artifact["name"].startswith("[concat(parameters("):
                artifact["name"] = "[concat(parameters('workspaceName'), '/{}')]".format(self.current_artifact_name )
                artifact["type"] = f"Microsoft.Synapse/workspaces/{config_type.lower()}"
                artifact["apiVersion"] = self.schema

                for replace_path, operation in replacement_config.items():
                    self.current_artifact_type = replace_path.split("_")[0].lower()
                    self.current_operations = operation

                    if config_type.lower() == self.current_artifact_type:

                        self.current_paramter_name = ""
                        levels = replace_path.split("_")[1:]

                        #* Special case for linked services - wildcards for linked service types
                        if self.current_artifact_type == "linkedservices":
                                        
                            config_linked_service_type = levels[0]
                            if config_linked_service_type == "*":
                                levels = levels[1:]
                                artifact = self._recursive_replace_values(artifact, levels=levels)
                            elif config_linked_service_type == artifact["properties"]["type"]:
                                artifact= self._recursive_replace_values(artifact, levels=levels)                        
                        #* Normal replacement for other artifact types
                        else:
                            artifact = self._recursive_replace_values(artifact, levels=levels)

                        artifact = self._dpendency_handler(artifact)

                self.DeploymentArtifacts.add_resource(artifact)


    def build(self):
        """Main function to start a build
        """

        # 1. Load all artifacts defined in parameter_definition
        artifact_paths = self.find_artifacts()

        # 2. search in synapse root for all artifact paths
        artifact_json_objects_dict = self.load_artifacts_from_file(artifact_paths)
        
        self.current_artifact_type_config = self.ParameterConfig.get_config()

        # 6. replace values in artifact objects
        self._replacement_handler(artifact_json_objects_dict, self.current_artifact_type_config)

        
        # save artifact_json_objects_dict to json file
        with open(os.path.join(self.output_dir, "test_artifacts.json"), "w",encoding="utf-8") as f:
            json.dump(self.DeploymentArtifacts.to_json(), f, indent=4)
        
        # save artifact_json_objects_dict to json file
        with open(os.path.join(self.output_dir,"test_parameters.json"), "w", encoding="utf-8") as f:
            json.dump(self.DeploymentParameters.to_json(), f, indent=4)

        # TODO: refactoring
        # TODO: add logging
        # TODO: add dependency handler
        # TODO: handle secure string   
        # TODO: add unit tests     
    
        return 

# client = BuildClient(
#     content_version="1.0.0.0", 
#     schema="2015-01-01", 
#     source_workspace="my-syn-synaps-dev",
#     output_folder="")

# client.build()