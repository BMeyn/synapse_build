from distutils.log import error
from logging import warning
import os
import json
from this import d


class TestCases_BuildClient():


    def helper_func_load_expected_test_data(self, excepted_dir):
        """
        Load expected test data from fixtures directory
        """
        # load expected config file from fixtures
        try:
            with open(os.path.join(excepted_dir, "artifacts.json"), 'r', encoding="utf-8") as f:
                artifacts_json = json.load(f)
        except FileNotFoundError as error_msg:
            raise FileNotFoundError from error_msg

        try:
            with open(os.path.join(excepted_dir, "parameters.json"), 'r', encoding="utf-8") as f:
                parameters_json = json.load(f)
        except FileNotFoundError as error_msg:
            raise FileNotFoundError from error_msg

        return artifacts_json, parameters_json

    def helper_func_clean_tmp_output_dir(self, test_case):
        """
        Setup a temporary output directory
        """
        output_dir=f"tmp/{self.__class__.__name__}/{test_case}"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            # delete files in output_dir
            for f in os.listdir(output_dir):
                os.remove(os.path.join(output_dir, f))
        return output_dir

    def helper_func_create_inputs_dict(self, output_dir, synapse_root, source_workspace="my-syn-synaps-dev", schema="2015-01-01", content_version="1.0.0.0"):
        return {
            "content_version": content_version,
            "schema": schema,
            "source_workspace": source_workspace,
            "output_dir": output_dir,
            "synapse_root": synapse_root
            }

    def helper_func_create_outputs_dict(self, artifacts_json, parameters_json):
        return {
                "artifacts": artifacts_json,
                "parameters": parameters_json
                }
    def helper_func_setup_test_dirs(self, test_data_root, relative_synapse_root, relative_excepted_dir):

        synapse_root=os.path.join(test_data_root, relative_synapse_root)
        excepted_dir=os.path.join(test_data_root, relative_excepted_dir)

        if not os.path.exists(test_data_root):
            os.makedirs(test_data_root)
        if not os.path.exists(synapse_root):
            os.makedirs(synapse_root)
        if not os.path.exists(excepted_dir):
            os.makedirs(excepted_dir)
        
        return synapse_root, excepted_dir

    def helper_func_setup_test_case(self, test_case):
        """
        Setup a temporary output directory
        """

        # test_data_dir = f"test/synapse_build/test_data/test_build_client/{test_case}/"
        # excepted_dir = os.path.join(test_data_dir, "expected")
        # synapse_root = os.path.join(test_data_dir, "inputs/synapse")

        # initialize test case folders
        synapse_root, excepted_dir = self.helper_func_setup_test_dirs(
            test_data_root=f"test/synapse_build/test_data/test_build_client/{test_case}/", 
            relative_synapse_root="inputs/synapse", 
            relative_excepted_dir="expected")

        # setup or clean output_dir
        output_dir = self.helper_func_clean_tmp_output_dir(test_case)

        # load expected config file from fixtures
        artifacts_json, parameters_json = self.helper_func_load_expected_test_data(excepted_dir)

        # create input and output dictionaries
        success = True
        inputs = self.helper_func_create_inputs_dict(output_dir, synapse_root)
        expected = self.helper_func_create_outputs_dict(artifacts_json, parameters_json)

        return success, inputs, expected

    def case_01_BuildClient_default_config_single_pipeline(self,test_case="case1-simple-pipeline"):
        """
        Test case 1:
        - build a single pipeline
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_02_BuildClient_default_config_multiple_pipelines(self,test_case="case2-multiple-pipelines"):
        """
        Test case 2:
        - build multiple pipelines
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    
    def case_03_BuildClient_default_config_simple_linked_service(self,test_case="case3-simple-linked-service"):
        """
        Test case 3:
        - build simple linked service
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_04_BuildClient_default_config_multiple_linked_service(self,test_case="case4-multiple-linked-service"):
        """
        Test case 4:
        - build multiple simple linked service
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_05_BuildClient_default_config_special_type_linked_service(self,test_case="case5-special-type-linked-service"):
        """
        Test case 5:
        - build special type linked service
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_06_BuildClient_default_config_simple_notebook(self,test_case="case6-simple-notebook"):
        """
        Test case 6:
        - build simple notebook
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_07_BuildClient_default_config_multiple_notebooks(self,test_case="case7-multiple-notebooks"):
        """
        Test case 7:
        - build multiple notebooks
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_08_BuildClient_default_config_simple_dataset(self,test_case="case8-simple-dataset"):
        """
        Test case 8:
        - build simple dataset
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_09_BuildClient_default_config_multiple_datasets(self,test_case="case9-multiple-datasets"):
        """
        Test case 9:
        - build multiple datasets
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_10_BuildClient_default_config_simple_integration_runtime(self,test_case="case10-simple_integration_runtime"):
        """
        Test case 10:
        - build simple integration runtime
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_11_BuildClient_default_config_simple_trigger(self,test_case="case11-simple-trigger"):
        """
        Test case 11:
        - build simple trigger
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    def case_12_BuildClient_default_config_multiple_simple_trigger(self,test_case="case12-multiple-trigger"):
        """
        Test case 11:
        - build multiple simple trigger
        """
        return self.helper_func_setup_test_case(test_case=test_case)

    # todo: add test cases for triggers
    # todo: add test case with multiple artifacts
    # todo: add test cases for different replacement configs
