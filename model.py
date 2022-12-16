import math

# все вычисления проводятся в СИ
gravitational_constant = 6.67408E-11  # гравитационная постоянная Ньютона G
dt = 0.01  # шаг по времени просчёта физической модели
density_air_0 = 1.225  # плотность воздуха на поверхности Земли
rocket_form_constant = 0.5  # константа на форму ракеты
g = 9.8  # ускорение свободного падения у поверхности Земли
R = 8.31  # универсальная газовая постоянная
temperature_gradient = -0.0065  # скорость изменения температуры
molar_mass_of_air = 0.02896  # молярная масса воздуха
temperature = 273  # температура при нормальных условиях
pi = math.pi


def calculate_gravity(rocket, obj):
    """
    :param rocket: экземпляр класса Rocket
    :param obj: объект с которым просчитывается гравитация
    :return: Возвращает массив из x- и y- составляющих силы притяжения ракеты к объекту obj
    """
    distance = ((rocket.x - obj.x) ** 2 + (rocket.y - obj.y) ** 2) ** 0.5
    force = (gravitational_constant * (rocket.shell_mass + rocket.fuel_mass) * obj.mass) / distance ** 2
    alpha = math.atan2((obj.y - rocket.y), (obj.x - rocket.x))
    force_x = force * math.cos(alpha)
    force_y = force * math.sin(alpha)

    return [force_x, force_y]


def calculate_acceleration(rocket, force_x, force_y):
    """
    Изменяет x- и y- составляющие скорости ракеты за 1 кадр в соответствии с её полным ускорением
    :param rocket: экземпляр класса Rocket, который изменяем
    :param force_x: сила по Ox
    :param force_y: cила по Oy
    :return: None
    """
    rocket.vx += (force_x / (rocket.shell_mass + rocket.fuel_mass)) * dt
    rocket.vy += (force_y / (rocket.shell_mass + rocket.fuel_mass)) * dt


def calculate_thrust_force(rocket):
    """
    :param rocket: экземпляр класса Rocket
    :return: Возвращает массив из x- и y- составляющих силы реактивной тяги ракет
    """

    force_x, force_y = [0, 0]
    if rocket.engine_on:
        force_x = - rocket.mu * rocket.u * math.sin(rocket.angle)  # при отклонении влево sin>0 -> force_x<0
        force_y = rocket.mu * rocket.u * math.cos(rocket.angle)  # без отклонения cos>0 -> force_y>0
    return [force_x, force_y]


def waste_fuel(rocket):
    """
    Тратит часть топлива каждый кадр, уменьшая fuel mass, выключает двигатель при отсутствии топлива
    :param rocket: экземпляр класса Rocket
    :return: None
    """
    if rocket.engine_on:
        rocket.fuel_mass -= rocket.mu * dt
    if rocket.fuel_mass <= 0:
        rocket.engine_on = False


def calculate_moment_of_inertia(rocket):
    """
    Считает момент инерции
    :param rocket: экземпляр класса Rocket
    :return: момент инерции
    """
    rocket.moment_of_inertia = (rocket.shell_mass + rocket.fuel_mass) * (rocket.height ** 2 / 4) / 6


def calculate_angular_acceleration(rocket):
    """
    Рассчитывает угловое ускорение
    :param rocket: экземпляр класса Rocket
    :return: угловое ускорение
    """
    if rocket.engine_on:
        moment_of_power = - rocket.mu * rocket.u * (rocket.height / 2) * math.sin(rocket.nozzle_angle)
        epsilon = moment_of_power / rocket.moment_of_inertia
        rocket.omega += epsilon * dt


def move(rocket):
    """
    Пересчитывает координаты ракеты
    :param rocket: экземпляр класса Rocket
    :return: None
    """
    rocket.x += rocket.vx * dt
    rocket.y += rocket.vy * dt

    rocket.angle += rocket.omega * dt


def calculate_physical_time(planet):
    """
    Рассчитывает физическое время
    :param planet: экземпляр класса Planet
    :return: None
    """
    planet.time += int(planet.dT / dt) * dt


def calculate_physics(rocket, planet):
    """
    Главный модуль, который просчитывает всю физику
    :param rocket: экземпляр класса Rocket
    :param planet: экземпляр класса Planet
    :return: None
    """
    for i in range(int(planet.dT / dt)):
        thrust_force_x, thrust_force_y = 0, 0
        if rocket.fuel_mass > 0 and not rocket.dead:
            thrust_force_x, thrust_force_y = calculate_thrust_force(rocket)
            waste_fuel(rocket)
        gravity_force_x, gravity_force_y = calculate_gravity(rocket, planet)
        air_force_x, air_force_y = air_resistance_force(rocket, planet)

        calculate_acceleration(rocket, gravity_force_x + thrust_force_x + air_force_x,
                               gravity_force_y + thrust_force_y + air_force_y)
        collision(planet, rocket)
        calculate_angular_acceleration(rocket)
        move(rocket)
    calculate_physical_time(planet)


def air_resistance_force(rocket, planet):
    """
    Рассчитываем силу сопротивления для ракеты
    :param rocket: экземпляр класса Rocket
    :param planet: экземпляр класса Planet
    :return: None
    """
    height = (rocket.x ** 2 + rocket.y ** 2) ** 0.5 - planet.r
    if height > planet.air_force_height:
        return 0, 0
    degree = (-g * molar_mass_of_air / (R * temperature_gradient))
    density_air = density_air_0 * (1 + temperature_gradient * height / temperature) ** degree
    air_force = density_air * (rocket.vx ** 2 + rocket.vy ** 2) * rocket_form_constant * pi * (rocket.radius ** 2)
    v = (rocket.vx ** 2 + rocket.vy ** 2) ** 0.5
    if v != 0:
        air_force_x = - air_force * rocket.vx / v
        air_force_y = - air_force * rocket.vy / v
    else:
        air_force_x = 0
        air_force_y = 0
    return air_force_x, air_force_y


def calculate_energy(rocket, obj):
    """
    Возвращает энергию в каждый момент времени
    :return: полную энегрию тела
    """
    distance = ((rocket.x - obj.x) ** 2 + (rocket.y - obj.y) ** 2) ** 0.5
    potentional_energy = - gravitational_constant * obj.mass * (rocket.shell_mass + rocket.fuel_mass) / distance
    kinetic_energy = (rocket.shell_mass + rocket.fuel_mass) * (rocket.vx ** 2 + rocket.vy ** 2) / 2
    energy = potentional_energy + kinetic_energy

    return energy


def calculate_ellipse_param(rocket, obj):
    """Просчитывает параметры эллипса и возвращает их"""
    energy = calculate_energy(rocket, obj)
    distance = ((rocket.x - obj.x) ** 2 + (rocket.y - obj.y) ** 2) ** 0.5
    v_r = ((rocket.vx * rocket.x) + (rocket.vy * rocket.y)) / distance
    v_phi = ((rocket.vx ** 2 + rocket.vy ** 2) - v_r ** 2) ** 0.5
    l_0 = v_phi * distance
    print(energy)
    a = - gravitational_constant * (rocket.shell_mass + rocket.fuel_mass) * obj.mass / energy
    b = l_0 / (-2 * energy / (rocket.shell_mass + rocket.fuel_mass)) ** 0.5
    c = (a ** 2 - b ** 2) ** 0.5
    x_0 = a * (distance - a) / (a ** 2 - b ** 2) ** 0.5
    if abs((x_0 + c) / distance) >= 1:
        phi = math.pi
    else:
        phi = math.pi - math.acos(abs((x_0 + c) / distance))
    if x_0 == 0:
        psi = 0
    else:
        psi = math.atan(abs((distance * math.sin(phi)) / x_0))
    return a, b, psi


def collision(planet, rocket):
    """
    Отслеживает столконовение с планетой
    :param rocket: экземпляр класса Rocket
    :param planet: экземпляр класса Planet
    :return: None
    """
    for point in rocket.collision_point:
        x_point_collision = point[0] * math.cos(rocket.angle) + point[1] * math.sin(rocket.angle) + rocket.x
        y_point_collision = point[1] * math.cos(rocket.angle) - point[0] * math.sin(rocket.angle) + rocket.y
        if x_point_collision ** 2 + y_point_collision ** 2 <= planet.r ** 2:
            if (rocket.vx**2 + rocket.vy**2) ** 0.5 >= 300:
                rocket.explosion_start((x_point_collision - rocket.x) * planet.scale_factor,
                                       (y_point_collision - rocket.y) * planet.scale_factor)
            normal_velocity = (rocket.vx * rocket.x + rocket.vy * rocket.y) / ((rocket.x ** 2 + rocket.y ** 2) ** 0.5)
            if normal_velocity <= 0:
                rocket.vx -= normal_velocity * rocket.x / (rocket.x ** 2 + rocket.y ** 2) ** 0.5
                rocket.vy -= normal_velocity * rocket.y / (rocket.x ** 2 + rocket.y ** 2) ** 0.5
                rocket.vx /= 2
                rocket.vy /= 2
            rocket.omega = 0


if __name__ == "__main__":
    print("This module is not for direct call!")
