import os

import geopandas
from PIL import Image
from osgeo import gdal, ogr
import numpy as np
from osgeo.ogr import Layer
from osgeo.osr import SpatialReference


class ShapeFileRepository:
    """
    To access the shapefile open the following: .dbf, .shp, .shx

    https://gdal.org/tutorials/vector_python_driver.html
    https://pcjericks.github.io/py-gdalogr-cookbook/gdal_general.html
    """

    def __init__(self, file: str):
        gdal.UseExceptions()
        self.file = file
        self.file_name = os.path.splitext(os.path.basename(file))[0]
        self.file_path = os.path.dirname(os.path.abspath(file))
        self.driver_name = 'ESRI Shapefile'
        self.width = 512
        self.height = 512

    def read(self):
        """
        Read the shape path and get some points.

        :return: the shape path points.
        """
        driver = ogr.GetDriverByName(self.driver_name)
        data_source = driver.Open(self.file)  # type: ogr.Driver

        layer = data_source.GetLayer()  # type: ogr.Layer

        features = []
        for feature in layer:  # type: ogr.Feature
            geom = feature.GetGeometryRef()  # type: ogr.Geometry
            g = geom.GetGeometryRef(0)  # type: ogr.Geometry
            pts = g.GetPoints()
            if pts is not None:
                points = []
                for point in pts:
                    points.append([point[0], point[1]])
                features.append(np.array(points))

        layer.ResetReading()
        return features

    def file_w_ext(self, ext):
        return os.path.join(self.file_path, self.file_name + '.' + ext)

    def write_tiff(self):
        # https://stackoverflow.com/questions/59821554/converting-vector-shp-to-raster-tiff-using-python-gdal-library
        # making the shapefile as an object.
        input_shp = ogr.Open(self.file)

        # getting layer information of shapefile.
        shp_layer = input_shp.GetLayer()  # type: Layer

        # get extent values to set size of output raster.
        x_min, x_max, y_min, y_max = shp_layer.GetExtent()

        # calculate size/resolution of the raster.
        pixel_size_x = float((x_max - x_min) / self.height)
        pixel_size_y = float((y_max - y_min) / self.width)

        # get GeoTiff driver by
        image_type = 'GTiff'
        driver = gdal.GetDriverByName(image_type)

        # passing the filename, x and y direction resolution, no. of bands, new raster.
        new_raster = driver.Create(self.file_w_ext('tiff'), self.width, self.height, 1, gdal.GDT_Byte)

        # transforms between pixel raster space to projection coordinate space.
        new_raster.SetGeoTransform((x_min, pixel_size_x, 0, y_min, 0, pixel_size_y))

        # get required raster band.
        band = new_raster.GetRasterBand(1)

        # assign no data value to empty cells.
        no_data_value = -9999
        band.SetNoDataValue(no_data_value)
        band.FlushCache()

        # main conversion method
        gdal.RasterizeLayer(new_raster, [1], shp_layer, burn_values=[255])

        # adding a spatial reference
        new_raster_sr = SpatialReference()
        new_raster_sr.ImportFromEPSG(2975)
        new_raster.SetProjection(new_raster_sr.ExportToWkt())

        return new_raster

    def write_png(self):
        raster = self.write_tiff()
        driver = gdal.GetDriverByName("PNG")
        save_options = ["QUALITY=100"]
        driver.CreateCopy(self.file_w_ext('png'), raster, 0, save_options)
        self.change_color_png('png')

    def write_jpg(self):
        raster = self.write_tiff()
        driver = gdal.GetDriverByName("JPEG")
        save_options = ["QUALITY=100"]
        driver.CreateCopy(self.file_w_ext('jpg'), raster, 0, save_options)
        self.change_color_png('jpg')

    def write_geojson(self):
        shp_file = geopandas.read_file(self.file)
        shp_file.to_file(self.file_w_ext('geojson'), driver='GeoJSON')

    def change_color_png(self, ext):
        """
        Invert the colors and change them a bit.
        """
        image = Image.open(self.file_w_ext(ext))
        image_data = image.load()
        height, width = image.size
        for loop1 in range(height):
            for loop2 in range(width):
                color = image_data[loop1, loop2]
                if color == 0:
                    image_data[loop1, loop2] = 200
                else:
                    image_data[loop1, loop2] = 100

        image.save(self.file_w_ext(ext))
