import random
import string
import requests
from requests.exceptions import Timeout


def main(_dict):
    host = _dict['api']['host']
    port = _dict['api']['port']
    login = _dict['login']

    if 'dataset' in _dict:
        dataset_name = _dict['dataset']['datasetName']
        derived_dataset = new_derived_dataset()

        try:
            login_response = requests.post(
                'http://' + host + ':' + port + '/api/v3/Users/Login',
                json=login,
                timeout=(5, 10)
            )
        except Timeout:
            output = "Error: Login request timed out"
            return {"datasetName": dataset_name, "output": output}
        else:
            access_token = login_response.json()['id']
            try:
                response = requests.post(
                    'http://' + host + ':' + port + '/api/v3/DerivedDatasets?access_token=' + access_token,
                    json=derived_dataset,
                    timeout=(5, 10))
            except Timeout:
                output = "Error: The request timed out"
                return {"datasetName": dataset_name, "output": output}
            else:
                output = "Success: New Derived Dataset created."
                return {"datasetName": dataset_name, "derived_dataset": response.json(), "output": output}

    else:
        dataset_name = "Unknown"
        output = "Error: Input did not reach Action 'reduce-test'."
        return {"datasetName": dataset_name, "output": output}


def random_pid(letters=string.ascii_uppercase, digits=string.digits):
    return ''.join(random.choice(letters) for _ in range(3)) + ''.join(random.choice(digits) for _ in range(3))


def new_derived_dataset():
    return {
        "investigator": "string",
        "inputDatasets": [
            "string"
        ],
        "usedSoftware": [
            "string"
        ],
        "jobParameters": {},
        "jobLogData": "string",
        "scientificMetadata": {},
        "pid": random_pid(),
        "owner": "string",
        "ownerEmail": "string",
        "orcidOfOwner": "string",
        "contactEmail": "string",
        "sourceFolder": "string",
        "size": 0,
        "packedSize": 0,
        "creationTime": "2019-05-21T07:08:52.028Z",
        "type": "string",
        "validationStatus": "string",
        "keywords": [
            "string"
        ],
        "description": "string",
        "datasetName": "string",
        "classification": "string",
        "license": "string",
        "version": "string",
        "isPublished": True,
        "ownerGroup": "string",
        "accessGroups": [
            "string"
        ],
        "createdBy": "string",
        "updatedBy": "string",
        "createdAt": "2019-05-21T07:08:52.028Z",
        "updatedAt": "2019-05-21T07:08:52.028Z",
        "datasetlifecycle": {
            "archivable": True,
            "retrievable": True,
            "publishable": True,
            "dateOfDiskPurging": "2019-05-21T07:08:52.028Z",
            "archiveRetentionTime": "2019-05-21T07:08:52.028Z",
            "dateOfPublishing": "2019-05-21T07:08:52.028Z",
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
