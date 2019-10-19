import argparse
import config
import todoist
import mystrings as s
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def parse_commandline(default_start, default_end):
    parser = argparse.ArgumentParser(description='View completed tasks - input parameters')
    parser.add_argument('-tz', action='store', dest='current_timezone', default=s.DEFAULT_TIMEZONE)
    parser.add_argument('-start', action='store', dest='start_date', default=default_start) 
    parser.add_argument('-end', action='store', dest='end_date', default=default_end)
    args = parser.parse_args()
    return args


def initialize_todoist_api():
    todoist_api = todoist.TodoistAPI(config.access_token)
    todoist_api.sync()
    return todoist_api


def get_projects_df(todoist_api):
    # Creating DataFrame of projects from 'projects' list of dicts
    # .data attribute retrieves a python dictionary rather than todoist.models.Project
    projects = [project.data for project in todoist_api.state[s.PROJECTS]] 
    df = pd.DataFrame(projects)
    return df


def get_tasks_df(todoist_api):
    tasks = [task.data for task in todoist_api.state[s.ITEMS]]
    df = pd.DataFrame(tasks)
    return df


def add_parent_projects_to_tasks(df_p, df_t):
    # Adds "project parent" column to projects dataframe
    map_project = dict(df_p[[s.ID, s.NAME]].values) 
    df_p[s.PARENT_PROJECT] = df_p.parent_id.map(map_project)
    map_project_parent = dict(df_p[[s.ID, s.PARENT_PROJECT]].values) 

    # Use these mappings to create task columns with tasks' project name and parent project
    df_t[s.PROJECT_NAME] = df_t.project_id.map(map_project)
    df_t[s.PARENT_PROJECT] = df_t.project_id.map(map_project_parent)
    return df_t


def add_parent_tasks_to_tasks(df_t):
    # Create maps to create task columns with parent task, and parent task priority
    map_task = dict(df_t[[s.ID, s.CONTENT]].values) 
    map_priorities = dict(df_t[[s.ID, s.PRIORITY]].values)
    df_t[s.PARENT_TASK] = df_t.parent_id.map(map_task)
    df_t[s.PARENT_PRIORITY] = df_t.parent_id.map(map_priorities)
    
    # Fill in values when task is top leel
    df_t[s.PARENT_PRIORITY] = np.where(pd.isnull(df_t[s.PARENT_TASK]), df_t[s.PRIORITY], df_t[s.PARENT_PRIORITY])
    df_t[s.PARENT_TASK] = np.where(pd.isnull(df_t[s.PARENT_TASK]), df_t[s.CONTENT], df_t[s.PARENT_TASK])
    df_t[s.PARENT_ID] = np.where(pd.isnull(df_t[s.PARENT_ID]), 0, df_t[s.PARENT_ID])
    return df_t


def convert_datetimes_to_tz(df, timezone, datetime_format):
    # Convert Date strings (in UTC by default) to datetime and format it 
    df[s.DATE_ADDED] = pd.to_datetime(
	    (pd.to_datetime(df[s.DATE_ADDED], utc=True)
	    .dt.tz_convert(timezone) 
	    .dt.strftime(datetime_format))) 
    df[s.DATE_COMPLETED] = pd.to_datetime(
	    (pd.to_datetime(df[s.DATE_COMPLETED], utc=True)
        .dt.tz_convert(timezone)
        .dt.strftime(datetime_format)))
    return df


def filter_completed_tasks(df_t, start_date, end_date):
    # Filter rows to those that are completed (checked) in the start/end windows
    mask = (df_t[s.DATE_COMPLETED] >= start_date) & (df_t[s.DATE_COMPLETED] <= end_date) & (df_t[s.CHECKED] == 1) 
    df_t = df_t[mask]
    return df_t


def sort_dataframe(df, columns, asc):
    df = df.sort_values(columns, ascending=asc)
    return df


def save_dataframe_to_csv(df, filename):
    df.to_csv(s.DEFAULT_FILE_COMPLETED, index = False, encoding='utf8')

