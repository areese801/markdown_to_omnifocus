import urllib.parse
import requests

"""
This module contains functions for interacting with Omnifocus
"""


def create_task(task_name: str, task_description: str = '') -> str:
    """
    Create a task in Omnifocus using the Mac and iOS compatible URL scheme

    See:  https://inside.omnifocus.com/url-schemes

    :param task_name:  The content of the task
    :param task_description:  The description of the task
    :return:  The URL of the task
    """

    """
    Validate task name and description
    """
    if not task_name:
        raise ValueError(f"Task name needs to be passed in as a truthy string.  Got type {type(task_name)} of length {len(task_name)}")

    """
    Assemble parameters
    """
    percent_encoded_task_name = urllib.parse.quote(task_name)
    percent_encoded_task_description = urllib.parse.quote(task_description)

    # 'autosave=true' bypasses quick entry dialog.
    # https://discourse.omnigroup.com/t/url-schemes-to-inbox-directly/42489/2
    params = dict(name=percent_encoded_task_name, autosave='true')

    if task_description:
        params['note'] = percent_encoded_task_description

    params = {k: v for k, v in params.items() if v is not None}

    """
    Construct URL
    """
    base_url = r"omnifocus:///add?"
    url_params = "&".join([f"{k}={v}" for k, v in params.items()])
    url = base_url + url_params

    """
    "Request" the URL to take advantage of callback functionality
    """
    response = requests.get(url)
    print("!")


    print(url)


if __name__ == "__main__":
    create_task("test task", "test description")




