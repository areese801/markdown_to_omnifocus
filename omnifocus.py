from python_xcall import xcall
import sys

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
    'autosave=true' bypasses quick entry dialog.
    """

    # https://discourse.omnigroup.com/t/url-schemes-to-inbox-directly/42489/2
    params = dict(name=task_name, autosave='true')

    if task_description:
        params['note'] = task_description

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
    print(f"Adding Task '{task_name}'\n\t{url}")
    # response = python-xcall.xcall(url=url)
    action_params=dict(name=task_name, autosave='true')
    if task_description:
        action_params['note'] = task_description

    response = xcall.xcall(scheme='omnifocus', action='add', action_parameters=action_params)

    # The response has the  URL scheme that corresponds with the new task
    new_task_url = response['result']
    print(f"The task was created.  It can be found at {new_task_url}")

    return new_task_url


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments were passed in
        raise ValueError("A task name needs to be passed in as a truthy string")
    elif len(sys.argv) == 2:
        # Task without description was passed in
        task_name = sys.argv[1]
        create_task(task_name=task_name)
    elif len(sys.argv) == 3:
        # Task with description was passed in
        task_name = sys.argv[1]
        task_description = sys.argv[2]
        create_task(task_name=task_name, task_description=task_description)
    else:
        raise ValueError("Too many arguments were passed in.  Only a task name and description are supported.  "
                         "Be sure to quote them if they contain spaces.")






