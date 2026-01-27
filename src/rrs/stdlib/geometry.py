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
    points = set()
    r = int(radius)
    
    for x in range(cx - r, cx + r + 1):
        for y in range(cy - r, cy + r + 1):
            for z in range(cz - r, cz + r + 1):
                dist_sq = (x - cx)**2 + (y - cy)**2 + (z - cz)**2
                if dist_sq <= r**2:
                    if fill:
                        points.add((x, y, z))
                    elif dist_sq >= (r - 1)**2: # Shell
                        points.add((x, y, z))
    return list(points)

def rasterize_cylinder(base, radius, height, axis='y', fill=False):
    bx, by, bz = base
    points = []
    r = int(radius)
    h = int(height)
    
    # Pre-calculate 2D offsets
    disk_offsets = []
    ring_offsets = []

    r_sq = r * r
    r_inner_sq = (r - 1) ** 2

    for u in range(-r, r + 1):
        for v in range(-r, r + 1):
            dist_sq = u*u + v*v
            if dist_sq <= r_sq:
                disk_offsets.append((u, v))
                if dist_sq >= r_inner_sq:
                    ring_offsets.append((u, v))

    # Simple axis alignment
    if axis == 'y':
        for i in range(h):
            y = by + i
            is_cap = (i == 0 or i == h - 1)

            if fill or is_cap:
                current_offsets = disk_offsets
            else:
                current_offsets = ring_offsets

            for u, v in current_offsets:
                points.append((bx + u, y, bz + v))

    elif axis == 'x':
        for i in range(h):
            x = bx + i
            is_cap = (i == 0 or i == h - 1)

            if fill or is_cap:
                current_offsets = disk_offsets
            else:
                current_offsets = ring_offsets

            for u, v in current_offsets:
                points.append((x, by + u, bz + v))

    elif axis == 'z':
        for i in range(h):
            z = bz + i
            is_cap = (i == 0 or i == h - 1)

            if fill or is_cap:
                current_offsets = disk_offsets
            else:
                current_offsets = ring_offsets

            for u, v in current_offsets:
                points.append((bx + u, by + v, z))
                             
    return points

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
