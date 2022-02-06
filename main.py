import random

import moderngl_window as mglw
from Effect import Effect


class App(mglw.WindowConfig):
    title = 'Ball'
    cursor = True
    window_size = 1600, 900
    resource_dir = 'shaders'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = mglw.geometry.quad_fs()
        self.program = self.load_program(vertex_shader='vertex.glsl',
                                         fragment_shader='fragment.glsl')
        self.program['u_resolution'] = self.window_size

        self.effect = Effect()
        self.spawn_point = (0, 0, 0)
        self.effect.explode(self.spawn_point)

        self.particle_array = []
        self.sphere_radius_array = []
        self.respawn()

    def render(self, time: float, frame_time: float):

        self.update_particles()

        self.ctx.clear()
        self.quad.render(self.program)

    def mouse_position_event(self, x: int, y: int, dx: int, dy: int):
        self.program['u_mouse'] = x + dx, y + dy

    def mouse_press_event(self, x: int, y: int, button: int):
        self.respawn()
        self.effect.explode(self.spawn_point)

    def respawn(self):
        self.spawn_point = [round(random.random(), 2) for _ in range(3)]
        self.spawn_point[1] -= 6

    def create_arrays(self):
        self.particle_array = [(p.x, p.y, p.z) for p in self.effect.particles]
        self.sphere_radius_array = [round(p.radius, 2) for p in self.effect.particles]

        self.program['particle_array'] = self.particle_array
        self.program['sphere_radius_array'] = self.sphere_radius_array

    def update_particles(self):
        self.effect.update()
        self.create_arrays()
        # print('----------------\n', self.particle_array,  '\n', self.sphere_radius_array)


if __name__ == '__main__':
    mglw.run_window_config(App)

