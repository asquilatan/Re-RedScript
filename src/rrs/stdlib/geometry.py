import math

def distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def bresenham_line(start, end):
    """Generates points for a 3D line using Bresenham's algorithm."""
    x1, y1, z1 = start
    x2, y2, z2 = end
    points = []
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    
    xs = 1 if x2 > x1 else -1
    ys = 1 if y2 > y1 else -1
    zs = 1 if z2 > z1 else -1
    
    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x1 != x2:
            points.append((x1, y1, z1))
            x1 += xs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dx
            if p2 >= 0:
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y1 != y2:
            points.append((x1, y1, z1))
            y1 += ys
            if p1 >= 0:
                x1 += xs
                p1 -= 2 * dy
            if p2 >= 0:
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z1 != z2:
            points.append((x1, y1, z1))
            z1 += zs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dz
            if p2 >= 0:
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            
    points.append((x1, y1, z1))
    return points

def bezier_curve(points, segments=20):
    """Calculates points along a cubic Bezier curve."""
    curve_points = []
    n = len(points) - 1
    for t in [i / segments for i in range(segments + 1)]:
        x, y, z = 0, 0, 0
        for i, pos in enumerate(points):
            bernstein = math.factorial(n) / (math.factorial(i) * math.factorial(n - i)) * (t ** i) * ((1 - t) ** (n - i))
            x += pos[0] * bernstein
            y += pos[1] * bernstein
            z += pos[2] * bernstein
        curve_points.append((int(round(x)), int(round(y)), int(round(z))))
    return curve_points

def rasterize_sphere(center, radius, fill=False):
    cx, cy, cz = center
    points = []
    r = int(radius)
    r2 = r**2
    
    # Pre-calculate constants
    inner_limit = (r - 1)**2 - 1 if not fill else -1

    # Optimization: Iterate only within the bounding sphere bounds
    # x goes from -r to r
    for x in range(-r, r + 1):
        x2 = x * x
        # Max y for this x is sqrt(r^2 - x^2)
        y_max = math.isqrt(r2 - x2)

        for y in range(-y_max, y_max + 1):
            y2 = y * y
            d2_xy = x2 + y2

            # Max z for this x, y is sqrt(r^2 - x^2 - y^2)
            z_max = math.isqrt(r2 - d2_xy)

            if fill or inner_limit < 0 or d2_xy > inner_limit:
                # Fill mode OR point is already "outside" the inner hole in XY plane
                # (so all valid z will be part of the shell)
                # OR hole is empty
                for z in range(-z_max, z_max + 1):
                    points.append((cx + x, cy + y, cz + z))
            else:
                # Hollow mode and we might overlap with the hole
                # We need to skip z values where x^2 + y^2 + z^2 <= (r-1)^2 - 1
                # i.e., z^2 <= inner_limit - d2_xy
                rem = inner_limit - d2_xy
                z_skip = math.isqrt(rem)

                # We keep points in [-z_max, -z_skip - 1] and [z_skip + 1, z_max]
                # Python range stop is exclusive, so range(a, b) goes up to b-1.
                # Lower part: -z_max to -z_skip-1 inclusive -> range(-z_max, -z_skip)
                for z in range(-z_max, -z_skip):
                    points.append((cx + x, cy + y, cz + z))

                # Upper part: z_skip+1 to z_max inclusive -> range(z_skip + 1, z_max + 1)
                for z in range(z_skip + 1, z_max + 1):
                    points.append((cx + x, cy + y, cz + z))

    return points

def rasterize_cylinder(base, radius, height, axis='y', fill=False):
    bx, by, bz = base
    points = set()
    r = int(radius)
    h = int(height)
    
    # Simple axis alignment
    if axis == 'y':
        for y in range(by, by + h):
            for x in range(bx - r, bx + r + 1):
                for z in range(bz - r, bz + r + 1):
                    dist_sq = (x - bx)**2 + (z - bz)**2
                    if dist_sq <= r**2:
                        if fill or dist_sq >= (r-1)**2 or y == by or y == by + h - 1:
                             points.add((x, y, z))
    elif axis == 'x':
         for x in range(bx, bx + h):
            for y in range(by - r, by + r + 1):
                for z in range(bz - r, bz + r + 1):
                    dist_sq = (y - by)**2 + (z - bz)**2
                    if dist_sq <= r**2:
                        if fill or dist_sq >= (r-1)**2 or x == bx or x == bx + h - 1:
                             points.add((x, y, z))
    elif axis == 'z':
        for z in range(bz, bz + h):
            for x in range(bx - r, bx + r + 1):
                for y in range(by - r, by + r + 1):
                    dist_sq = (x - bx)**2 + (y - by)**2
                    if dist_sq <= r**2:
                        if fill or dist_sq >= (r-1)**2 or z == bz or z == bz + h - 1:
                             points.add((x, y, z))
                             
    return list(points)

def catmull_rom_spline(points, segments=10):
    """Calculates points along a Catmull-Rom spline passing through all points."""
    if len(points) < 2:
        return points
        
    curve_points = []
    
    # Duplicate start/end points to handle boundaries
    # P[0], P[0], P[1], P[2] ... P[N-1], P[N-1]
    extended_points = [points[0]] + points + [points[-1]]
    
    for i in range(len(points) - 1):
        p0 = extended_points[i]
        p1 = extended_points[i+1]
        p2 = extended_points[i+2]
        p3 = extended_points[i+3]
        
        for j in range(segments):
            t = j / segments
            t2 = t * t
            t3 = t2 * t
            
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            z = 0.5 * ((2 * p1[2]) + (-p0[2] + p2[2]) * t + (2 * p0[2] - 5 * p1[2] + 4 * p2[2] - p3[2]) * t2 + (-p0[2] + 3 * p1[2] - 3 * p2[2] + p3[2]) * t3)
            
            curve_points.append((int(round(x)), int(round(y)), int(round(z))))
            
    curve_points.append(points[-1])
    return curve_points
