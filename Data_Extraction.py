import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def read_dat_files(filepath=r'D:\Graduation Project\QuadPlane Design\APC Propellers\PERFILES_WEB\PERFILES2'):
    '''
    input:
        --> filepath: path to the folder containing the dat files
    output:
        --> datContent: list of lists. each list item is a list of all the lines in one file.
        e.g. datContent[i] is a list of the line inside file number i
    '''
    file_names_list = os.listdir(filepath)
    datContent = []
    for file_name in file_names_list:
        datContent.append([line.strip().split() for line in open(filepath + '\\' + file_name).readlines()])

    return datContent


def remove_empty_lines(dataframe):
    '''
    Empty lines are defined as the lines that has a null value in the first column.
    input:
        --> dataframe: pandas dataframe
    output:
        --> dataframe: pandas dataframe without any empty lines and a new index
    '''
    dataframe = dataframe.drop(dataframe.loc[dataframe[0].isnull()].index, axis=0)    # Dropping all empty lines
    dataframe = dataframe.reset_index().drop(['index'], axis=1)    # Resetting the index and removing the introduced old 'index' column by pandas.
    return dataframe


def get_prop_size(dataframe):
    '''
    input:
        --> dataframe: pandas dataframe with the propeller size stated at the first line in the shape of '123x45.67ABC'
    output:
        --> (prop_diameter, prop_pitch): tuple
    '''
    prop_size_str = dataframe[0][0]
    x_idx = prop_size_str.find('x')
    prop_diameter = float(prop_size_str[:x_idx])
    pitch_end_idx = len(prop_size_str)    # assuming that there is no letter after the pitch
    for char in prop_size_str[x_idx+1:]:
        if not char.isdigit() and char != '.':    # the char is a letter (not a dot)
            pitch_end_idx = prop_size_str.find(char)    # let this letter index be the end of the pitch number
            break
    prop_pitch = float(prop_size_str[x_idx+1:pitch_end_idx])
    return prop_diameter, prop_pitch

def remove_lines_before_rpm(dataframe):
    '''
    input:
        --> dataframe: pandas dataframe
    output:
        --> dataframe: pandas dataframe without the lines before the first rpm and a new index
    '''
    rpm_rows_idx_list = dataframe.loc[dataframe[0] == 'PROP'].index    # all the rows that have PROP in it
    first_rpm_idx = rpm_rows_idx_list[0]
    dataframe = dataframe.drop(range(first_rpm_idx), axis=0)    # dropping all lines before the first rpm
    dataframe = dataframe.reset_index().drop(['index'], axis=1)    # Resetting the index and removing the introduced old 'index' column by pandas.
    return dataframe


def add_diam_pitch_cols(dataframe):
    '''
    input:
        --> dataframe: pandas dataframe with the prop size in the first line.
    output:
        --> dataframe: pandas dataframe with two new columns for the diameter and the pitch of the prop.
    '''
    prop_diameter, prop_pitch = get_prop_size(dataframe)
    dataframe['diameter'] = prop_diameter
    dataframe['pitch'] = prop_pitch
    return dataframe

def add_rpm_col(dataframe):
    '''
    input:
        --> dataframe: pandas dataframe
    output:
        --> dataframe: pandas dataframe with the rpm added as a col beside each area.
    '''
    rpm_rows_idx_list = dataframe.loc[dataframe[0] == 'PROP'].index
    rpm_df = pd.DataFrame()    # an empty dataframe awaiting to be filled with rpm values in the correct index

    rpm_values_list = dataframe.loc[dataframe[0] == 'PROP'][3].to_list()    # still not a list
    rpm_values_list = [float(r) for r in rpm_values_list]
    for rpm_idx in range(len(rpm_values_list)):
        if rpm_idx < len(rpm_values_list) - 1:
            area_length = rpm_rows_idx_list[rpm_idx+1] - rpm_rows_idx_list[rpm_idx]
            rpm_np = np.dot(rpm_values_list[rpm_idx], np.ones((area_length, 1)))
        else:
            area_length = dataframe.shape[0] - rpm_rows_idx_list[rpm_idx] + 1
            rpm_np = np.dot(rpm_values_list[rpm_idx], np.ones((area_length, 1)))
        rpm_series = pd.Series(rpm_np[:,0], index=range(len(rpm_np[:,0])))
        rpm_df = rpm_df.append(pd.DataFrame(rpm_series), ignore_index=True)
    
    dataframe['rpm'] = rpm_df
    return dataframe

def remove_prop_rpm_lines(dataframe):
    '''
    input:
        --> dataframe: pandas dataframe
    output:
        --> dataframe: pandas dataframe without the rows starting with 'PROP' and with a new index
    '''
    rpm_rows_idx_list = dataframe.loc[dataframe[0] == 'PROP'].index    # all the rows that have PROP in it
    for rpm_idx in range(len(rpm_rows_idx_list)):
        dataframe = dataframe.drop(rpm_rows_idx_list[rpm_idx]+range(0,3), axis=0)    # dropping rpm lines and the 2 following lines
    dataframe = dataframe.reset_index().drop(['index'], axis=1)    # Resetting the index and removing the introduced old 'index' column by pandas.
    return dataframe

if __name__ == "__main__":
    big_df = pd.DataFrame()
    dat_files_list = read_dat_files()
    for dat_file in dat_files_list:
        file_df = pd.DataFrame(dat_file)    # converting the list of file lines into a dataframe
        file_df = remove_empty_lines(file_df)
        file_df = add_diam_pitch_cols(file_df)
        file_df = remove_lines_before_rpm(file_df)
        file_df = add_rpm_col(file_df)
        file_df = remove_prop_rpm_lines(file_df)
        file_df.columns = ['V', 'J', 'Pe', 'Ct', 'Cp', 'PWR', 'Torque', 'Thrust', 8, 'diameter', 'pitch', 'rpm']
        file_df = file_df.drop([8], axis=1)
        # with pd.option_context('display.max_rows', None, 'display.max_columns', 8):
        #     print(file_df)
        big_df = big_df.append(file_df, ignore_index=True)
    with pd.option_context('display.max_rows', 10, 'display.max_columns', 8):
        print(big_df)
    big_df.to_csv(r'D:\Graduation Project\QuadPlane Design\APC Propellers\PERFILES_WEB\all_props.csv', index=False)
