#!/usr/bin/env python

from __future__ import division
import numpy as np
import matplotlib
# avoid import errors on macOS
matplotlib.use("AGG")  # noqa
import matplotlib.pyplot as plt
import sys

import descarteslabs.scenes as scn

aoi_geometry = {
    'type': 'Polygon',
    'coordinates': ((
        (-93.52300099792355, 41.241436141055345),
        (-93.7138666, 40.703737),
        (-94.37053769704536, 40.83098709945576),
        (-94.2036617, 41.3717716),
        (-93.52300099792355, 41.241436141055345)
    ),)
}

# Search for Scenes within it:

scenes = scn.search(aoi_geometry,
                    products=["landsat:LC08:PRE:TOAR"],
                    start_datetime="2013-07-01",
                    end_datetime="2013-09-01",
                    limit=10)
# scenes
# SceneCollection of 10 scenes
#   * Dates: Jul 07, 2013 to Aug 24, 2013
#   * Products: landsat:LC08:PRE:TOAR: 10
#   * ctx: AOI with resolution 60, bounds (-94.37053769704536, 40.703737, -93.52300099792355, 41.3717716)
#
# Quickly inspect metadata:
#
# scenes.each.properties.id
# 'landsat:LC08:PRE:TOAR:meta_LC80260312013188_v1'
# 'landsat:LC08:PRE:TOAR:meta_LC80260312013204_v1'
# 'landsat:LC08:PRE:TOAR:meta_LC80260312013220_v1'
# 'landsat:LC08:PRE:TOAR:meta_LC80260312013236_v1'
# 'landsat:LC08:PRE:TOAR:meta_LC80260322013188_v1'
# 'landsat:LC08:PRE:TOAR:meta_LC80260322013204_v1'
# 'landsat:LC08:PRE:TOAR:meta_LC80260322013220_v1'
# 'landsat:LC08:PRE:TOAR:meta_LC80260322013236_v1'
# ...
# scenes.each.properties.date.month
# 7
# 7
# 7
# 7
# 7
# 7
# 8
# 8
# ...
#
# Load and display a scene:
#
# scene = scenes[-2]
# arr = scene.ndarray(scenes.ctx, "red green blue")
# scn.display(arr)
#
# .. image:: https://cdn.descarteslabs.com/docs/api/scenes/init-1.png
#
# Monthly median composites of NDVI within our area of interest:

monthly_composites = {}
for month, month_scenes in scenes.groupby("properties.date.month"):
    stack = month_scenes.stack("red nir")
    red, nir = stack[:, 0], stack[:, 1]
    ndvi = (nir - red) / (nir + red)
    ndvi_composite = np.ma.median(ndvi, axis=0)
    monthly_composites[month] = ndvi_composite

# And the mean NDVI value of each month's composite is:
#
# {month: composite.mean() for month, composite in monthly_composites.items()}
# {7: 0.32535368527404873, 8: 0.41194597940346561}
#
# View the NDVI composites:

scn.display(*monthly_composites.values(), title=list(monthly_composites.keys()))

# .. image:: https://cdn.descarteslabs.com/docs/api/scenes/init-2.png

###


plt.savefig(sys.argv[1])
