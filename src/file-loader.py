"""
A utility module that loads files and returns their contents. 
Files that are sourced and read can be in a variety of formats, including xlsx, csv, tsv, and json.
This module supports sourcing files from various locations, including local files, S3 Buckets, and URLs.
The module has a main class called FileLoader that, when initialized, accepts parameters that specify the file location and format.
Lastly, the module supports loading a single file, or multiple files in a specified location at once.
Returned content is in the form of a python dictionary, list, or string, depending on the file format.
The module does not use pandas, and is intended to be a lightweight alternative to pandas for reading files.
The module also accepts a logger object to log messages and errors.
"""

from typing import Any, Dict, Optional
import os
import json
import csv
import logging
import requests
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError

from mypy_boto3_s3.client import S3Client

from src.literals import FileLoaderFormat


def S3Loader(client: S3Client, bucket: str, key: str):
    """
    Load a file from an S3 bucket and return its contents.

    Parameters:
    client (boto3.client): The S3 client.
    bucket (str): The bucket name.
    key (str): The key name.

    Returns:
    Any: The contents of the file.
    """

    try:
        response = client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read().decode("utf-8")

    except ClientError as err:
        raise ValueError(f"An error occurred: {err}")


class FileLoader:
    """
    A class that loads files and returns their contents. It can be initialized by specifying the file
    location and file format. Optionally, a logger object can be passed to log messages and errors.
    """

    def __init__(self, file: str, logger: Optional[logging.Logger] = None):
        self.file: str = file
        self.file_format: str = ""
        self.location_type: str = ""

        self._set_file_type()
        self._set_location_type()

        self.logger: logging.Logger = (
            self._create_logger() if logger is None else logger
        )

        return None

    def _create_logger(self):
        """
        Create a logger object and return it.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger

    def _set_file_type(self):
        if self.file.endswith(".json"):
            self.file_format = "json"
        elif self.file.endswith(".csv"):
            self.file_format = "csv"
        elif self.file.endswith(".tsv"):
            self.file_format = "tsv"
        elif self.file.endswith(".yml"):
            self.file_format = "yaml"
        elif self.file.endswith(".yaml"):
            self.file_format = "yaml"
        else:
            raise ValueError("Unsupported file format")

    def _set_location_type(self):
        if self.file.startswith("http"):
            self.location_type = "url"
        elif self.file.startswith("s3://"):
            self.location_type = "s3"
        else:
            self.location_type = "local"

    def load_file(self) -> Any:
        """
        Load a file and return its contents based on the file format and location type.
        """
        if self.location_type == "local":
            return self.load_from_local()
        elif self.location_type == "s3":
            return self.load_from_s3()
        elif self.location_type == "url":
            return self.load_from_url()
        else:
            raise ValueError("Unsupported location type")

    def load_from_s3(self) -> Any:
        session = boto3.Session()
        s3 = session.client("s3")

    def load_from_url(self) -> Any:
        pass

    def load_from_local(self) -> Any:
        pass
