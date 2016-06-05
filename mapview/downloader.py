# coding=utf-8

__all__ = ["Downloader"]

from kivy.network.urlrequest import UrlRequest
from os.path import join, exists
from os import makedirs
from random import choice
from mapview import CACHE

class Downloader(object):
    _instance = None

    @staticmethod
    def instance():
        if Downloader._instance is None:
            Downloader._instance = Downloader()
        return Downloader._instance

    def __init__(self,  *args):
        super(Downloader, self).__init__()

        if not exists(CACHE['directory']):
            makedirs(CACHE['directory'])
    
    def download_tile(self, tile):
        if tile.state == "done":
            return
        cache_fn = tile.cache_fn
        if exists(cache_fn):
            tile.set_source(cache_fn)
        tile_y = tile.map_source.get_row_count(tile.zoom) - tile.tile_y - 1
        uri = tile.map_source.url.format(z=tile.zoom,
                                         x=tile.tile_x,
                                         y=tile_y,
                                         s=choice(tile.map_source.subdomains))

        def success(request, result):
            # print('SUCCESS:', request.file_path)
            tile.set_source(request.file_path)
        def failure(request, result):
            pass
        def error(request, error):
            pass

        req = UrlRequest(uri,
                         on_success=success,
                         on_failure=failure,
                         on_error=error,
                         timeout=5,
                         method='GET',
                         file_path=cache_fn)
        
        #tile.set_source(cache_fn)
