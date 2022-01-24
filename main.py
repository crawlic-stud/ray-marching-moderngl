import moderngl_window as mglw


class App(mglw.WindowConfig):
    window_size = 1280, 720
    resource_dir = 'shaders'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = mglw.geometry.quad_fs()
        self.program = self.load_program(vertex_shader='vertex.glsl',
                                         fragment_shader='fragment.glsl')
        self.program['u_resolution'] = self.window_size

    def render(self, time: float, frame_time: float):
        self.ctx.clear()
        self.quad.render(self.program)


if __name__ == '__main__':
    mglw.run_window_config(App)
