#!/usr/bin/env python3
"""
Generate US states location table with bounding boxes.

This script downloads GeoJSON data for US states and converts it to the
locations.csv format, calculating bounding boxes from the state boundaries.

Usage:
    python generate_us_states_polygons.py [--output OUTPUT_FILE]

Options:
    --output FILE         Output CSV file path (default: us_states.csv)
    --max-vertices N      Unused (kept for backward compatibility)
"""

import json
import urllib.request
import argparse


def location_id_from_name(name):
    """Convert state name to location ID."""
    return name.lower().replace(' ', '-')


def process_geojson(output_file, max_vertices=50):
    """
    Download GeoJSON and create CSV with bounding boxes for each state.
    
    Args:
        output_file: Path to output CSV file
        max_vertices: Unused parameter (kept for backward compatibility)
    """
    
    # Download US states GeoJSON
    url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    print(f"Downloading data from {url}...")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return 1
    
    print(f"Processing {len(data['features'])} states/territories...")
    
    # Write CSV header
    with open(output_file, 'w') as f:
        # Write comments explaining the format
        f.write("# US States Location Table\n")
        f.write("# Format: Name,Description,Latmin,Latmax,Lonmin,Lonmax\n")
        f.write("# Longitude: negative for West, positive for East\n")
        f.write("# Latitude: negative for South, positive for North\n")
        f.write("Name,Description,Latmin,Latmax,Lonmin,Lonmax\n")
        
        # Process each state
        for feature in data['features']:
            name = feature['properties']['name']
            location_id = location_id_from_name(name)
            
            # Get coordinates - handle both Polygon and MultiPolygon
            geometry = feature['geometry']
            coordinates = []
            
            if geometry['type'] == 'Polygon':
                # Polygon has one outer ring
                coordinates = geometry['coordinates'][0]
            elif geometry['type'] == 'MultiPolygon':
                # MultiPolygon - use the largest polygon
                largest = max(geometry['coordinates'], key=lambda p: len(p[0]))
                coordinates = largest[0]
            
            # Calculate bounding box from polygon
            lons = [coord[0] for coord in coordinates]
            lats = [coord[1] for coord in coordinates]
            latmin = min(lats)
            latmax = max(lats)
            lonmin = min(lons)
            lonmax = max(lons)
            
            # Write the row: Name (location_id), Description (full name), bounds
            f.write(f"{location_id},{name},{latmin},{latmax},{lonmin},{lonmax}\n")
            
            print(f"  {name}: bounds [{latmin:.2f}, {latmax:.2f}] x [{lonmin:.2f}, {lonmax:.2f}]")
    
    print(f"\nOutput written to: {output_file}")
    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate US states location table with bounding boxes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--output',
        default='us_states.csv',
        help="Output CSV file path (default: us_states.csv)"
    )
    
    parser.add_argument(
        '--max-vertices',
        type=int,
        default=50,
        help="Unused parameter (kept for backward compatibility)"
    )
    
    args = parser.parse_args()
    
    return process_geojson(args.output, args.max_vertices)


if __name__ == '__main__':
    import sys
    sys.exit(main())
