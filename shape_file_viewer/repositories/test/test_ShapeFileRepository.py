import unittest

from shape_file_viewer.repositories.ShapeFileRepository import ShapeFileRepository


class TestShapeFileRepository(unittest.TestCase):

    file = '../../../sample/shape_files/test.shp'

    def test_read(self):
        repo = ShapeFileRepository(file=self.file)
        points = repo.read()
        print(points)

    def test_write_tiff(self):
        """
        Ref: https://stackoverflow.com/questions/59821554/converting-vector-shp-to-raster-tiff-using-python-gdal-library
        """
        repo = ShapeFileRepository(file=self.file)
        repo.write_tiff()

    def test_write_png(self):
        repo = ShapeFileRepository(file=self.file)
        repo.write_png()

    def test_write_jpg(self):
        repo = ShapeFileRepository(file=self.file)
        repo.write_jpg()

    def test_write_geojson(self):
        repo = ShapeFileRepository(file=self.file)
        repo.write_geojson()
