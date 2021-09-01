#-------------------------------------------------------------------------------
# Title:       mxdToAprx.py
# Author:      Mary Grace McClellan
# Created:     12/30/2019
# Revised:     4/21/2021 
# Summary:     Create ArcGIS Pro projects from MXDs. Result will be project
#              folder for each .MXD in the input folder. 
# Requirements: A blank .aprx Pro project to use as a template.
# Version: Python 3.6.9
#-------------------------------------------------------------------------------

import arcpy
import os
import logging
import shutil

def mxdToAprx(folder, template, new_folder, log_file):
    
    # Set environmental variables
    arcpy.env.workspace = folder
    arcpy.env.overwriteOutput = True

    # Log file configuration
    logging.basicConfig(filename=log_file,
                    format='%(asctime)s %(levelname)s\n%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

    try:
            
        # Import each MXD into the blank project, rename map frame, save new project
        for mxd in arcpy.ListFiles('*.mxd'):

            # Set variables
            #aprx = arcpy.mp.ArcGISProject(blank)
            mapdoc = os.path.join(folder, mxd)
            base_name = mxd.split('.mxd')[0]
            proj_name = base_name + '.aprx'
            new_proj_folder = os.path.join(new_folder, base_name)
            new_proj = os.path.join(new_proj_folder, proj_name)
            default_gdb = os.path.join(new_proj_folder, base_name + '.gdb')
            default_tbx = os.path.join(new_proj_folder, base_name + '.tbx')
            logging.info('f{base_name.upper} --------------------- \n')

            # Make a copy of template project folder in destination folder
            shutil.copytree(template, new_proj_folder)

            # Rename copied folder to MXD name
            for root, dirs, files in os.walk(new_proj_folder):
                for name in files:
                    item = os.path.join(new_proj_folder, name)
                    if '.aprx' in name:                        
                        shutil.move(item, new_proj)
                    elif '.tbx' in name:
                        shutil.move(item, default_tbx)
                    else:
                        pass
                for name in dirs:
                    item = os.path.join(new_proj_folder, name)
                    if 'Index' in name:
                        shutil.rmtree(item)
                    elif 'ImportLog' in name:
                        shutil.rmtree(item)
                    elif '.gdb' in name:
                        shutil.move(item, default_gdb)
                    else:
                        pass

            logging.info(f'Moved and renamed files for {new_folder}')
            
            # Create project object from new project
            new_aprx = arcpy.mp.ArcGISProject(new_proj)
            
            # Import MXD into project
            new_aprx.importDocument(mapdoc, include_layout=False)
            logging.info(f'Imported {mxd} to {proj_name} \n')

            # Rename 'Layers' to MXD name
            layers = new_aprx.listMaps()[0]
            old_name = layers.name
            layers.name = base_name
            logging.info(f'Renamed {old_name} to {base_name} \n')            
            
            # Set default home folder, gdb, and tbx for new project
            new_aprx.homeFolder = new_proj_folder
            new_aprx.defaultGeodatabase = default_gdb
            new_aprx.defaultToolbox = default_tbx
            logging.info(f'Set defaults {proj_name} \n')

            # Save changes made to new project
            new_aprx.save()
            logging.info(f'Saved changes {proj_name} \n \n \n')
        
    except Exception as error:
        logging.warning(f'{mxd} ERROR: {str(error)}\n \n \n')
        output = error
        print(f'\tError importing {mxd}')


    return

                      
if __name__ == '__main__':

    #Set variables
    folder = r'<folder with MXDs to convert>'
    template = r'<template folder containing .APRX and other files for copying>'
    new_folder = r'<folder location for saving new projects>'
    log_file = r'<path to .log file that will be created>'

    # Log file configuration
    logging.basicConfig(filename=log_file,
                    format='%(asctime)s %(levelname)s\n%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

    mxdToAprx(folder, template, new_folder, log_file)

        
        
        
