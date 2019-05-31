import datetime
import random
import string
import requests
from requests.exceptions import Timeout


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


class Utils:

    def random_pid(self, letters=string.ascii_uppercase, digits=string.digits):
        return ''.join(random.choice(letters) for _ in range(3)) + ''.join(random.choice(digits) for _ in range(3))

    def new_derived_dataset(self):
        timestamp = datetime.datetime.now().isoformat()

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
            "pid": self.random_pid(),
            "owner": "string",
            "ownerEmail": "string",
            "orcidOfOwner": "string",
            "contactEmail": "string",
            "sourceFolder": "string",
            "size": 0,
            "packedSize": 0,
            "creationTime": timestamp,
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
            "createdAt": timestamp,
            "updatedAt": timestamp,
            "datasetlifecycle": {
                "archivable": True,
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


def main(input_data):
    if 'dataset' in input_data:
        catamel = Catamel(input_data)
        utils = Utils()

        dataset_name = input_data['dataset']['datasetName']
        access_token = catamel.login()

        if len(access_token) == 64:
            derived_dataset = utils.new_derived_dataset()
            post_response = catamel.post_derived_dataset(access_token, derived_dataset)
            message = "Success: Dataset reduction complete."
            return {"datasetName": dataset_name, "derivedDataset": post_response, "message": message}
        else:
            return {"datasetName": dataset_name, "message": access_token}

    else:
        dataset_name = "Unknown"
        message = "Error: Input did not reach Action 'reduce-test'."
        return {"datasetName": dataset_name, "message": message}
