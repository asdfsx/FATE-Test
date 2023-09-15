# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["fate_test", "fate_test.scripts"]

package_data = {"": ["*"]}

install_requires = [
    "click>=8.0.0",
    "loguru>=0.6.0",
    "pandas>=2.0.3",
    "prettytable>=1.0.0,<2.0.0",
    "ruamel.yaml>=0.16,<0.17.0",
    'colorama>0.4.4',
    'xgboost>=1.7.6',
    "scikit-learn"
]

entry_points = {"console_scripts": ["fate_test = fate_test.scripts.cli:cli"]}

setup_kwargs = {
    "name": "fate-test",
    "version": "2.0.0-beta",
    "description": "test tools for FATE",
    "long_description": 'FATE Test\n=========\n\nA collection of useful tools to running FATE\'s test.\n\n.. image:: images/tutorial.gif\n   :align: center\n   :alt: tutorial\n\nquick start\n-----------\n\n1. (optional) create virtual env\n\n   .. code-block:: bash\n\n      python -m venv venv\n      source venv/bin/activate\n      pip install -U pip\n\n\n2. install fate_test\n\n   .. code-block:: bash\n\n      pip install fate_test\n      fate_test --help\n\n\n3. edit default fate_test_config.yaml\n\n   .. code-block:: bash\n\n      # edit priority config file with system default editor\n      # filling some field according to comments\n      fate_test config edit\n\n4. configure FATE-Pipeline and FATE-Flow Commandline server setting\n\n.. code-block:: bash\n\n      # configure FATE-Pipeline server setting\n      pipeline init --port 9380 --ip 127.0.0.1\n      # configure FATE-Flow Commandline server setting\n      flow init --port 9380 --ip 127.0.0.1\n\n5. run some fate_test suite\n\n   .. code-block:: bash\n\n      fate_test suite -i <path contains *testsuite.json>\n\n\n6. run some fate_test benchmark\n\n   .. code-block:: bash\n\n      fate_test benchmark-quality -i <path contains *benchmark.json>\n\n7. useful logs or exception will be saved to logs dir with namespace shown in last step\n\ndevelop install\n---------------\nIt is more convenient to use the editable mode during development: replace step 2 with flowing steps\n\n.. code-block:: bash\n\n   pip install -e ${FATE}/python/fate_client && pip install -e ${FATE}/python/fate_test\n\n\n\ncommand types\n-------------\n\n- suite: used for running testsuites, collection of FATE jobs\n\n  .. code-block:: bash\n\n     fate_test suite -i <path contains *testsuite.json>\n\n\n- benchmark-quality used for comparing modeling quality between FATE and other machine learning systems\n\n  .. code-block:: bash\n\n      fate_test benchmark-quality -i <path contains *benchmark.json>\n\n\n\nconfiguration by examples\n--------------------------\n\n1. no need ssh tunnel:\n\n   - 9999, service: service_a\n   - 10000, service: service_b\n\n   and both service_a, service_b can be requested directly:\n\n   .. code-block:: yaml\n\n      work_mode: 1 # 0 for standalone, 1 for cluster\n      data_base_dir: <path_to_data>\n      parties:\n        guest: [10000]\n        host: [9999, 10000]\n        arbiter: [9999]\n      services:\n        - flow_services:\n          - {address: service_a, parties: [9999]}\n          - {address: service_b, parties: [10000]}\n\n2. need ssh tunnel:\n\n   - 9999, service: service_a\n   - 10000, service: service_b\n\n   service_a, can be requested directly while service_b don\'t,\n   but you can request service_b in other node, say B:\n\n   .. code-block:: yaml\n\n      work_mode: 0 # 0 for standalone, 1 for cluster\n      data_base_dir: <path_to_data>\n      parties:\n        guest: [10000]\n        host: [9999, 10000]\n        arbiter: [9999]\n      services:\n        - flow_services:\n          - {address: service_a, parties: [9999]}\n        - flow_services:\n          - {address: service_b, parties: [10000]}\n          ssh_tunnel: # optional\n          enable: true\n          ssh_address: <ssh_ip_to_B>:<ssh_port_to_B>\n          ssh_username: <ssh_username_to B>\n          ssh_password: # optional\n          ssh_priv_key: "~/.ssh/id_rsa"\n\n\nTestsuite\n---------\n\nTestsuite is used for running a collection of jobs in sequence. Data used for jobs could be uploaded before jobs are\nsubmitted, and are cleaned when jobs finished. This tool is useful for FATE\'s release test.\n\ncommand options\n~~~~~~~~~~~~~~~\n\n.. code-block:: bash\n\n      fate_test suite --help\n\n1. include:\n\n   .. code-block:: bash\n\n      fate_test suite -i <path1 contains *testsuite.json>\n\n   will run testsuites in *path1*\n\n2. exclude:\n\n   .. code-block:: bash\n\n      fate_test suite -i <path1 contains *testsuite.json> -e <path2 to exclude> -e <path3 to exclude> ...\n\n   will run testsuites in *path1* but not in *path2* and *path3*\n\n3. glob:\n\n   .. code-block:: bash\n\n      fate_test suite -i <path1 contains *testsuite.json> -g "hetero*"\n\n   will run testsuites in sub directory start with *hetero* of *path1*\n\n4. replace:\n\n   .. code-block:: bash\n\n      fate_test suite -i <path1 contains *testsuite.json> -r \'{"maxIter": 5}\'\n\n   will find all key-value pair with key "maxIter" in `data conf` or `conf` or `dsl` and replace the value with 5\n\n\n5. skip-data:\n\n   .. code-block:: bash\n\n       fate_test suite -i <path1 contains *testsuite.json> --skip-data\n\n   will run testsuites in *path1* without uploading data specified in *benchmark.json*.\n\n\n6. yes:\n\n   .. code-block:: bash\n\n      fate_test suite -i <path1 contains *testsuite.json> --yes\n\n   will run testsuites in *path1* directly, skipping double check\n\n7. skip-dsl-jobs:\n\n   .. code-block:: bash\n\n      fate_test suite -i <path1 contains *testsuite.json> --skip-dsl-jobs\n\n   will run testsuites in *path1* but skip all *tasks* in testsuites. It\'s would be useful when only pipeline tasks needed.\n\n8. skip-pipeline-jobs:\n\n   .. code-block:: bash\n\n      fate_test suite -i <path1 contains *testsuite.json> --skip-pipeline-jobs\n\n   will run testsuites in *path1* but skip all *pipeline tasks* in testsuites. It\'s would be useful when only dsl tasks needed.\n\n\nBenchmark Quality\n------------------\n\nBenchmark-quality is used for comparing modeling quality between FATE\nand other machine learning systems. Benchmark produces a metrics comparison\nsummary for each benchmark job group.\n\n.. code-block:: bash\n\n   fate_test benchmark-quality -i examples/benchmark_quality/hetero_linear_regression\n\n.. code-block:: bash\n\n    +-------+--------------------------------------------------------------+\n    |  Data |                             Name                             |\n    +-------+--------------------------------------------------------------+\n    | train | {\'guest\': \'motor_hetero_guest\', \'host\': \'motor_hetero_host\'} |\n    |  test | {\'guest\': \'motor_hetero_guest\', \'host\': \'motor_hetero_host\'} |\n    +-------+--------------------------------------------------------------+\n    +------------------------------------+--------------------+--------------------+-------------------------+---------------------+\n    |             Model Name             | explained_variance |      r2_score      | root_mean_squared_error |  mean_squared_error |\n    +------------------------------------+--------------------+--------------------+-------------------------+---------------------+\n    | local-linear_regression-regression | 0.9035168452250094 | 0.9035070863155368 |   0.31340413289880553   | 0.09822215051805216 |\n    | FATE-linear_regression-regression  | 0.903146386539082  | 0.9031411831961411 |    0.3139977881119483   | 0.09859461093919596 |\n    +------------------------------------+--------------------+--------------------+-------------------------+---------------------+\n    +-------------------------+-----------+\n    |          Metric         | All Match |\n    +-------------------------+-----------+\n    |    explained_variance   |    True   |\n    |         r2_score        |    True   |\n    | root_mean_squared_error |    True   |\n    |    mean_squared_error   |    True   |\n    +-------------------------+-----------+\n\ncommand options\n~~~~~~~~~~~~~~~\n\nuse the following command to show help message\n\n.. code-block:: bash\n\n      fate_test benchmark-quality --help\n\n1. include:\n\n   .. code-block:: bash\n\n      fate_test benchmark-quality -i <path1 contains *benchmark.json>\n\n   will run benchmark testsuites in *path1*\n\n2. exclude:\n\n   .. code-block:: bash\n\n      fate_test benchmark-quality -i <path1 contains *benchmark.json> -e <path2 to exclude> -e <path3 to exclude> ...\n\n   will run benchmark testsuites in *path1* but not in *path2* and *path3*\n\n3. glob:\n\n   .. code-block:: bash\n\n      fate_test benchmark-quality -i <path1 contains *benchmark.json> -g "hetero*"\n\n   will run benchmark testsuites in sub directory start with *hetero* of *path1*\n\n4. tol:\n\n   .. code-block:: bash\n\n      fate_test benchmark-quality -i <path1 contains *benchmark.json> -t 1e-3\n\n   will run benchmark testsuites in *path1* with absolute tolerance of difference between metrics set to 0.001.\n   If absolute difference between metrics is smaller than *tol*, then metrics are considered\n   almost equal. Check benchmark testsuite `writing guide <#benchmark-testsuite>`_ on setting alternative tolerance.\n\n5. skip-data:\n\n   .. code-block:: bash\n\n       fate_test benchmark-quality -i <path1 contains *benchmark.json> --skip-data\n\n   will run benchmark testsuites in *path1* without uploading data specified in *benchmark.json*.\n\n\n6. yes:\n\n   .. code-block:: bash\n\n      fate_test benchmark-quality -i <path1 contains *benchmark.json> --yes\n\n   will run benchmark testsuites in *path1* directly, skipping double check\n\n\nbenchmark testsuite\n~~~~~~~~~~~~~~~~~~~\n\nConfiguration of jobs should be specified in a benchmark testsuite whose file name ends\nwith "\\*benchmark.json". For benchmark testsuite example,\nplease refer `here <../../examples/benchmark_quality>`_.\n\nA benchmark testsuite includes the following elements:\n\n- data: list of local data to be uploaded before running FATE jobs\n\n  - file: path to original data file to be uploaded, should be relative to testsuite or FATE installation path\n  - head: whether file includes header\n  - partition: number of partition for data storage\n  - table_name: table name in storage\n  - namespace: table namespace in storage\n  - role: which role to upload the data, as specified in fate_test.config;\n    naming format is: "{role_type}_{role_index}", index starts at 0\n\n  .. code-block:: json\n\n        "data": [\n            {\n                "file": "examples/data/motor_hetero_host.csv",\n                "head": 1,\n                "partition": 8,\n                "table_name": "motor_hetero_host",\n                "namespace": "experiment",\n                "role": "host_0"\n            }\n        ]\n\n- job group: each group includes arbitrary number of jobs with paths to corresponding script and configuration\n\n  - job: name of job to be run, must be unique within each group list\n\n    - script: path to `testing script <#testing-script>`_, should be relative to testsuite\n    - conf: path to job configuration file for script, should be relative to testsuite\n\n    .. code-block:: json\n\n       "local": {\n            "script": "./local-linr.py",\n            "conf": "./linr_config.yaml"\n       }\n\n  - compare_setting: additional setting for quality metrics comparison, currently only takes ``relative_tol``\n\n    If metrics *a* and *b* satisfy *abs(a-b) <= max(relative_tol \\* max(abs(a), abs(b)), absolute_tol)*\n    (from `math module <https://docs.python.org/3/library/math.html#math.isclose>`_),\n    they are considered almost equal. In the below example, metrics from "local" and "FATE" jobs are\n    considered almost equal if their relative difference is smaller than\n    *0.05 \\* max(abs(local_metric), abs(pipeline_metric)*.\n\n  .. code-block:: json\n\n     "linear_regression-regression": {\n         "local": {\n             "script": "./local-linr.py",\n             "conf": "./linr_config.yaml"\n         },\n         "FATE": {\n             "script": "./fate-linr.py",\n             "conf": "./linr_config.yaml"\n         },\n         "compare_setting": {\n             "relative_tol": 0.01\n         }\n     }\n\n\ntesting script\n~~~~~~~~~~~~~~\n\nAll job scripts need to have ``Main`` function as an entry point for executing jobs; scripts should\nreturn two dictionaries: first with data information key-value pairs: {data_type}: {data_name_dictionary};\nthe second contains {metric_name}: {metric_value} key-value pairs for metric comparison.\n\nBy default, the final data summary shows the output from the job named "FATE"; if no such job exists,\ndata information returned by the first job is shown. For clear presentation, we suggest that user follow\nthis general `guideline <../../examples/data/README.md#data-set-naming-rule>`_ for data set naming. In the case of multi-host\ntask, consider numbering host as such:\n\n::\n\n    {\'guest\': \'default_credit_homo_guest\',\n     \'host_1\': \'default_credit_homo_host_1\',\n     \'host_2\': \'default_credit_homo_host_2\'}\n\nReturned quality metrics of the same key are to be compared.\nNote that only **real-value** metrics can be compared.\n\n- FATE script: ``Main`` always has three inputs:\n\n  - config: job configuration, `JobConfig <../fate_client/pipeline/utils/tools.py#L64>`_ object loaded from "fate_test_config.yaml"\n  - param: job parameter setting, dictionary loaded from "conf" file specified in benchmark testsuite\n  - namespace: namespace suffix, user-given *namespace* or generated timestamp string when using *namespace-mangling*\n\n- non-FATE script: ``Main`` always has one input:\n\n  - param: job parameter setting, dictionary loaded from "conf" file specified in benchmark testsuite\n\n\ndata\n----\n\n`Data` sub-command is used for upload or delete dataset in suite\'s.\n\ncommand options\n~~~~~~~~~~~~~~~\n\n.. code-block:: bash\n\n      fate_test data --help\n\n1. include:\n\n   .. code-block:: bash\n\n      fate_test data [upload|delete] -i <path1 contains *testsuite.json>\n\n   will upload/delete dataset in testsuites in *path1*\n\n2. exclude:\n\n   .. code-block:: bash\n\n      fate_test data [upload|delete] -i <path1 contains *testsuite.json> -e <path2 to exclude> -e <path3 to exclude> ...\n\n   will upload/delete dataset in testsuites in *path1* but not in *path2* and *path3*\n\n3. glob:\n\n   .. code-block:: bash\n\n      fate_test data [upload|delete] -i <path1 contains *testsuite.json> -g "hetero*"\n\n   will upload/delete dataset in testsuites in sub directory start with *hetero* of *path1*\n\n\nfull command options\n---------------------\n\n.. click:: fate_test.scripts.cli:cli\n  :prog: fate_test\n  :show-nested:\n',
    "author": "FederatedAI",
    "author_email": "contact@FedAI.org",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://fate.fedai.org/",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.8",
}

setup(**setup_kwargs)
