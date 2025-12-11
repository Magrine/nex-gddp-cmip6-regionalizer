import os
import glob
import xarray as xr

def merge_and_save_final(model, scenario, variable, temp_dir, base_dir, grade):
    print(f"\n--- Saving final file ---")
    
    # Search for files in TEMP folder
    search_pattern = os.path.join(temp_dir, f"MASKED_{variable}_day_{model}_{scenario}_*_{grade}_*.nc")
    files_to_merge = sorted(glob.glob(search_pattern))
    
    if not files_to_merge:
        print("No processed files found in Temp.")
        return

    try:
        # 1. Merge datasets
        ds = xr.open_mfdataset(files_to_merge, combine='by_coords')
        
        # 2. Prepare final directory: downloads/{model}/{scenario}
        final_dir = os.path.join(f"{base_dir}/models", model, scenario)
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)
            
        final_filename = f"{model}-{variable}-{scenario}.nc"
        final_path = os.path.join(final_dir, final_filename)
        
        #print(f"   Saving to: {final_path}")
        
        comp = dict(zlib=True, complevel=5)
        encoding = {var: comp for var in ds.data_vars}
        ds.to_netcdf(final_path, encoding=encoding)
        ds.close()
        
        # 4. Cleanup TEMP folder (delete annual masked files)
        #print("   Cleaning temporary folder...")
        for f in files_to_merge:
            try:
                os.remove(f)
            except:
                pass

        print("Done.")
            
    except Exception as e:
        print(f"Error while saving final file: {e}")
