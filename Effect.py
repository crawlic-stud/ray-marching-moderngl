import random
from math import sqrt


class Particle3D:
    def __init__(self, radius, pos, color):
        self.radius = radius
        self.x, self.y, self.z = pos
        self.color = tuple([i/255 for i in color])
        self.direction = 0, 0, 0
        self.shrink_speed = 0

        self.gravity = 0
        self.vertical_speed = self.gravity

        self.trace_shrink_speed = 0

    def shrink(self):
        if not self.shrink_speed:
            return
        self.radius -= self.shrink_speed

    def move(self):
        if not any(self.direction):
            return
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.z += self.direction[2]

    def apply_gravity(self):
        self.y += self.vertical_speed
        self.vertical_speed += self.gravity

    def update(self):
        self.move()
        self.apply_gravity()
        self.shrink()


class Effect:
    def __init__(self):
        self.particles = []

    def explode(self, pos):
        self.particles = explosion_effect(size=0.1,
                                          amount=50,
                                          pos=pos,
                                          ball_radius=0.5)
        print([[p.x, p.y, p.z] for p in self.particles])

    def update(self):
        for particle in self.particles:
            if particle.radius > 0:
                particle.update()


def explosion_effect(size, amount, pos, ball_radius, gravity=0.0005, ball_lifespan=100):
    particles = [Particle3D(
        ball_radius,
        pos,
        (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)))
        for _ in range(amount)]

    for i, particle in enumerate(particles):

        vector_len = random.random() * size
        dx = round(random.random(), 5) * random.choice([-1, 1])
        dy = round(random.random(), 5) * random.choice([-1, 1])
        dz = round(random.random(), 5) * random.choice([-1, 1])
        # dy = round(sqrt(abs(vector_len ** 2 - dx ** 2)), 5) * random.choice([-1, 1])
        # dz = round(sqrt(abs(vector_len ** 2 - dy ** 2)), 5) * random.choice([-1, 1])

        particles[i].direction = dx / 10, dy / 10, dz / 10
        particles[i].shrink_speed = round(random.random(), 5) / ball_lifespan
        particles[i].gravity = gravity

    # print([[p.direction, p.shrink_speed] for p in particles])
    return particles
