# SAR Preprocessing with SNAP (esa_snappy)

Automated preprocessing pipeline for Synthetic Aperture Radar (SAR) imagery using the **ESA SNAP** Python API (`esa_snappy`).

This tool applies the full preprocessing chain required for analysis-ready SAR products:
- Radiometric Calibration  
- Multilooking  
- Speckle Filtering  
- Terrain Correction  
- (Optional) Subset extraction via ROI in WKT format  

---

## Features

- Compatible with Sentinel-1, ICEYE, TerraSAR-X, and similar SAR formats supported by SNAP  
- Generates **GeoTIFF-BigTIFF** outputs  
- Modular functions for each preprocessing step  
- Optional ROI clipping using WKT geometry  

---

## Installation

1. Install [ESA SNAP](https://step.esa.int/main/download/)  
2. Configure `esa-snappy` by running:

```bash
snap --nogui --modules --update-all
snappy-conf
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Run directly:

```bash
python preprocess_sar.py
```

### Example ROI (WKT format):

```python
from preprocess_sar import preprocess

wkt_roi = "POLYGON((-47.92 -15.78, -47.85 -15.78, -47.85 -15.83, -47.92 -15.83, -47.92 -15.78))"
preprocess("input_file.h5", wkt_roi)
```

Output:
```
Preprocessed_input_file.tif
```

---

## Example Jupyter Notebook

See [`examples/sample_run.ipynb`](examples/sample_run.ipynb) for a minimal example on how to preprocess SAR files programmatically.

---

## Project Structure

```
sar-preprocessing-snappy/
├── preprocess_sar.py           # Main pipeline
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── LICENSE                     # MIT license
└── examples/
    └── sample_run.ipynb        # Usage example
```

---

## Processing Chain

```
SAR Input (.SAFE / .H5)
        ↓
Radiometric Calibration
        ↓
Multilooking
        ↓
Speckle Filtering (Lee Sigma)
        ↓
Terrain Correction (SRTM 3Sec)
        ↓
[Optional] Subset by WKT ROI
        ↓
GeoTIFF Output
```

---

## Example Command-Line Workflow

```bash
# Clone repository
git clone https://github.com/<your_username>/sar-preprocessing-snappy.git
cd sar-preprocessing-snappy

# Install dependencies
pip install -r requirements.txt

# Run the preprocessing script
python preprocess_sar.py
```

---

## Parameters Overview

| Step | Operator | Key Parameters |
|------|-----------|----------------|
| Calibration | `Calibration` | `outputSigmaBand=True`, `auxFile=Product Auxiliary File` |
| Multilook | `Multilook` | `grSquarePixel=True`, `nAzLooks=1`, `nRgLooks=1` |
| Speckle Filter | `Speckle-Filter` | `filter=Lee Sigma`, `windowSize=7x7` |
| Terrain Correction | `Terrain-Correction` | `demName=SRTM 3Sec`, `imgResamplingMethod=BILINEAR_INTERPOLATION` |
| Subset | `Subset` | `geoRegion=WKT geometry` |

---

## Notes

- The output products are written as **GeoTIFF-BigTIFF** for large datasets.  
- The script automatically loads all SNAP operator SPIs.  
- Ensure SNAP has access to DEM data (e.g., SRTM) for the terrain correction step.  

---


## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

