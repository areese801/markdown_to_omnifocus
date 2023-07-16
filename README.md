# Use Case

If you want to be able to create To-Do items in Markdown syntax in your note files (e.g. Notes created with [Obsidian](https://obsidian.md/)), but have those materialize in [Omnifocus](https://www.omnigroup.com/omnifocus/) then this package is for you.

In other words: Type away, making your notes fast and furiously. When a To-do item pops into your mind, no need to switch apps, just make your To-do item in your markdown file and stay in the zone.

# Why would I want to use this utility?

- Because notes kept in [Markdown](https://www.markdownguide.org/basic-syntax/) are very portable. Since they're plain text, they're compatible with a wide variety of tools.
  - This author's favorite tool is [Obsidian](https://obsidian.md/), but you're not limited to any one tool
- Because while To-Do items in Markdown are nice, there's no denying the power of [Omnifocus](https://www.omnigroup.com/omnifocus/). (Scheduling, Reminders, Tagging, etc)

# How does this tool work?

At a high level, here's what happens:

1. When invoked, the tool traverses a directory (e.g. Obsidian Vault Directory) looking for Markdown files with a `.md` file extension.
2. These files are inspected for _Incomplete_ To-Do items using regular expression pattern matching, looking for To-Do's that look like: `- [ ] Buy Milk`
3. Any To-Do items are "migrated" to Omnifocus
   - There is a basic check on file timestamp to try to ensure that To-Do items that are still being typed out aren't migrated into Omnifocus prematurely.
   - There is a basic check to try to avoid edge cases where a to-do with the same wording in different places would be created in Omnifocus more than once
4. Migrated To-Do items from `.md` files are 'crossed out' in the markdown file with a link to the corresponding task in Omnifocus to denote they've been migrated
5. Migrated To-Do items created in Omnifocus will contain the Task description as well as an [Obsidian URI](https://help.obsidian.md/Advanced+topics/Using+obsidian+URI) that points back to the file the To-Do was parsed out of
   - This linkage may be imperfect, especially if the file is moved or renamed.
   - However, in testing, basic file moves within Obsidian did not break the functionality

# Compatibility

This tool was created on a Mac using Python3. It was tested on that Mac and worked fine there. I would expect that this code work on Windows, but there may be some minor bugs as I didn't test for Windows. If you care to do so and encounter an issue, please get in touch with [Adam Reese](https://github.com/areese801) and/or fix it yourself and create a pull request.

# Setup

### Get the latest version of the code

Clone or Download and Extract the code from the repository to your preferred destination. `~/scripts` is a good spot if you're not sure where else to put it.

### Configure config files

There is 1 config file1 you'll need to create under the `config` folder:

- `config.json` which contains config for the program itself

#### Configure `config.json`

- As of this writing (2022-12-20), the only thing to configure in this file is the base directory (for example: `~/Obsidian`) where markdown files and subdirectories with more markdown files can be found.
- Make a copy of the file and remove the comments to make it valid JSON

# Using the tool (Manually)

### Just to see To-Do items

If you just want to print a list of your To-Do's but not "Migrate" them, as described above you can use `find_tasks.py` like this:

```bash
python find_tasks.py
```

Alternatively, you can use the wrapper script that's intended to place nicely with `pyenv`

```bash
./find.sh
```

### To Migrate To-Do items into Obsidian

# TODO: Put wording here

# To Exclude Specific files from To-Do Migration

If you want to exempt a specific file from having its to-do items migrated to Todoist, simply specify `omnifocus: false` in the YAML front matter at the top of the file.

For Example, a Packing list template for trips might look like the below. It's a checklist, but you might not want to actually make To-do items for everything in that template:

```yaml
---
tags:
  - Template
  - Travel
todoist: false
---
# Daily Clothing

- [ ] Shoes
- [ ] Socks
- [ ] Pants
- [ ] Shorts
```

# Automation

### On macOS or Linux

You can automate `migrate_tasks.py` on macOS (Or anything **\*nix**) using a `cron` entry. This set up is out of scope to describe here, but for the unfamiliar [here is a good place to start](https://www.howtogeek.com/101288/how-to-schedule-tasks-on-linux-an-introduction-to-crontab-files/). As an example, you might make a `crontab` entry like this:

```bash
# Parse to-do items out of Markdown files and create corresponding to-do's in Todoist
0 */1 * * 1-5 cd ~/path/to/wherever/you/have/this/script && python migrate_tasks.py > /tmp/migrate_tasks.log 2>&1
```

You can use [this website](https://crontab.guru/) to help generate and validate your crontab schedules

### On Windows

As mentioned above, this script hasn't been tested on Windows, but should work without requiring too much (or any) fixing. On Windows, instead of cron, you'd want to use the [Windows Task Scheduler](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10), the set-up for which is out of scope to describe here.

# About synchronization

### Synchronization should just work

If you've set up any kind of Synchronization for your Markdown notes ([Obsidian Sync](https://obsidian.md/sync), [Dropbox](https://www.dropbox.com/), [Syncthing](https://syncthing.net/), etc), this tool should, in-theory, work without any issue, but please let [Adam Reese](https://github.com/areese801) know and/or fix it yourself and create a pull request if you encounter any issues.

This was tested with Obsidian Sync, and it worked fine.

### Ok, but why "should it just work"?

When a task is "migrated", this tool modifies the markdown file that that task was parsed from on-the-fly.

So a task that looks like this, pre-migration:

![](./_resources/Pasted%20image%2020221220110643.png)

Will end up looking like this, post-migration:

![](./_resources/Pasted%20image%2020221220110655.png)

Visually, in Obsidian the syntax from the screen prints above renders like this, before and after
Before:

![](./_resources/Pasted%20image%2020221220110918.png)

After:

![](./_resources/Pasted%20image%2020221220110807.png)

Here's what the generated task in Todoist Looks like:

![](./_resources/Pasted%20image%2020221220110455.png)
