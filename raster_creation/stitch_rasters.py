import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy
import os

target_dir = "rasters/open_past_/pasture_exc_parts"
out_path = "rasters/open_past_/pasture_exc_400752_200376.tif"
dst_crs = 'EPSG:4326'
width, height = 400752, 200376

f = []
for path, subdirs, files in os.walk(target_dir):
    for name in files:
        f.append(os.path.join(path, name))
f = [file for file in f if ".tif" in file and ".aux" not in file]

src_files_to_mosaic = []
for file in f:
    src = rasterio.open(file)
    src_files_to_mosaic.append(src)
mosaic, transform = merge(src_files_to_mosaic)

out_meta = src.meta.copy()
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": transform})

with rasterio.open(out_path, 'w', **out_meta) as dest:
    dest.write(mosaic)

for src in src_files_to_mosaic:
    src.close()