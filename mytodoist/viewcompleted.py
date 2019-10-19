import argparse
import config
from datetime import datetime, timedelta
import mytodoist as mt
import mystrings as s

# Set defaults 
default_end = datetime.now()
default_start = default_end - timedelta(days=7)

# Use command line arguments
args = mt.parse_commandline(default_start, default_end)
start_date = args.start_date 
end_date = args.end_date 
current_timezone = args.current_timezone

# Get project and task data from Todoist API
api = mt.initialize_todoist_api()
df_projects = mt.get_projects_df(api)
df_tasks = mt.get_tasks_df(api)

# Add parent projects and parent tasks to the tasks dataframe
df_tasks = mt.add_parent_projects_to_tasks(df_projects,df_tasks) 
df_tasks = mt.add_parent_tasks_to_tasks(df_tasks)

# Convert UTC to local timezone
df_tasks = mt.convert_datetimes_to_tz(df_tasks, current_timezone, s.DATETIME_FORMAT)

# Filter to completed tasks
df_completed_tasks = mt.filter_completed_tasks(df_tasks, start_date, end_date)

# Sort tasks
sort_columns = [s.PARENT_PROJECT, s.PROJECT_NAME, s.PARENT_PRIORITY, s.PARENT_ID, s.DATE_COMPLETED]
sort_asc = [True,True,False,True,True]
df_completed_tasks = mt.sort_dataframe(df_completed_tasks, sort_columns, sort_asc)

# Print out tasks with specific columns
print_columns = [s.PARENT_PROJECT, s.PROJECT_NAME, s.PARENT_PRIORITY,s.PARENT_TASK, s.PRIORITY, s.CONTENT, s.DATE_COMPLETED]
print(df_completed_tasks[print_columns])

# Save completed tasks to file
mt.save_dataframe_to_csv(df_completed_tasks, s.DEFAULT_FILE_COMPLETED)