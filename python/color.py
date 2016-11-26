def to_rgb(hex):
    return (
        hex >> 16 & 0xFF,
        hex >> 8 & 0xFF,
        hex & 0xFF
    )


def to_hex(rgb):
    return rgb[0] << 16 | rgb[1] << 8 | rgb[2]


def adjust_brightness(hex, by=1):
    return to_hex(map(lambda c: int(c * by), to_rgb(hex)))
