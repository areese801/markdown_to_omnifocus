"""
Code having to do with migrating tasks read from Markdown files into Omnifocus

Rather than having to try to come up with some tricky way to sync and keep track
of (potentially renamed) files across multiple machines, I decided to
build functionality to 'migrate' tasks into omnifocus on the fly with a standard
convention to denote those having been migrated.  This approach allows me to
avoid duplications, forget about tracking file names and locations, and
take advantage of the very nature of sync.
"""
import os.path
import sys
from find_tasks import find_tasks
from config import _read_base_dir_from_config
import re
import datetime
from datetime import timezone
from hashing import make_task_hash


def migrate_tasks(parent_directory:str = '~/Obsidian'):
	"""
	Migrates open tasks into Omnifocus by creating a task in todoist then modifying the markdown
	File / line from where the task was encountered
	"""

	# TODO:  Read the parent directory path out of a config file

	tasks_from_markdown_files = find_tasks(parent_directory=parent_directory)

	# Exit if there's nothing to do
	if not tasks_from_markdown_files:
		# Nothing to do
		print(f"There are no tasks to migrate.  Call to find_tasks results in: {str(tasks_from_markdown_files)}")
		return


	# TODO:  Some way to get a list of existing tasks from Omnifocus in order to try to not duplicate them

	recently_modified_files = [] #Tracks files that were modified by current invocation.  To not-skip due to modify time.

	for task_dict in tasks_from_markdown_files:

		"""
		Check the last modified time of the file.  If it's less than X seconds ago, don't bother with it
		The idea here is to not ship incomplete to-do items that the user might still by typing out into to
		Omnifocus prematurely.  For example, if this program was scheduled on a cron job
		"""

		markdown_file_name = task_dict['file_name']

		# take note of the current timestamp in UTC
		right_now = datetime.datetime.now(timezone.utc)
		right_now_utc_timestamp = right_now.timestamp()

		# take note of the timestamp on the file
		file_last_modified_timestamp = os.path.getmtime(markdown_file_name)

		time_diff_sec = right_now_utc_timestamp - file_last_modified_timestamp
		if file_last_modified_timestamp > right_now_utc_timestamp or time_diff_sec < 60:  # TODO:  This 60-second threshold should be read out of a config file
			
			# The file is too new.  Skip it.
			if markdown_file_name not in recently_modified_files:
				# We might have just modified a file due to another to-do item, thus changing its timestamp.  It's okay to modify again in this case
				continue





	print("!")

if __name__ == '__main__':
	migrate_tasks()
