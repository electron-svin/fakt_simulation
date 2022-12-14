import math

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""
planet_mass = 5.9742E24
R_planet = 6371
dt = 0.01


def calculate_gravity(rocket, obj):
    """Возвращает массив из x- и y- составляющих силы притяжения ракеты к объекту obj"""
    distance = ((rocket.x - obj.x) ** 2 + (rocket.y - obj.y) ** 2) ** 0.5
    force = (gravitational_constant * (rocket.shell_mass + rocket.fuel_mass) * obj.mass) / distance ** 2
    alpha = math.atan2((obj.y - rocket.y), (obj.x - rocket.x))
    force_x = force * math.cos(alpha)
    force_y = force * math.sin(alpha)

    return [force_x, force_y]


def calculate_acceleration(rocket, force_x, force_y):
    """Изменяет x- и y- составляющие скорости ракеты за 1 кадр в соответствии с её полным ускорением"""
    rocket.vx += (force_x / (rocket.shell_mass + rocket.fuel_mass)) * dt
    rocket.vy += (force_y / (rocket.shell_mass + rocket.fuel_mass)) * dt


def calculate_thrust_force(rocket):
    """Возвращает массив из x- и y- составляющих силы реактивной тяги ракеты"""
    force_x, force_y = [0, 0]
    if rocket.engine_on:
        force_x = - rocket.mu * rocket.u * math.sin(rocket.angle)  # при отклонении влево sin>0 -> force_x<0
        force_y = rocket.mu * rocket.u * math.cos(rocket.angle)  # без отклонения cos>0 -> force_y>0 (ось y инвертирована)
    return [force_x, force_y]


def waste_fuel(rocket):
    """Тратит часть топлива каждый кадр, уменьшая fuel mass, выключает двигатель при отсутствии топлива"""
    if rocket.engine_on:
        rocket.fuel_mass -= rocket.mu * dt
    if rocket.fuel_mass <= 0:
        rocket.engine_on = False
    
def calculate_moment_of_inertia(rocket):
    rocket.moment_of_inertia = (rocket.shell_mass + rocket.fuel_mass) * (rocket.height ** 2 / 4 + rocket.coord_cm ** 2) / 6


def calculate_angular_acceleration(rocket):
    if rocket.engine_on:
        moment_of_power = - rocket.mu * rocket.u * (rocket.height / 2 + rocket.coord_cm) * math.sin(rocket.nozzle_angle)
        epsilon = moment_of_power / rocket.moment_of_inertia
        rocket.omega += epsilon * dt


def move(rocket):
    rocket.x += rocket.vx * dt
    rocket.y += rocket.vy * dt

    rocket.angle += rocket.omega * dt


def calculate_physical_time(planet):
    planet.time += int(planet.dT / dt) * dt


def calculate_rocket(rocket, planet):
    for i in range(int(planet.dT / dt)):
        thrust_force_x, thrust_force_y = 0, 0
        if rocket.fuel_mass > 0:
            thrust_force_x, thrust_force_y = calculate_thrust_force(rocket)
            waste_fuel(rocket)
        gravity_force_x, gravity_force_y = calculate_gravity(rocket, planet)

        calculate_acceleration(rocket, gravity_force_x + thrust_force_x, gravity_force_y + thrust_force_y)
        calculate_moment_of_inertia(rocket)
        collision(planet, rocket)
        calculate_angular_acceleration(rocket)
        move(rocket)


def calculate_energy(rocket, obj):
    """Возвращает энергию в каждый момент времени"""
    distance = ((rocket.x - obj.x) ** 2 + (rocket.y - obj.y) ** 2)
    potentional_energy = - gravitational_constant * obj.mass / distance
    kinetic_energy = (rocket.shell_mass + rocket.fuel_mass) * (rocket.vx ** 2 + rocket.vy ** 2) / 2
    energy = potentional_energy + kinetic_energy

    return energy


def calculate_ellipse_param(rocket, obj, energy):
    """Просчитывает параметры эллипса и возвращает их"""
    a = - gravitational_constant * (rocket.shell_mass + rocket.fuel_mass) * obj.mass / energy
    b = 10 #чуть позже
    return a, b


def collision(planet, rocket):
    count = 0
    for point in rocket.collision_point:
        if (point[0] * math.cos(rocket.angle) + point[1] * math.sin(rocket.angle) + rocket.x) ** 2 + \
                (point[1] * math.cos(rocket.angle) - point[0] * math.sin(rocket.angle) + rocket.y) ** 2 <= planet.r ** 2:
            normal_velocity = (rocket.vx * rocket.x + rocket.vy * rocket.y) / ((rocket.x ** 2 + rocket.y ** 2) ** 0.5)
            if normal_velocity <= 0:
                rocket.vx -= normal_velocity * rocket.x / (rocket.x ** 2 + rocket.y ** 2) ** 0.5
                rocket.vy -= normal_velocity * rocket.y / (rocket.x ** 2 + rocket.y ** 2) ** 0.5
                rocket.vx /= 2
                rocket.vy /= 2
            count += 1
            rocket.omega = 0


if __name__ == "__main__":
    print("This module is not for direct call!")