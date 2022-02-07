# euler angle definitions are as expected by scipy Rotation objects
# uppercase is intrinsic, lowercase extrinsic

class Naaf:
    COORD_HEADERS = ['x', 'y', 'z']
    ROT_HEADER = 'rot'
    ALL_HEADER = COORD_HEADERS + [ROT_HEADER]

class Relion:
    COORD_HEADERS = [f'rlnCoordinate{axis}' for axis in 'XYZ']
    EULER_HEADERS = {
        3: [f'rlnAngle{angle}' for angle in ('Rot', 'Tilt', 'Psi')],
        2: ['rlnAnglePsi']
    }
    SHIFT_HEADERS = {
        '3.0': [f'rlnOrigin{axis}' for axis in 'XYZ'],
        '3.1': [f'rlnOrigin{axis}Angst' for axis in 'XYZ']
    }
    PIXEL_SIZE_HEADERS = {
        '3.0': ['rlnDetectorPixelSize'],
        '3.1': ['rlnImagePixelSize']
    }
    MICROGRAPH_NAME_HEADER = 'rlnMicrographName'
    OPTICS_GROUP_HEADER = 'rlnOpticsGroup'
    ALL_HEADERS = (
        COORD_HEADERS +
        EULER_HEADERS[3] +
        SHIFT_HEADERS['3.0'] +
        SHIFT_HEADERS['3.1'] +
        PIXEL_SIZE_HEADERS['3.0'] +
        PIXEL_SIZE_HEADERS['3.1'] +
        [MICROGRAPH_NAME_HEADER] +
        [OPTICS_GROUP_HEADER]
    )

    EULER = 'ZYZ'
    INPLANE = 'Z'

class Dynamo:
    COORD_HEADERS = ['x', 'y', 'z']
    SHIFT_HEADERS = ['dx', 'dy', 'dz']
    EULER_HEADERS = {
        3: ['tdrot', 'tilt', 'narot'],
        2: ['tilt']  # TODO: 2d column name might be wrong!
    }
    ALL_HEADERS = COORD_HEADERS + SHIFT_HEADERS + EULER_HEADERS[3]

    EULER = 'zxz'
    INPLANE = 'z'
