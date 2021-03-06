# -*- coding: utf-8 -*-

###########################
###    Load packages    ###
###########################

import os
import os.path
import unittest

from keypy.preprocessing.file_info_classes import *
from keypy.preprocessing.data_loading import *
from keypy.preprocessing.avg_referencing import *
from keypy.preprocessing.filtering import *
from keypy.preprocessing.helper_functions import *


class Test_a_mstates_preprocessing_test5(unittest.TestCase):
    def test_a_mstates_preprocessing_test5(self):
        ###########################
        ### Run Study Info File ###
        ###########################

        #enter number of channels
        nch=2
        #enter number of time frames for each segment
        tf = 4
        #enter sampling rate
        sf = 2
        # enter your channel list in the same order as in your files
        chlist=['FP1','AF7']

        #create object of EEG info information
        eeg_info_study_obj = EegInfo(nch, tf, sf, chlist)

        ################################
        ### Specify data folder info ###
        ################################

        library_path = os.path.dirname(os.path.abspath(__file__))

        inputfolder = os.path.join(library_path, "..","data","test5")
        outputfolder = os.path.join(library_path, "..","data","test5_output")

        if not os.path.exists(outputfolder):
            os.makedirs(outputfolder)

        outputhdf5 = os.path.join( outputfolder, 'all_recordings.hdf')
        loaddata_output = 'rawdata'

        ########################
        ## Specify data info ###
        ########################

        ##Where in the filename is the following information (at which index of the string)? inclusive
        ##Where in the folder structure is the following information? 0 outtermost folder, 1 second folder, 2 third folder
        ##Specify for each element (group, partcipant, condition, run) whether the information is in the filename or folder structure.

        #group
        group_indices_range = [0,1]
        group_folder_level = 0
        has_group = 'none' ###can be 'folder', 'filename', or 'none'

        #participant
        participant_indices_range = [3,5]
        participant_folder_level = 0
        has_participant = 'none'

        #condition
        condition_indices_range = [0,0]
        condition_folder_level = 1
        has_condition = 'none'

        #run
        run_indices_range = [0,0]
        run_folder_level = 0
        has_run = 'filename'

        file_ending = 'txt'

        ##Generate objects based on info above

        file_name_obj = FileNameDescription(group_indices_range, participant_indices_range, condition_indices_range, run_indices_range, file_ending)
        folder_structure_obj = FolderStructureDescription(group_folder_level, participant_folder_level, condition_folder_level, run_folder_level)
        filename_folder_obj = FilenameFolderDescription(has_group, has_participant, has_condition, has_run)

        ########################
        ###Load Data to HDF 5###
        ########################

        loaddata(inputfolder, outputhdf5, loaddata_output, file_name_obj, folder_structure_obj, filename_folder_obj, eeg_info_study_obj)

        ########################
        ###Compute Avg Ref   ###
        ########################

        inputhdf5 = os.path.join( outputfolder, 'all_recordings.hdf')

        average_input = 'rawdata'
        average_output = 'avg_ref'

        averageref(inputhdf5, average_input, average_output )


        #################################
        ###  Filter for microstates   ###
        #################################

        ######
        ###Use detrending before filtering?
        ######
        enable_detrending = True

        ######
        ###Choose Filter Settings
        ######
        filter_settings = {
            "mstate1": {
                "low": 2.0,
                "high": 20
            },
            "mstate2": {
                "low": 1.5,
                "high": 30
            },
            "mstate3": {
                "low": 1.5,
                "high": 45
            }
        }


        ######
        ###HDF5 File Preparation
        ######
        #define processing stage of input and name of output
        filter_input = 'avg_ref'
        filter_output = filter_settings

        ######
        ###Inputhdf (Outputhdf from before)
        ######

        inputhdf5 = os.path.join( outputfolder, 'all_recordings.hdf')

        boxkeyfilter(inputhdf5, eeg_info_study_obj, filter_input, filter_settings, enable_detrending)
