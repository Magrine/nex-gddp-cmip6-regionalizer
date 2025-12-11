def get_extented_coords(regions):
    min_lons = [r['min_lon'] for r in regions.values()]
    max_lons = [r['max_lon'] for r in regions.values()]
    min_lats = [r['min_lat'] for r in regions.values()]
    max_lats = [r['max_lat'] for r in regions.values()]

    return {
        "min_lon": min(min_lons), "max_lon": max(max_lons),
        "min_lat": min(min_lats), "max_lat": max(max_lats)
    }