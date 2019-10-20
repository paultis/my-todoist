# Default values
COMPLETED_TASKS_FILENAME = 'completed_tasks'
DEFAULT_TIMEZONE = 'America/Los_Angeles'
DEFAULT_USER_FOLDER = 'Desktop'
DATETIME_FORMAT = '%Y-%m-%d'  # %H:%M:%S'

# Todoist field names, collections
CHECKED = 'checked'
CONTENT = 'content'
DATE_ADDED = 'date_added'
DATE_COMPLETED = 'date_completed'
ID = 'id'
ITEMS = 'items'
NAME = 'name'
PARENT_ID = 'parent_id'
PRIORITY = 'priority'
PROJECTS = 'projects'

# Calculated fields, views
PARENT_PRIORITY = 'parent_priority'
PARENT_PROJECT = 'parent_project'
PARENT_TASK = 'parent_task'
PROJECT_NAME = 'project_name'
VIEW_COMPLETED_PRINT = [CONTENT, PARENT_TASK, PROJECT_NAME, PARENT_PROJECT, PARENT_PRIORITY,PRIORITY, DATE_COMPLETED]
VIEW_COMPLETED_SORT = [PARENT_PROJECT, PROJECT_NAME, PARENT_PRIORITY, PARENT_ID, DATE_COMPLETED]
VIEW_COMPLETED_SORT_ASC = [True,True,False,True,True]
