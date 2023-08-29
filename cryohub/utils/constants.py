# note: order in dicts matters (early entries are checked first,
# so better to check new versions first)
class Relion:
    COORD_HEADERS = [f"rlnCoordinate{axis}" for axis in "XYZ"]
    EULER_HEADERS = [f"rlnAngle{angle}" for angle in ["Rot", "Tilt", "Psi"]]
    SHIFT_HEADERS = {
        "4.0": [f"rlnOrigin{axis}Angst" for axis in "XYZ"],
        "3.1": [f"rlnOrigin{axis}Angst" for axis in "XYZ"],
        "3.0": [f"rlnOrigin{axis}" for axis in "XYZ"],
    }
    PIXEL_SIZE_HEADER = {
        "4.0": "rlnTomoTiltSeriesPixelSize",
        "3.1": "rlnImagePixelSize",
        "3.0": "rlnDetectorPixelSize",
    }
    MICROGRAPH_NAME_HEADER = {
        "4.0": "rlnTomoName",
        "3.1": "rlnMicrographName",
        "3.0": "rlnMicrographName",
    }
    OPTICS_GROUP_HEADER = "rlnOpticsGroup"
    POSSIBLE_OPTICS_GROUP_HEADERS = [
        "rlnVoltage",
        "rlnSphericalAberration",
        "rlnAmplitudeContrast",
        "rlnImageSize",
        "rlnImageDimensionality",
        "rlnOpticsGroupName",
        "rlnDetectorPixelSize",
        "rlnImagePixelSize",
        "rlnTomoTiltSeriesPixelSize",
        "rlnMicrographOriginalPixelSize",
        "rlnImageSize",
    ]
    REDUNDANT_HEADERS = (
        COORD_HEADERS
        + EULER_HEADERS
        + SHIFT_HEADERS["3.0"]
        + SHIFT_HEADERS["3.1"]
        + SHIFT_HEADERS["4.0"]
        + [
            PIXEL_SIZE_HEADER["3.0"],
            PIXEL_SIZE_HEADER["3.1"],
            PIXEL_SIZE_HEADER["4.0"],
        ]
    )

    # euler angle definitions are as expected by scipy Rotation objects
    # uppercase is intrinsic, lowercase extrinsic
    EULER = "ZYZ"
    INPLANE = "Z"


class Dynamo:
    COORD_HEADERS = ["x", "y", "z"]
    SHIFT_HEADERS = ["dx", "dy", "dz"]
    EULER_HEADERS = {
        3: ["tdrot", "tilt", "narot"],
        2: ["tilt"],  # TODO: 2d column name might be wrong!
    }
    EXP_ID_HEADER = "tomo"
    EXP_NAME_HEADER = "tomo_file"
    REDUNDANT_HEADERS = COORD_HEADERS + SHIFT_HEADERS + EULER_HEADERS[3]

    EULER = "zxz"
    INPLANE = "z"
