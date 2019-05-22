from ..._volume_data import _VolumeData
from nanome.util import Logs
import os
import gzip
import struct

float_unpack = struct.Struct('!f').unpack_from
int_unpack = struct.Struct('!i').unpack_from

def parse_file(path):
    try:
        data = []
        if (os.path.splitext(path)[1] == ".gz"):
            with gzip.open(path, mode='rb') as f:
                data = f.read()
        else:
            with open(path, mode='rb') as f:
                data = f.read()
        if data == []:
            raise ValueError("File is empty.")
        result = parse_data(data)
        return result
    except:
        Logs.error("Could not read em file: " + path)
        raise

def read_buffer(bytes_):
    header_size = 1024 #size in bytes
    header = struct.unpack(str(256)+"i", bytes_[:header_size])
    unit_cell = struct.unpack(str(6)+"f", bytes_[40:64])
    symmetry_size = header[23] #size in bytes
    symmetry = bytes_[header_size:header_size + symmetry_size]
    body_length = int((len(bytes_)-(header_size+symmetry_size))/4) #length in floats
    body = struct.unpack(str(body_length) + "f", bytes_[header_size+symmetry_size:])
    return header, unit_cell, symmetry, body

def parse_data(bytes):
    results = read_buffer(bytes)
    header, unit_cell, symmetry_size, body = results
    if (header[52] != 0x2050414d):
        if (header[52] == 0x4d415020):
            raise Exception("CryoEM> File is encoded on a big-endian machine")
        raise Exception("CryoEM> File doesn't have proper header")
    n_columns = header[0]
    n_rows = header[1]
    n_section = header[2]
    mode = header[3]
    data_size_byte = 0
    if (mode == 2):
        data_size_byte = 4
    else:
        raise Exception("CryoEM> Only mode 2 is supported")
    
    start_x = header[4]
    start_y = header[5]
    start_z = header[6]
    
    if (unit_cell[3] != 90 or unit_cell[4] != 90 or unit_cell[5] != 90):
        raise ("CryoEM> Cell is not perpendicular. Is this an Electron Density Map?")

    delta_x = unit_cell[0] / header[7]
    delta_y = unit_cell[1] / header[8]
    delta_z = unit_cell[2] / header[9]
    map = _VolumeData(n_columns, n_rows, n_section, delta_x, delta_y, delta_z)
    if (header[16] != 1 or header[17] != 2 or header[18] != 3):
        raise Exception("CryoEM> data layout doesn't meet Cryo-EM standard. Is this an Electron Density Map?")
    symmetrySizeByte = header[23]
    if (symmetrySizeByte != 0):
        raise Exception("CryoEM> contains symmetry operation.")
    map._data = body

    return map