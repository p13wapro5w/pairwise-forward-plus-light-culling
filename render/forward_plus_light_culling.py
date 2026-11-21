import math


def _ceil_div(value, divisor):
    """向上取整的整数除法。"""
    if divisor <= 0:
        raise ValueError("divisor must be positive")
    return -(-int(value) // int(divisor))


def index_capacity(total, slices):
    """索引表容量：按深度切片均分后每个切片可容纳的灯数。

    向上取整，保证总数不能整除时最后一盏灯也有位置。
    """
    return _ceil_div(total, slices)


def tile_count(resolution, tile):
    """分块数量：屏幕某一维按分块边长切分后的块数。"""
    return _ceil_div(resolution, tile)


def depth_slice(near, far, slices):
    """深度切片：单个切片覆盖的深度区间厚度。"""
    if slices <= 0:
        raise ValueError("slices must be positive")
    return (far - near) / slices


def sphere_radius(radius, scale):
    """包围球半径：光源半径按实际缩放，不能用半径的一半。"""
    return radius * scale


def sphere_hits_box(cx, cy, cz, radius, box):
    """球盒相交：球心到轴对齐包围盒的最近距离与半径比较。

    box 为 (min_x, min_y, min_z, max_x, max_y, max_z)。
    球心在盒内时距离为 0，必然相交。
    """
    min_x, min_y, min_z, max_x, max_y, max_z = box
    nx = min(max(cx, min_x), max_x)
    ny = min(max(cy, min_y), max_y)
    nz = min(max(cz, min_z), max_z)
    dx = cx - nx
    dy = cy - ny
    dz = cz - nz
    return dx * dx + dy * dy + dz * dz <= radius * radius


def overflow(overflow_count, capacity):
    """溢出计数：写入索引表的溢出灯数，受表容量上限约束。"""
    return max(0, min(int(overflow_count), int(capacity)))


def cone_keep(direction_dot, cos_outer):
    """聚光锥剔除：光轴与分块方向的夹角在锥内才保留。"""
    return direction_dot >= cos_outer


def merge_visible(full, visible):
    """可见表合并：取两表中的交集，保持 full 的顺序并去重。"""
    visible_set = set(visible)
    merged = []
    seen = set()
    for light in full:
        if light in visible_set and light not in seen:
            merged.append(light)
            seen.add(light)
    return merged


def rebuild_needed(old_count, new_count):
    """容量重建：灯数量变化时缓冲容量不再匹配，必须重建。"""
    return old_count != new_count


def tile_size(resolution, target):
    """分块尺寸：按目标块数把分辨率均分，向上取整。"""
    return _ceil_div(resolution, target)


def index_offset(tile, capacity):
    """索引偏移：第 tile 个分块在索引表中的起始位置。"""
    return tile * capacity


def cull_keep(inside, in_front):
    """视锥保留：同时在视锥内且位于相机前方才保留。"""
    return bool(inside and in_front)


def light_key(seed, index):
    """光源键：用稳定前缀和序号唯一标识一盏灯。"""
    return f"{seed}:{index}"


def tile_id(ix, iy, cols):
    """分块 id：按行优先把二维分块坐标压成一维。"""
    return iy * cols + ix


def total_lights(lists):
    """灯总数：展开各分块的灯列表后统计条目数。"""
    total = 0
    for item in lists:
        if isinstance(item, (list, tuple, set, frozenset, dict)):
            total += len(item)
        else:
            total += 1
    return total
