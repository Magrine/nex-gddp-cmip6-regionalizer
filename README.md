<h1 align="center">NEX-GDDP CMIP6 REGIONALIZER</h1>

<p align="center">
A pipeline for downloading, cropping, masking, and merging NEX-GDDP CMIP6 climate datasets into regionalized NetCDF files.
</p>

---

## 🌍 Overview

**nex-gddp-cmip6-regionalizer** is a command-line tool that automates the full workflow for generating **regionalized CMIP6 climate datasets** from NASA's **NEX-GDDP-CMIP6** archive.

This tool performs:

- ✔ Model, scenario, and variable selection  
- ✔ Download of downscaled daily CMIP6 datasets  
- ✔ Geographic cropping (bounding box)  
- ✔ Multi-region masking  
- ✔ Yearly file generation  
- ✔ Automatic merging into a single regional NetCDF  

Ideal for climate analytics, environmental modeling, agriculture, hydrology, and impact studies.

---

## 🌐 Official Data Source (NASA)

This tool uses the publicly available, bias-corrected downscaled CMIP6 archive:

🔗 **https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6**

Resolution: **~25 km**, daily timestep, bias corrected using LOCA2.

---

## ⚠️ Important Notice: Model & Variable Availability

Not all CMIP6 models include every variable in the NEX-GDDP-CMIP6 archive.

Some have **missing variables** (404 on download), and others only include data for:

- historical  
- historical + partial SSPs  
- no SSPs  
- missing radiation or humidity variables  

Below is a summary table based on NASA’s documentation.

---

## 📊 CMIP6 Model × Variable Availability

Legend:  
- 🟩 **Available (historical + SSPs)**  
- 🟨 **Partially available (historical + some SSPs)**  
- 🟥 **Not available**  


Always check this table before selecting models and variables to avoid failed downloads.

| Model            | Variant   | hurs | huss | pr  | rlds | rsds | sfcWind | tas | tasmax | tasmin |
|------------------|-----------|:----:|:----:|:---:|:----:|:----:|:-------:|:---:|:------:|:------:|
| ACCESS-CM2       | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| ACCESS-ESM1-5    | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| BCC-CSM2-MR      | r1i1p1f1  | 🟥 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| CanESM5          | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| CESM2-WACCM      | r4i1p1f1  | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟥 | 🟩 | 🟥 | 🟥 |
| CESM2            | r3i1p1f1  | 🟩 | 🟩 | 🟩 | 🟨 | 🟩 | 🟥 | 🟩 | 🟥 | 🟥 |
| CMCC-CM2-SR5     | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟨 | 🟨 |
| CMCC-ESM2        | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| CNRM-CM6-1       | r1i1p1f2  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| CNRM-ESM2-1      | r1i1p1f2  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| EC-Earth3-Veg-LR | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| EC-Earth3        | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| FGOALS-g3        | r3i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| GFDL-CM4         | r1i1p1f1  | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 |
| GFDL-CM4_gr2     | r1i1p1f1  | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 |
| GFDL-ESM4        | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| GISS-E2-1-G      | r1i1p1f2  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| HadGEM3-GC31-LL  | r1i1p1f3  | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟥 | 🟥 |
| HadGEM3-GC31-MM  | r1i1p1f3  | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟥 | 🟥 |
| IITM-ESM         | r1i1p1f1  | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 |
| INM-CM4-8        | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟥 | 🟥 |
| INM-CM5-0        | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟥 | 🟥 |
| IPSL-CM6A-LR     | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| KACE-1-0-G       | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| KIOST-ESM        | r1i1p1f1  | 🟩 | 🟥 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| MIROC-ES2L       | r1i1p1f2  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| MIROC6           | r1i1p1f1  | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 |
| MPI-ESM1-2-HR    | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| MPI-ESM1-2-LR    | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| MRI-ESM2-0       | r1i1p1f1  | 🟩 | 🟨 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| NESM3            | r1i1p1f1  | 🟥 | 🟥 | 🟨 | 🟨 | 🟥 | 🟥 | 🟨 | 🟨 | 🟨 |
| NorESM2-LM       | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| NorESM2-MM       | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| TaiESM1          | r1i1p1f1  | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| UKESM1-0-LL      | r1i1p1f2  | 🟥 | 🟥 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 | 🟨 |

## 🛠 Installation

```bash
git clone https://github.com/Magrine/nex-gddp-cmip6-regionalizer
cd nex-gddp-cmip6-regionalizer
```
---

## 🌎 Defining Regions (Bounding Boxes)

Before running the pipeline, users must define the geographic regions that will be cropped and masked in the final NetCDF output.

Regions are specified inside `main.py` using bounding boxes (min/max latitude and longitude):

```python
regions = {
    "alagoas": {
        "min_lon": -39.0, "max_lon": -35.0,
        "min_lat": -11.0, "max_lat": -8.5
    },
    "sao_paulo": {
        "min_lon": -53.5, "max_lon": -44.0,
        "min_lat": -25.5, "max_lat": -19.5
    },
    "matopipa": {
        "min_lon": -50.0, "max_lon": -40.0,
        "min_lat": -15.0, "max_lat": -2.0
    }
}
```

## ▶️ Running the Pipeline

```bash
python main.py
```

---

## 📂 Project Structure

```
nex-gddp-cmip6-regionalizer/
│
├── funcs/
│   ├── crop_and_mask_area.py
│   ├── download_file.py
│   ├── get_extented_coords.py
│   ├── merge_and_save_final.py
│
├── downloads/
│   ├── models/
│   └── temp/
│
├── main.py
├── README.md
└── requirements.txt
```

---

## 📁 Output Example

```
downloads/
 └── models/
      └── ACCESS-CM2/
            └── ssp585/
                  ACCESS-CM2-tas-ssp585.nc
```

## 📜 License

MIT License.  
