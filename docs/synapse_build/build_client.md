# BuildClient

> Auto-generated documentation for [synapse_build.build_client](../../../synapse_build/build_client.py) module.

- [Src](../README.md#src-index) / [Modules](../MODULES.md#src-modules) / [Synapse Build](index.md#synapse-build) / BuildClient
    - [BuildClient](#buildclient)
        - [BuildClient().build](#buildclientbuild)
        - [BuildClient().find_artifacts](#buildclientfind_artifacts)
        - [BuildClient().flatten](#buildclientflatten)
        - [BuildClient().load_artifacts_from_file](#buildclientload_artifacts_from_file)

## BuildClient

[[find in source code]](../../../synapse_build/build_client.py#L8)

```python
class BuildClient(object):
    def __init__(
        content_version,
        schema,
        source_workspace,
        output_dir,
        synapse_root,
    ):
```

### BuildClient().build

[[find in source code]](../../../synapse_build/build_client.py#L418)

```python
def build():
```

Main function to start a build

### BuildClient().find_artifacts

[[find in source code]](../../../synapse_build/build_client.py#L32)

```python
def find_artifacts():
```

### BuildClient().flatten

[[find in source code]](../../../synapse_build/build_client.py#L62)

```python
def flatten(d, parent_key='', sep='_'):
```

flatten a neasted dictionary with a key path to each value.
example:
    input:
    sample_dict = {'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y' : 10}}, 'd': [1, 2, 3]}

result:
    {'a': 1, 'c_a': 2, 'c_b_x': 5, 'd': [1, 2, 3], 'c_b_y': 10}

### BuildClient().load_artifacts_from_file

[[find in source code]](../../../synapse_build/build_client.py#L43)

```python
def load_artifacts_from_file(artifact_paths):
```
