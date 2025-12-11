import xarray as xr
import os

def crop_and_mask_area(global_path, crop_path, extent, regions):
    try:        
        with xr.open_dataset(global_path) as ds:
            # Longitude adjustment
            ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180)).sortby('lon')

            # 1. Full Bounding Box Crop
            ds_subset = ds.sel(
                lon=slice(extent["min_lon"], extent["max_lon"]),
                lat=slice(extent["min_lat"], extent["max_lat"])
            )
            ds_subset.load()

            # 2. Mask
            mask = xr.full_like(ds_subset['lat'], False, dtype=bool) * xr.full_like(ds_subset['lon'], False, dtype=bool)
            final_mask = mask.copy()
            
            for region in regions.values():
                region_mask = (ds_subset.lon >= region["min_lon"]) & \
                              (ds_subset.lon <= region["max_lon"]) & \
                              (ds_subset.lat >= region["min_lat"]) & \
                              (ds_subset.lat <= region["max_lat"])
                final_mask = final_mask | region_mask

            ds_masked = ds_subset.where(final_mask)

        # Saves the masked dataset in the TEMP folder
        comp = dict(zlib=True, complevel=5)
        encoding = {var: comp for var in ds_masked.data_vars}
        ds_masked.to_netcdf(crop_path, encoding=encoding)
        ds_masked.close()

        # Deletes the global file from the TEMP folder
        if os.path.exists(global_path):
            os.remove(global_path)        
        return True

    except Exception as e:
        print(f"   Error during masking: {e}")
        return False
