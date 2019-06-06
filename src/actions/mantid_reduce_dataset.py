from __future__ import (absolute_import, division, print_function)
import datetime
import random
import string
import subprocess
import requests
from requests.exceptions import Timeout
from mantid.simpleapi import *
from ISISCommandInterface import *


def main(input_data):
    catamel = Catamel(input_data)
    sans2d = SANS2DLimitEventsTime(input_data)
    utils = Utils()

    if 'datasetPid' in input_data:
        dataset_pid = input_data['datasetPid']
    elif 'messages' in input_data and 'datasetPid' in input_data['messages'][0]['value']:
        dataset_pid = input_data['messages'][0]['value']['datasetPid']
    else:
        message = "Error: Input did not reach Action 'mantid-reduce-dataset'."
        return {"inputDataset": input_data, "derivedDataset": "N/A", "message": message}

    access_token = catamel.login()

    if len(access_token) == 64:
        input_dataset = catamel.fetch_dataset_from_pid(access_token, dataset_pid)
        reduce_data = sans2d.run()
        derived_dataset = utils.new_derived_dataset(input_dataset, reduce_data)
        post_response = catamel.post_derived_dataset(access_token, derived_dataset)
        message = "Success: Dataset reduction complete."
        return {"inputDataset": dataset_pid, "derivedDataset": post_response, "message": message}
    else:
        return {"inputDataset": dataset_pid, "derivedDataset": "N/A", "message": access_token}


class SANS2DLimitEventsTime(object):

    def __init__(self, input_data):
        self.input_data = input_data

    def run(self):
        SANS2D()
        MaskFile('/data/MaskSANS2DReductionGUI_LimitEventsTime.txt')
        AssignSample('/data/SANS2D00022048.nxs')
        return WavRangeReduction()


class Catamel:

    def __init__(self, input_data):
        self.host = input_data['api']['host']
        self.port = input_data['api']['port']
        self.login_details = input_data['login']

    def login(self):
        try:
            login_response = requests.post(
                'http://' + self.host + ':' + self.port + '/api/v3/Users/Login',
                json=self.login_details,
                timeout=(5, 10)
            )
        except Timeout:
            return "Error: Login request timed out."
        else:
            return login_response.json()['id']

    def post_derived_dataset(self, access_token, derived_dataset):
        try:
            post_response = requests.post(
                'http://' + self.host + ':' + self.port + '/api/v3/DerivedDatasets?access_token=' + access_token,
                json=derived_dataset,
                timeout=(5, 10)
            )
        except Timeout:
            return "Error: Post request timed out."
        else:
            return post_response.json()

    def fetch_dataset_from_pid(self, access_token, dataset_pid):
        formatted_pid = dataset_pid.replace("/", "%2F")
        try:
            fetch_response = requests.get(
                'http://' + self.host + ':' + self.port + '/api/v3/Datasets/' + formatted_pid + '?access_token=' + access_token,
                timeout=(5, 10)
            )
        except Timeout:
            return "Error: Get request timed out."
        else:
            return fetch_response.json()


class Utils:

    def random_string(self, characters=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(characters) for _ in range(6))

    def new_derived_dataset(self, input_dataset, reduce_data):
        timestamp = datetime.datetime.now().isoformat()

        return {
            "investigator": input_dataset['owner'],
            "inputDatasets": [
                input_dataset['pid']
            ],
            "usedSoftware": [
                "mantidpython " + subprocess.check_output(["mantidpython", "--version"]).rstrip()
            ],
            "jobParameters": {},
            "jobLogData": reduce_data,
            "scientificMetadata": {},
            "owner": input_dataset['owner'],
            "ownerEmail": input_dataset['ownerEmail'],
            "orcidOfOwner": input_dataset['orcidOfOwner'],
            "contactEmail": input_dataset['contactEmail'],
            "sourceFolder": "string",
            "size": 0,
            "packedSize": 0,
            "creationTime": timestamp,
            "type": "string",
            "validationStatus": "string",
            "keywords": [
                "string"
            ],
            "description": "Reduction of " + input_dataset['datasetName'],
            "datasetName": "Reduction no. " + self.random_string(),
            "classification": "string",
            "license": input_dataset['license'],
            "version": "string",
            "isPublished": True,
            "ownerGroup": "string",
            "accessGroups": [
                "string"
            ],
            "createdBy": "string",
            "updatedBy": "string",
            "createdAt": timestamp,
            "updatedAt": timestamp,
            "datasetlifecycle": {
                "archivable": False,
                "retrievable": True,
                "publishable": True,
                "dateOfDiskPurging": timestamp,
                "archiveRetentionTime": timestamp,
                "dateOfPublishing": timestamp,
                "isOnCentralDisk": True,
                "archiveStatusMessage": "string",
                "retrieveStatusMessage": "string",
                "archiveReturnMessage": {},
                "retrieveReturnMessage": {},
                "exportedTo": "string",
                "retrieveIntegrityCheck": True
            },
            "history": [
                {
                    "id": "string"
                }
            ]
        }
