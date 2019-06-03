import re
from src.actions.reduce_dataset import *

utils = Utils()


def test_utils_random_pid():
    generated_pid = utils.random_pid()
    pid_pattern = re.compile('[A-Z]{3,}\\d{3,}')
    assert re.match(pid_pattern, generated_pid)


def test_utils_new_derived_dataset():
    derived_dataset = utils.new_derived_dataset()
    date_pattern = re.compile('\\d{4,}-\\d{2,}-\\d{2,}T\\d{2,}:\\d{2,}:\\d{2,}.\\w{6,}')
    assert 'datasetName' in derived_dataset
    assert re.match(date_pattern, derived_dataset['creationTime'])
