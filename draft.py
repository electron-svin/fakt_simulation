import math

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""
planet_mass = 5.9742E24
R_planet = 6371
rocket_mass = 1
fuel_mass = 1
mu = 1 #скорость изменения массы топлива
u = 1 #скороскть истекания топлива относительно ракеты

def calculate_force(rocket):

    r = R_planet + actual_position #актульное расстляние от центра земли до ракеты
    f = (actual_mass * gravitational_constant * planet_mass) / (r)**2 #актуальная сила притяжения


def calculate_mass(rocket, t, dt):
    global  actual_mass
    actual_mass = rocket_mass + fuel_mass #масса в t=0
    actual_mass = actual_mass - dt * mu #изменение массы

def calculate_movement(rocket, t, dt):

    dv = (-u * mu - rocket.f) / actual_mass
    dx = dv * dt







