import argparse
import config
from datetime import datetime, timedelta
import mytodoist as mt
import mystrings as s
import os 

def parse_commandline(default_start, default_end):
    parser = argparse.ArgumentParser(description='View completed tasks - input parameters')
    parser.add_argument('-tz', action='store', dest='current_timezone', default=s.DEFAULT_TIMEZONE)
    parser.add_argument('-start', type=lambda s: datetime.strptime(s, '%Y-%m-%d'), action='store', dest='start_date', default=default_start) 
    parser.add_argument('-end', type=lambda s: datetime.strptime(s, '%Y-%m-%d'), action='store', dest='end_date', default=default_end)
    parser.add_argument('-savefile', action='store', dest='savefile', default=False)
    args = parser.parse_args()
    return args

def save_view_to_csv(start_date, end_date):
    filename = mt.get_timestamped_filename(s.COMPLETED_TASKS_FILENAME,start_date,end_date,s.DATETIME_FORMAT,'.csv')
    filename = mt.get_user_filepath(s.DEFAULT_USER_FOLDER, filename)
    mt.save_dataframe_to_csv(df_completed_tasks[print_columns], filename)
    print('File saved to ' + filename)


# Set defaults 
default_end = datetime.now()
default_start = default_end - timedelta(days=7)

# Use command line arguments
args = parse_commandline(default_start, default_end)
start_date = args.start_date 
end_date = args.end_date 
current_timezone = args.current_timezone
savefile = args.savefile

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
sort_columns = s.VIEW_COMPLETED_SORT 
sort_asc = s.VIEW_COMPLETED_SORT_ASC 
df_completed_tasks = mt.sort_dataframe(df_completed_tasks, sort_columns, sort_asc)

# Print out tasks with specific columns
print_columns = s.VIEW_COMPLETED_PRINT 
print(df_completed_tasks[print_columns])

# Save completed tasks to file - include start/end dates in the filename
if(savefile):
    save_view_to_csv(start_date,end_date)