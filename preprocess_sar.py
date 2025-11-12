import os
import esa_snappy
from esa_snappy import ProductIO, Product, ProductUtils, HashMap, GPF, GeoPos, PixelPos, WKTReader
import numpy as np


def calibrateGRD(product):
    """
    Apply radiometric calibration to convert raw SAR data to sigma0 values.
    """
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('outputSigmaBand', True)
    parameters.put('auxFile', 'Product Auxiliary File')
    calibrated = GPF.createProduct('Calibration', parameters, product)
    return calibrated


def speckleFilteringGRD(product):
    """
    Apply speckle noise filtering (Lee Sigma filter).
    """
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('filter', 'Lee Sigma')
    parameters.put('numLooksStr', '1')
    parameters.put('windowSize', '7x7')
    specklefiltered = GPF.createProduct('Speckle-Filter', parameters, product)
    return specklefiltered


def multilooking(product):
    """
    Perform multilooking to reduce speckle and improve pixel geometry.
    """
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('grSquarePixel', True)
    parameters.put('nAzLooks', '1')
    parameters.put('nRgLooks', '1')
    multilooked = GPF.createProduct('Multilook', parameters, product)
    return multilooked


def subset(product, wkt_geometry):
    """
    Crop the image to a region of interest (ROI) defined in WKT format.
    """
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('copyMetadata', True)
    geom = WKTReader().read(wkt_geometry)
    parameters.put('geoRegion', geom)
    subsetimg = GPF.createProduct('Subset', parameters, product)
    return subsetimg


def slant2grd(product):
    """
    Convert slant range geometry to ground range using terrain correction.
    """
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('auxFile', 'Product Auxiliary File')
    parameters.put('demName', 'SRTM 3Sec')
    parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('nodataValueAtSea', False)
    grd = GPF.createProduct('Terrain-Correction', parameters, product)
    return grd


def preprocess(sar_file, wkt_roi=None):
    """
    Complete SAR preprocessing chain:
    Calibration → Multilook → Speckle Filter → Terrain Correction → Subset (optional)
    """
    product = ProductIO.readProduct(sar_file)
    product = calibrateGRD(product)
    product = multilooking(product)
    product = speckleFilteringGRD(product)
    product = slant2grd(product)
    
    if wkt_roi is not None:
        product = subset(product, wkt_roi)

    out_name = f"./Preprocessed_{os.path.splitext(os.path.basename(sar_file))[0]}.tif"
    ProductIO.writeProduct(product, out_name, "GeoTIFF-BigTIFF")
    product.dispose()
    print('DONE!')


if __name__ == "__main__":
    # Example list of SAR files and ROIs
    list_sar_files = [
        './d4/920002698_2025-03-19T16_22_32Z/workvol/output/ICEYE_X39_SLC_SLH_920002698_20250315T022701.h5'
    ]
    list_wkt_roi = [None]

    for i in range(len(list_sar_files)):
        preprocess(list_sar_files[i], list_wkt_roi[i])
