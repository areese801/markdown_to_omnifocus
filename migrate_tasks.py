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

from omnifocus import create_task


def migrate_tasks(parent_directory:str = '~/Obsidian'):
	"""
	Migrates open tasks into Omnifocus by creating a task in Omnifocus then modifying the markdown
	File / line from where the task was encountered
	"""

	# TODO:  Read the parent directory path out of a config file

	tasks_from_markdown_files = find_tasks(parent_directory=parent_directory)

	# Exit if there's nothing to do
	if not tasks_from_markdown_files:
		# Nothing to do
		print(f"There are no tasks to migrate.  Call to find_tasks results in: {str(tasks_from_markdown_files)}")
		return

	recently_modified_files = []  # Tracks files that were modified by current invocation.  To not-skip due to modify time.

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

		"""
		Make the task in Omnifocus
		"""
		task_name = task_dict['task']
		task_from_file_name = task_dict['file_name']
		task_from_obsidian_uri = task_dict['obsidian_uri']

		# Beautify the task name by removing [[Brackets]] from names, etc
		re_pattern = r'(\[\[)([^]]+)(\]\])'  # Matches: [[Jamie Hepner]] and returns Jamie Hepner in group 2
		re_replacement = r'\2'
		task_name_no_brackets = re.sub(pattern=re_pattern, repl=re_replacement, string=task_name)

		# Whip up a block of text to serve as the description
		task_description = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - \n\n"
		task_description += f"Parsed from Obsidian file: \"{os.path.basename(task_from_file_name)}\" at the URI below:\n"
		task_description += f"Note:  If the file has been renamed or modified in Obsidian, this link may not work\n\n"
		task_description += f"{task_from_obsidian_uri}"
		task_description += "\n\n---"

		new_task_url = create_task(task_name=task_name_no_brackets, task_description=task_description)

		"""
		Construct a markdown string to replace the original with
		"""
		# Handle the markdown part of the task:  '- [ ] "
		markdown_todo_regex_pattern = "(^\s*- \[)( )(\]\s*)"
		arrow_character = "→" # Used to denote a 'migrated' task.  In markdown any char other than ' ' will signify complete.
		task_markdown_part = task_dict['markdown_part']  # This looks like:  '- [ ]'
		markdown_todo_regex_match = re.match(string=task_markdown_part, pattern=markdown_todo_regex_pattern)
		re_1 = markdown_todo_regex_match.group(1) # Looks like:  - [
		re_3 = markdown_todo_regex_match.group(3).rstrip() # Looks like:  ].  The empty space would be in group 2
		new_task_markdown_part = f"{re_1}{arrow_character}{re_3} "

		# Handle the part of the string that links to the new task in Omnifocus
		omnifocus_link_part = f" [(This Task Migrated to Omnifocus)]({new_task_url})"

		# Construct a complete line of text to replace the original to-do that was parsed from the file
		replacement_todo_string = f"{new_task_markdown_part}~~{task_dict['task']}~~{omnifocus_link_part}"

		# Print some logging stuff
		print("\nThe program will find and replace the following:")
		print(f"\tWithin the file '{markdown_file_name}'")
		print(f"\tThis string will be sought:            {task_dict['original_string']}")
		print(f"\tWhich will be replaced by the string:  {replacement_todo_string}")

		"""
		Replace the original line in the file with a to-do item on it with the new field that 
		show's it's been migrated to Omnifocus
		"""
		# Read the lines of the file first
		with open(markdown_file_name, 'r') as f:
			lines = f.readlines()

		# Modify the lines
		new_lines = []
		for line in lines:
			if line.strip().startswith(task_dict['original_string']):
				new_lines.append(replacement_todo_string)
			else:
				new_lines.append(line.rstrip())  # We don't want trailing \n char or we'll get doubles when we join
		new_file_data = "\n".join(new_lines)

		# Replace the lines of the original file with the new lines
		with open(markdown_file_name, 'w') as f:
			f.write(new_file_data)
			f.close()
		recently_modified_files.append(markdown_file_name) # Helps us merge many tasks from the same file in without TS check


if __name__ == '__main__':

	# Resolve the path to the vault.  If it's not passed in, get it from the config file
	args = sys.argv

	if len(args) >= 2:
		base_dir = args[1]
	else:
		base_dir = _read_base_dir_from_config()

	migrate_tasks(parent_directory=base_dir)

if __name__ == '__main__':
	migrate_tasks()
