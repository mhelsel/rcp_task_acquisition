# CLARA_DLC
Adaptation of deeplabcut for video acquisition and analysis using the BioElectrics Lab CLARA (closed-loop automated reaching apparatus)

# Quick Code Overview
Entrypoint is multiCam_DLC/multiCamDLC_videoAcquisition_v1.py

visual stimulus  configs should be stored in a .yaml file in stimulus_config_files
screen/user and other configs are stored in config_files

if moving file/file path locations, must change the hardcoded paths in utils/file_utils.py
    there are some paths also in userdata.yaml so check if that should be updated as well
    
updating the labjack inputs or outputs is in models/Inputs.py

testing/labjack_test.py is used to manually graph labjack file- used to visually check the output from the labjack

# Gui Overview
some important notes for using the gui for the first time

-start session: enables cameras(if not done already), starts labjack (if not done already), records and presents stimulus. Note: This 
    is the only way currently to create a labjack_data.csv
-initialize labjack: starts the labjack. note: this does not record a labjack_data.csv. 
-config file dropdown: to select a config file stored in the stimulus_config_files folder. once the correct file is selected, it will run when
    start session/present stimulus is ran, there are no other actions that need to be taken
-update configs list: if a visual stimulus config is created while the gui is open, then this button will update the dropdown to include this new 
    file