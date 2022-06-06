# Models

> Auto-generated documentation for [synapse_build.models](../../../synapse_build/models.py) module.

- [Src](../README.md#src-index) / [Modules](../MODULES.md#src-modules) / [Synapse Build](index.md#synapse-build) / Models
    - [DeploymentArtifacts](#deploymentartifacts)
        - [DeploymentArtifacts().add_parameters](#deploymentartifactsadd_parameters)
        - [DeploymentArtifacts().add_resource](#deploymentartifactsadd_resource)
        - [DeploymentArtifacts().add_variables](#deploymentartifactsadd_variables)
        - [DeploymentArtifacts().dict_update_parameters](#deploymentartifactsdict_update_parameters)
        - [DeploymentArtifacts().get_parameter_with_key](#deploymentartifactsget_parameter_with_key)
        - [DeploymentArtifacts().parm_validation](#deploymentartifactsparm_validation)
        - [DeploymentArtifacts().remove_parameter_with_key](#deploymentartifactsremove_parameter_with_key)
        - [DeploymentArtifacts().to_json](#deploymentartifactsto_json)
    - [DeploymentParameters](#deploymentparameters)
        - [DeploymentParameters().add_parameters](#deploymentparametersadd_parameters)
        - [DeploymentParameters().dict_update_parameters](#deploymentparametersdict_update_parameters)
        - [DeploymentParameters().get_parameter_with_key](#deploymentparametersget_parameter_with_key)
        - [DeploymentParameters().remove_parameter_with_key](#deploymentparametersremove_parameter_with_key)
        - [DeploymentParameters().to_json](#deploymentparametersto_json)
    - [ParameterConfig](#parameterconfig)
        - [ParameterConfig().check_if_path_in_config](#parameterconfigcheck_if_path_in_config)
        - [ParameterConfig().get_config](#parameterconfigget_config)
        - [ParameterConfig().load_config](#parameterconfigload_config)
        - [ParameterConfig().to_json](#parameterconfigto_json)

## DeploymentArtifacts

[[find in source code]](../../../synapse_build/models.py#L6)

```python
class DeploymentArtifacts(object):
    def __init__(content_version: str, schema: str, source_workspace: str):
```

Class to represent deployment file for synapse workspace artifacts.
Resources and parameters can be added to this class. When all artifacts
are collected the DeploymentArtifacts config can be returned as a json
object to use it for a synapse workspace deployment.

### DeploymentArtifacts().add_parameters

[[find in source code]](../../../synapse_build/models.py#L66)

```python
def add_parameters(parameter_name, value):
```

Add a paramter to the DeploymentArtifacts

#### Arguments

- `parameter_name` *str* - The name of the paramters
value (dict or list or str): The default value for this paramters

### DeploymentArtifacts().add_resource

[[find in source code]](../../../synapse_build/models.py#L43)

```python
def add_resource(resource):
```

Add a new synapse artifact resource to the DeploymentArtifacts

#### Arguments

resource (dict or list): _description_

### DeploymentArtifacts().add_variables

[[find in source code]](../../../synapse_build/models.py#L80)

```python
def add_variables(variables):
```

### DeploymentArtifacts().dict_update_parameters

[[find in source code]](../../../synapse_build/models.py#L77)

```python
def dict_update_parameters(update_dict):
```

### DeploymentArtifacts().get_parameter_with_key

[[find in source code]](../../../synapse_build/models.py#L51)

```python
def get_parameter_with_key(key):
```

### DeploymentArtifacts().parm_validation

[[find in source code]](../../../synapse_build/models.py#L38)

```python
def parm_validation(value, type_, name):
```

### DeploymentArtifacts().remove_parameter_with_key

[[find in source code]](../../../synapse_build/models.py#L56)

```python
def remove_parameter_with_key(key):
```

Remove a parameter from the DeploymentArtifacts

#### Arguments

- `key` *string* - parameter key that should be removed

### DeploymentArtifacts().to_json

[[find in source code]](../../../synapse_build/models.py#L83)

```python
def to_json():
```

## DeploymentParameters

[[find in source code]](../../../synapse_build/models.py#L93)

```python
class DeploymentParameters(object):
    def __init__(content_version, schema, source_workspace):
```

### DeploymentParameters().add_parameters

[[find in source code]](../../../synapse_build/models.py#L101)

```python
def add_parameters(parameter_name, value):
```

### DeploymentParameters().dict_update_parameters

[[find in source code]](../../../synapse_build/models.py#L113)

```python
def dict_update_parameters(update_dict):
```

### DeploymentParameters().get_parameter_with_key

[[find in source code]](../../../synapse_build/models.py#L105)

```python
def get_parameter_with_key(key):
```

### DeploymentParameters().remove_parameter_with_key

[[find in source code]](../../../synapse_build/models.py#L109)

```python
def remove_parameter_with_key(key):
```

### DeploymentParameters().to_json

[[find in source code]](../../../synapse_build/models.py#L116)

```python
def to_json():
```

## ParameterConfig

[[find in source code]](../../../synapse_build/models.py#L124)

```python
class ParameterConfig(object):
    def __init__(config_path=''):
```

### ParameterConfig().check_if_path_in_config

[[find in source code]](../../../synapse_build/models.py#L207)

```python
def check_if_path_in_config(parameter_path, artifact_name, artifact_type):
```

### ParameterConfig().get_config

[[find in source code]](../../../synapse_build/models.py#L177)

```python
def get_config():
```

### ParameterConfig().load_config

[[find in source code]](../../../synapse_build/models.py#L138)

```python
def load_config():
```

Load parameter replacement config from files.
When no config file was found the default parameter
config is used

#### Returns

- `dict` - replacement config

### ParameterConfig().to_json

[[find in source code]](../../../synapse_build/models.py#L174)

```python
def to_json():
```
