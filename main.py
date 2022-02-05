import random

import moderngl_window as mglw


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

        self.particle_array = []
        self.sphere_radius = 1
        self.recreate()

    def render(self, time: float, frame_time: float):
        #self.move_particles(0.0, -0.05, 0.0)
        #self.shrink_particles(0.01)
        self.update_particles()
        self.ctx.clear()
        self.quad.render(self.program)

    def mouse_position_event(self, x: int, y: int, dx: int, dy: int):
        self.program['u_mouse'] = x + dx, y + dy

    def mouse_press_event(self, x: int, y: int, button: int):
        self.recreate()

    def recreate(self, size=50):
        array = [(random.random(), random.random(), random.random()) for _ in range(size)]
        self.particle_array = array
        self.sphere_radius = 1

    def move_particles(self, dx, dy, dz):
        self.particle_array = [(p[0] + dx, p[1] + dy, p[2] + dz) for p in self.particle_array]
    
    def shrink_particles(self, amount):
        self.sphere_radius -= amount if self.sphere_radius > 0 else 0
    
    def update_particles(self):
        self.program['random_array'] = self.particle_array
        self.program['sphere_radius'] = self.sphere_radius


if __name__ == '__main__':
    mglw.run_window_config(App)
