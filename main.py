from funcs.get_extented_coords import get_extented_coords
from funcs.download_file import download_file
from funcs.crop_and_mask_area import crop_and_mask_area
from funcs.merge_and_save_final import merge_and_save_final


import subprocess
import inquirer
import os
import sys

models = [
    {"model": "ACCESS-CM2",       "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "ACCESS-ESM1-5",    "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "BCC-CSM2-MR",      "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "CanESM5",          "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "CESM2-WACCM",      "variant": "r4i1p1f1",  "grid": "gn"},
    {"model": "CESM2",            "variant": "r3i1p1f1",  "grid": "gn"},
    {"model": "CMCC-CM2-SR5",     "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "CMCC-ESM2",        "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "CNRM-CM6-1",       "variant": "r1i1p1f2",  "grid": "gr"},
    {"model": "CNRM-ESM2-1",      "variant": "r1i1p1f2",  "grid": "gr"},
    {"model": "EC-Earth3-Veg-LR", "variant": "r1i1p1f1",  "grid": "gr"},
    {"model": "EC-Earth3",        "variant": "r1i1p1f1",  "grid": "gr"},
    {"model": "FGOALS-g3",        "variant": "r3i1p1f1",  "grid": "gn"},
    {"model": "GFDL-CM4",         "variant": "r1i1p1f1",  "grid": "gr1"},
    {"model": "GFDL-CM4_gr2",     "variant": "r1i1p1f1",  "grid": "gr2"},
    {"model": "GFDL-ESM4",        "variant": "r1i1p1f1",  "grid": "gr1"},
    {"model": "GISS-E2-1-G",      "variant": "r1i1p1f2",  "grid": "gn"},
    {"model": "HadGEM3-GC31-LL",  "variant": "r1i1p1f3",  "grid": "gn"},
    {"model": "HadGEM3-GC31-MM",  "variant": "r1i1p1f3",  "grid": "gn"},
    {"model": "IITM-ESM",         "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "INM-CM4-8",        "variant": "r1i1p1f1",  "grid": "gr1"},
    {"model": "INM-CM5-0",        "variant": "r1i1p1f1",  "grid": "gr1"},
    {"model": "IPSL-CM6A-LR",     "variant": "r1i1p1f1",  "grid": "gr"},
    {"model": "KACE-1-0-G",       "variant": "r1i1p1f1",  "grid": "gr"},
    {"model": "KIOST-ESM",        "variant": "r1i1p1f1",  "grid": "gr1"},
    {"model": "MIROC-ES2L",       "variant": "r1i1p1f2",  "grid": "gn"},
    {"model": "MIROC6",           "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "MPI-ESM1-2-HR",    "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "MPI-ESM1-2-LR",    "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "MRI-ESM2-0",       "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "NESM3",            "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "NorESM2-LM",       "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "NorESM2-MM",       "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "TaiESM1",          "variant": "r1i1p1f1",  "grid": "gn"},
    {"model": "UKESM1-0-LL",      "variant": "r1i1p1f2",  "grid": "gn"}
]

experiments = [
    {"value": "historical", "name": "Historical"},
    {"value": "ssp126",     "name": "SSP1-2.6"},
    {"value": "ssp245",     "name": "SSP2-4.5"},
    {"value": "ssp370",     "name": "SSP3-7.0"},
    {"value": "ssp585",     "name": "SSP5-8.5"},
]

variables = [
    {"value": "hurs",    "name": "Relative air humidity"},
    {"value": "huss",    "name": "Specific humidity"},
    {"value": "pr",      "name": "Precipitation"},
    {"value": "rlds",    "name": "Downward longwave radiation"},
    {"value": "rsds",    "name": "Downward shortwave radiation"},
    {"value": "sfcWind", "name": "10m wind speed"},
    {"value": "tas",     "name": "Mean air temperature"},
    {"value": "tasmax",  "name": "Maximum air temperature"},
    {"value": "tasmin",  "name": "Minimum air temperature"},
]

years_historical = None
years_ssp = None

base_dir = "downloads"
temp_dir = os.path.join(base_dir, "temp")
base_url = "https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/NEX-GDDP-CMIP6"

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

var_label_by_value = {v["value"]: v["name"] for v in variables}

# ========= 0) Install dependencies (requirements.txt) ==========

def install_requirements():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

    if not os.path.exists(req_path):
        print("requirements.txt not found. Continuing without installing dependencies.")
        return

    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
        print("Dependencies installed.\n")
    except Exception as e:
        print("Error installing dependencies:", e)
        sys.exit(1)

install_requirements()

# ================== 1) Select multiple models ==================
model_question = [
    inquirer.List(
        "models",
        message="Select a model:",
        choices=[v["model"] for v in models]
    )
]
answers_models = inquirer.prompt(model_question)
models_selected = answers_models["models"]

# ================== 2) Select multiple experiments =============
exp_question = [
    inquirer.Checkbox(
        "experiments",
        message="Select one or more experiments:",
        choices=[(v["name"], v["value"]) for v in experiments],
    )
]
answers_exp = inquirer.prompt(exp_question)
experiments_selected = answers_exp["experiments"]

# ================== 3) Select multiple variables =================
var_question = [
    inquirer.Checkbox(
        "variables",
        message="Select one or more variables:",
        choices=[(v["name"], v["value"]) for v in variables],
    )
]
answers_var = inquirer.prompt(var_question)
variables_selected = answers_var["variables"]

# ================== 4) Define historical and SSP intervals ==================
def validate_year(answer: str) -> bool:
    return answer.isdigit() and len(answer) == 4

def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))

def ask_year_interval(label, min_year, max_year):
    start_question = [
        inquirer.Text(
            "start_year",
            message=f"[{label}] Enter the start year ({min_year}–{max_year}) ",
            validate=lambda _, x: (
                validate_year(x) or "Enter a 4-digit year."
            ),
        )
    ]
    start_raw = int(inquirer.prompt(start_question)["start_year"])
    start_year = clamp(start_raw, min_year, max_year)

    end_question = [
        inquirer.Text(
            "end_year",
            message=f"[{label}] Enter the end year ({start_year}–{max_year}) ",
            validate=lambda _, x: (
                validate_year(x) or "Enter a 4-digit year."
            ),
        )
    ]
    end_raw = int(inquirer.prompt(end_question)["end_year"])
    end_year = clamp(end_raw, start_year, max_year)

    return start_year, end_year


# ------------------ Historical interval adjustment ------------------
if "historical" in experiments_selected:
    min_h, max_h = 1950, 2014
    start_h, end_h = ask_year_interval("Historical", min_h, max_h)
    years_historical = range(start_h, end_h + 1)

# ------------------ SSPs interval adjustment ------------------
ssp_selected = [e for e in experiments_selected if e != "historical"]
if ssp_selected:
    min_s, max_s = 2030, 2100
    start_s, end_s = ask_year_interval("SSP scenarios", min_s, max_s)
    years_ssp = range(start_s, end_s + 1)

# ================== 5) Total calculation and summary ==================

# Compute exact total number of files considering the selected years
count_years_total = 0
for exp in experiments_selected:
    if exp == "historical":
        count_years_total += len(years_historical)
    else:
        count_years_total += len(years_ssp)

total_files = len(models_selected) * len(variables_selected) * count_years_total

print("\nSelection summary:")
print("------------------")
print(f"Selected model: {(models_selected)}")

print(f"\nSelected scenarios ({len(experiments_selected)}):")

for e in experiments_selected:
    print(f"  - {e}")

print(f"\nSelected variables ({len(variables_selected)}):")

for v in variables_selected:
    label = var_label_by_value.get(v, v)
    print(f"  - {v} ({label})")

print("\nDefined periods:")
if years_historical is not None:
    print("  - Historical period:", years_historical.start, "→", years_historical.stop - 1)
else:
    print("  - Historical period: not selected")
if years_ssp is not None:
    print("  - SSPs period:", years_ssp.start, "→", years_ssp.stop - 1)
else:
    print("  - SSPs period: not selected")

print("\nTotal model files to be downloaded:")
print(f"  -> { len(variables_selected) * len(experiments_selected) * count_years_total}\n")

# ================== 6) Confirm and run ==================

confirm_question = [
    inquirer.List(
        "confirm",
        message="Do you want to proceed with the download?",
        choices=["Yes", "No"],
    )
]
if inquirer.prompt(confirm_question)["confirm"] == "No":
    print("Cancelled.")
    exit(0)

print("Starting process...\n")

combined_extent = get_extented_coords(regions)

# Create temporary folder if it does not exist
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

model_variant = [m["variant"] for m in models if m["model"] in models_selected][0]

model_grid = [m["grid"] for m in models if m["model"] in models_selected][0]

for scenario in experiments_selected:
    for variable in variables_selected:
        
        print(f"\n==================================================")
        print(f"PROCESSING: {models_selected} | {variable} | {scenario}")
        print(f"==================================================")
        
        # Define which year list to use
        current_years = years_historical if scenario == "historical" else years_ssp
        
        counter = 0
        for year in current_years:
            counter += 1
            
            global_filename = f"{variable}_day_{models_selected}_{scenario}_{model_variant}_{model_grid}_{year}.nc"
            crop_filename = f"MASKED_{global_filename}"
            
            global_path = os.path.join(temp_dir, global_filename)
            crop_path = os.path.join(temp_dir, crop_filename)
            
            # Build correct URL
            url = f"{base_url}/{models_selected}/{scenario}/{model_variant}/{variable}/{global_filename}"

            if os.path.exists(crop_path):
                print(
                    f"Progress ({counter}/{len(years_historical if scenario == 'historical' else years_ssp)}): "
                    f"Year {year} already processed. Skipping."
                )
                continue

            # 1. Download
            if download_file(
                url,
                global_path,
                counter,
                len(years_historical if scenario == "historical" else years_ssp)
            ):
                # 2. Mask (updates the same line)
                sys.stdout.write(
                    f"\rProgress ({counter}/{len(years_historical if scenario == 'historical' else years_ssp)}): "
                    f"[{'='*50}] 100%  (2/3 Masking)"
                )
                sys.stdout.flush()

                try:
                    crop_and_mask_area(global_path, crop_path, combined_extent, regions)
                except Exception as e:
                    print(f"\nError while cropping the file: {e}")
                    continue

                # 3. Clean up (updates the same line)
                sys.stdout.write(
                    f"\rProgress ({counter}/{len(years_historical if scenario == 'historical' else years_ssp)}): "
                    f"[{'='*50}] 100%  (3/3 Cleaning)"
                )
                sys.stdout.flush()
                
                # Remove the large file
                if os.path.exists(global_path):
                    os.remove(global_path)
                
                # New line for the next file
                print("") 
            
            else:
                print(f"\nDownload failed for year {year}. URL: {url}")

        # After finishing all years for this scenario/variable, merge them
        merge_and_save_final(models_selected, scenario, variable, temp_dir, base_dir, model_grid)
