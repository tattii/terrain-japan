FROM geodata/gdal

WORKDIR /data

RUN apt-get update
RUN apt-get install -y python-scipy

# https://mapbox.github.io/rasterio/topics/migrating-to-v1.html#deprecated-rasterio-drivers
RUN pip install makesurface --pre
RUN pip install --upgrade six
RUN pip install rasterio==0.34.0
RUN pip install joblib

VOLUME ["/data"]

