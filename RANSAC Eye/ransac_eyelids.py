import numpy as np
import random


class BadFitShape(Exception):
    pass


def fit_line(xs, ys):
    
    a, b = np.polyfit(np.array(xs), np.array(ys), 1)

    if abs(a) > 0.5: raise BadFitShape()
    return a, b


def fit_parabola(xs, ys):
    
    a, b, c = np.polyfit(xs, ys, 2)

    if a < 0: raise BadFitShape()
    return a, b, c


def ransac_parabola(points_l, points_r, ransac_iters_max=5, refine_iters_max=2, max_err=2, debug=False):
    
    if len(points_l) < 3 or len(points_r) < 3: return None
    
    points = np.concatenate([points_l, points_r])
    pts_x, pts_y = np.split(points, 2, axis=1)
    pts_x, pts_y = np.squeeze(pts_x), np.squeeze(pts_y)
    
    best_parabola = None
    best_support = float('-inf')

    # Not enough points to start process
    if len(points_r) < 3 or len(points_l) < 3: return None
    
    # Perform N RANSAC iterations
    for _ in range(ransac_iters_max):
        
        try:
            sample = random.sample(points_r, 3) + (random.sample(points_l, 3))
            sample_xs, sample_ys = [x for (x, _) in sample], [y for (_, y) in sample]
            a, b, c = fit_parabola(sample_xs, sample_ys)
            
            # Iteratively refine inliers further
            for _ in range(refine_iters_max):
                
                pts_parabola_y = a * pts_x ** 2 + b * pts_x + c
                inlier_inds = np.squeeze([np.abs(pts_y - pts_parabola_y) < max_err])
                inliers = points[inlier_inds]
                
                if inliers.size < 5: break
                a, b, c = fit_parabola(pts_x[inlier_inds], pts_y[inlier_inds])
    
            support = len(inliers)
            
            if support > best_support:
                best_parabola = (a, b, c)
                best_support = support
                
        except BadFitShape: continue 
            
        # Early termination for > 90% inliers
        if len(inliers) / len(points) > 0.90: break

    return best_parabola


__lower_eyelid_inliers_min = 30

def ransac_line(points, ransac_iters_max=5, refine_iters_max=2, max_err=2, debug=False):
    
    if len(points) < __lower_eyelid_inliers_min: return None
    
    pts_x, pts_y = np.split(points, 2, axis=1)
    pts_x, pts_y = np.squeeze(pts_x), np.squeeze(pts_y)
    
    best_line = None
    best_support = float('-inf')

    # Not enough points to start process
    if len(points) < __lower_eyelid_inliers_min : return None
    
    # Perform N RANSAC iterations
    for _ in range(ransac_iters_max):
        
        try:
            #TypeError: Population must be a sequence.  For dicts or sets, use sorted(d).
            points = list(points)

            sample = random.sample(points, 3)
            sample_xs, sample_ys = [x for (x, _) in sample], [y for (_, y) in sample]
            a, b = fit_line(sample_xs, sample_ys)
            
            # Iteratively refine inliers further
            for _ in range(refine_iters_max):
                
                pts_line_y = a * pts_x + b
                inlier_inds = np.squeeze([np.abs(pts_y - pts_line_y) < max_err])
                inliers = points[inlier_inds]
                
                if len(inliers) < 3: break
                
                a, b = fit_line(pts_x[inlier_inds], pts_y[inlier_inds])
    
            support = len(inliers)
            
            if len(inliers) > __lower_eyelid_inliers_min and support > best_support:
                best_line = (a, b)
                best_support = support
                
        except BadFitShape: continue 
            
        # Early termination for > 90% inliers
        if len(inliers) / len(points) > 0.90: break

    return best_line