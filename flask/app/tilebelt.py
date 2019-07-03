# Porting the parts of the tilebelt Utility from https:#github.com/mapbox/tilebelt to Python
# https://github.com/buckhx/QuadKey/blob/master/quadkey/tile_system.py <-- With code from here too :)
import numpy as np
d2r = np.pi / 180,
r2d = 180 / np.pi


def tile_to_point(tile):
    bbox = tile_to_bbox([tile[0]+.5, tile[1]+.5, tile[2]])
    return {'type': 'Point',
            'coordinates': [
                bbox[0],
                bbox[3]
            ]
            }


def tile_to_bbox(tile):
    e = tile2lon(tile[0] + 1, tile[2])
    w = tile2lon(tile[0], tile[2])
    s = tile2lat(tile[1] + 1, tile[2])
    n = tile2lat(tile[1], tile[2])
    return [w, s, e, n]


def tile_to_geojson(tile):
    bbox = tile_to_bbox(tile)
    poly = {
        'type': 'Polygon',
        'coordinates': [[
            [bbox[0], bbox[1]],
            [bbox[0], bbox[3]],
            [bbox[2], bbox[3]],
            [bbox[2], bbox[1]],
            [bbox[0], bbox[1]]
        ]]}
    return poly


def tile2lon(x, z):
    return x / np.power(2, z) * 360 - 180


def tile2lat(y, z):
    n = np.pi - 2 * np.pi * y / np.power(2, z)
    return r2d * np.arctan(0.5 * (np.exp(n) - np.exp(-n)))


def tile_to_quadkey(tile, level):
    tile_x = tile[0]
    tile_y = tile[1]
    quadkey = ""
    for i in range(level):
        bit = level - i
        digit = ord('0')
        mask = 1 << (bit - 1)  # if (bit - 1) > 0 else 1 >> (bit - 1)
        if (tile_x & mask) is not 0:
            digit += 1
        if (tile_y & mask) is not 0:
            digit += 2
        quadkey += chr(digit)
    return quadkey


def quadkey_to_tile(quadkey):
    """Transform quadkey to tile coordinates"""
    tile_x, tile_y = (0, 0)
    level = len(quadkey)
    for i in range(level):
        bit = level - i
        mask = 1 << (bit - 1)
        if quadkey[level - bit] == '1':
            tile_x |= mask
        if quadkey[level - bit] == '2':
            tile_y |= mask
        if quadkey[level - bit] == '3':
            tile_x |= mask
            tile_y |= mask
    return [tile_x, tile_y, level]
