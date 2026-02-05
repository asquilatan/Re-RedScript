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
    """
    Generates points for a sphere using an optimized rasterization algorithm.

    Optimizations:
    1. Loop Bounds: Instead of iterating the full bounding box (O(R^3)), we calculate
       exact loop bounds for Y and Z based on the sphere equation, skipping ~50% of
       checks (corners of the cube).
    2. Hollow Skipping: For hollow spheres (fill=False), we calculate the inner solid
       core radius and skip iterating Z values within that core. This reduces the
       complexity from O(R^3) to roughly O(R^2) (proportional to surface area).
    """
    cx, cy, cz = center
    points = []
    r = int(radius)
    r_sq = r**2

    # Precompute inner radius sq for shell logic
    # The shell includes points where dist_sq >= (r-1)^2
    min_r_sq = (r - 1)**2 if not fill else 0
    
    # Iterate X within radius
    for x in range(cx - r, cx + r + 1):
        dx = x - cx
        dx2 = dx*dx
        # If x is outside radius (should cover by range, but for safety/clarity)
        if dx2 > r_sq: continue

        # Calculate max Y deviation at this X
        # y^2 <= r^2 - x^2
        dy_max = int(math.sqrt(r_sq - dx2))

        for y in range(cy - dy_max, cy + dy_max + 1):
            dy = y - cy
            dy2 = dy*dy
            # Calculate remaining squared radius allowance for Z
            rem_sq = r_sq - dx2 - dy2
            if rem_sq < 0: continue

            # Max Z deviation
            dz_max = int(math.sqrt(rem_sq))

            if fill:
                # Solid sphere: Fill the entire Z column
                for z in range(cz - dz_max, cz + dz_max + 1):
                    points.append((x, y, z))
            else:
                # Hollow sphere: Skip the inner core.
                # We need points where dz^2 >= (r-1)^2 - dx^2 - dy^2
                rhs_in = min_r_sq - dx2 - dy2

                if rhs_in <= 0:
                    # Inner radius constraint is irrelevant (inner sphere doesn't reach this x,y column).
                    # All points in the outer sphere at this x,y are part of the shell.
                    for z in range(cz - dz_max, cz + dz_max + 1):
                        points.append((x, y, z))
                else:
                    # We have a hollow core.
                    # We need |dz| >= sqrt(rhs_in)
                    # Use ceil(sqrt(rhs_in)) logic carefully with integers
                    dz_min = int(math.sqrt(rhs_in))
                    if dz_min * dz_min < rhs_in:
                        dz_min += 1

                    # Add bottom cap of the shell column
                    # Range: [-dz_max, -dz_min]
                    if dz_min <= dz_max:
                        for z in range(cz - dz_max, cz - dz_min + 1):
                             points.append((x, y, z))

                        # Add top cap of the shell column
                        # Range: [dz_min, dz_max]
                        for z in range(cz + dz_min, cz + dz_max + 1):
                             points.append((x, y, z))

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
