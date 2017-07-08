FROM geodata/gdal

WORKDIR /data

RUN apt-get update &\
    apt-get install -y python-scipy

# https://mapbox.github.io/rasterio/topics/migrating-to-v1.html#deprecated-rasterio-drivers
RUN pip install rasterio==0.34.0
RUN pip install makesurface

VOLUME ["/data"]

