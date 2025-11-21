# US States Polygon Tools

This directory contains tools for generating and visualizing US state boundary polygons.

## Scripts

### generate_us_states_polygons.py

Generate or regenerate the `us_states.csv` file with actual state boundary polygons from online GeoJSON data.

**Usage:**
```bash
# Generate with default settings (50 vertices max per state)
python generate_us_states_polygons.py

# Customize output file and vertex count
python generate_us_states_polygons.py --output custom_states.csv --max-vertices 40
```

**Options:**
- `--output FILE`: Output CSV file path (default: `us_states.csv`)
- `--max-vertices N`: Maximum vertices per polygon (default: 50)

**Data Source:**
Downloads GeoJSON data from [PublicaMundi/MappingAPI](https://github.com/PublicaMundi/MappingAPI)

### plot_us_states.py

Plot state polygons on a map with coastal lines using various map projections.

**Requirements:**
```bash
pip install matplotlib cartopy
```

**Note:** This script requires cartopy which downloads Natural Earth data for coastlines. If you don't have internet access or want a simpler alternative, use `plot_us_states_simple.py` instead.

**Usage:**
```bash
# Plot all states on default projection
python plot_us_states.py

# Plot specific states
python plot_us_states.py --states california texas florida

# Use different projection
python plot_us_states.py --projection LambertConformal

# Save to file instead of displaying
python plot_us_states.py --output us_states_map.png --states california

# Plot without state name labels
python plot_us_states.py --no-labels
```

**Options:**
- `--locations-file FILE`: Path to CSV file with state polygons (default: `us_states.csv`)
- `--states STATE [STATE ...]`: Specific states to plot (e.g., `california texas`)
- `--projection NAME`: Map projection to use (default: `PlateCarree`)
- `--output FILE`: Save figure to file instead of displaying
- `--no-labels`: Don't show state name labels
- `--figsize WIDTH HEIGHT`: Figure size in inches (default: 15 10)

**Available Projections:**
- `PlateCarree`: Simple lat-lon projection (default)
- `LambertConformal`: Lambert conformal conic
- `Mercator`: Mercator projection
- `Orthographic`: Orthographic (globe) projection
- `Robinson`: Robinson projection
- `AlbersEqualArea`: Albers equal-area conic

### plot_us_states_simple.py

Plot state polygons using simple matplotlib without map projections (no internet required).

**Requirements:**
```bash
pip install matplotlib
```

**Usage:**
```bash
# Plot all states
python plot_us_states_simple.py

# Plot specific states
python plot_us_states_simple.py --states california texas florida

# Save to file
python plot_us_states_simple.py --output us_states_map.png
```

**Options:**
- `--locations-file FILE`: Path to CSV file with state polygons (default: `us_states.csv`)
- `--states STATE [STATE ...]`: Specific states to plot
- `--output FILE`: Save figure to file instead of displaying
- `--no-labels`: Don't show state name labels
- `--figsize WIDTH HEIGHT`: Figure size in inches (default: 15 10)

## Examples

### Generate state polygons with 40 vertices maximum
```bash
python generate_us_states_polygons.py --max-vertices 40
```

### Plot California on a Lambert Conformal projection (requires cartopy)
```bash
python plot_us_states.py --states california --projection LambertConformal --output california.png
```

### Plot West Coast states (simple version, no cartopy needed)
```bash
python plot_us_states_simple.py --states california oregon washington --output west_coast.png
```

### Plot all states and save high-res image
```bash
python plot_us_states_simple.py --output all_states.png
```

### Plot Texas, Florida, and California
```bash
python plot_us_states_simple.py --states texas florida california --output three_states.png
```

## File Format

The generated `us_states.csv` file follows this format:

```
Name,Description,Latmin,Latmax,Lonmin,Lonmax
california,California,32.53,42.01,-124.48,-114.13
```

Where:
- **Name**: State identifier (lowercase with hyphens)
- **Description**: Full state name
- **Latmin**: Minimum latitude of bounding box
- **Latmax**: Maximum latitude of bounding box
- **Lonmin**: Minimum longitude of bounding box
- **Lonmax**: Maximum longitude of bounding box

The existing scripts (`generate_config.py`, `prepare_initial_condition.py`) automatically calculate rectangular simulation bounds and center points from these bounding boxes.

## Notes

- Bounding boxes are calculated from the original state boundary polygons
- Alaska uses extended western longitude (around -189° to -130°) for consistency across the International Date Line
- All longitude/latitude values follow standard conventions:
  - Longitude: negative for West, positive for East
  - Latitude: negative for South, positive for North
