import pytest
import math
from render import forward_plus_light_culling as mod

CASES = [
    ("cap", 'm.index_capacity(256, 8) == 32'),
    ("tiles", 'm.tile_count(1920, 16) == 120'),
    ("slice", 'm.depth_slice(1, 9, 8) == approx(1.0)'),
    ("radius", 'm.sphere_radius(2, 3) == 6'),
    ("hit", 'm.sphere_hits_box(0, 0, 0, 1, (-1, -1, -1, 1, 1, 1)) is True'),
    ("overflow", 'm.overflow(3, 32) == 3'),
    ("cone", 'm.cone_keep(0.9, 0.8) is True'),
    ("merge", 'm.merge_visible([1, 2, 3], [2, 3]) == [2, 3]'),
    ("rebuild", 'm.rebuild_needed(10, 12) is True'),
    ("size", 'm.tile_size(1920, 120) == 16'),
    ("offset", 'm.index_offset(2, 32) == 64'),
    ("cull", 'm.cull_keep(True, True) is True'),
    ("key", 'm.light_key("lamp", 2) == "lamp:2"'),
    ("tile", 'm.tile_id(1, 2, 120) == 241'),
    ("total", 'm.total_lights([1, 2, 3]) == 3')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
