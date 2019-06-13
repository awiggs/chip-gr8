def default(screen, x, y):
    return screen.foreground

def rainbow(screen, x, y):
    frac = y / screen.height
    if frac < 0.5:
        a = frac * 2
        b = 1 - frac
        return (255 * b, 255 * a, 0)
    else:
        a = (frac - 0.5) * 2
        b = 1 - frac
        return (0, 255 * b, 255 * a)