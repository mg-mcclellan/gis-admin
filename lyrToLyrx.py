#--------------------------------------------------------------
# Title: lyrToLyrx.py
# Author: Mary Grace McClellan
# Date created: August 26, 2021
# Summary: This script was created to convert .LYR files in a
#          folder to the new .LYRX format supported by
#          ArcGIS Pro.
# Version: Python 3.6.9
#--------------------------------------------------------------

import os
import arcpy
import logging


def lyrToLyrx(lyrFolder, lyrxFolder, logPath):
    logging.basicConfig(filename=logPath, level=logging.DEBUG)
    for dirName, subdirList, fileList in os.walk(lyrFolder):
        try:
            for layer in fileList:
                lyr = os.path.join(lyrFolder, layer)
                base = layer.split('.lyr')[0]
                lyrx = os.path.join(lyrxFolder, base + '.lyrx')

                if os.path.exists(lyrx):
                    pass
                else: 
                    arcpy.management.SaveToLayerFile(lyr, lyrx)
                    logging.info(f'Converted {lyr} to {lyrx}')
        except Exception as e:
            print('Not converted: ', base)
            logging.warning(e)
            pass

    return


if __name__ == '__main__':

    lyrFolder = r'<folder with .LYR files>'
    lyrxFolder = r'<folder to store new .LYRX files>'
    logPath = r'<file location to store .log document'

    lyrToLyrx(lyrFolder, lyrxFolder, logPath)


