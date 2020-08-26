from osgeo import gdal, ogr
import numpy as np


class ShapeFileRepository:
    """
    To access the shapefile open the following: .dbf, .shp, .shx

    https://gdal.org/tutorials/vector_python_driver.html
    https://pcjericks.github.io/py-gdalogr-cookbook/gdal_general.html
    """

    def __init__(self, path: str):
        gdal.UseExceptions()
        self.path = path
        self.driver_name = 'ESRI Shapefile'

    def read(self):
        """
        Read the shape path and get some points.

        :return: the shape path points.
        """
        driver = ogr.GetDriverByName(self.driver_name)
        data_source = driver.Open(self.path, 0)  # type: ogr.Driver

        layer = data_source[0]  # type: ogr.Layer

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
