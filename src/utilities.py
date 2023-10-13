import numpy as np

def MAR(point1, point2, point3, point4, point5, point6, point7, point8):
    mar = (calculate_distance(point1, point2) + calculate_distance(point3, point4) + calculate_distance(point5, point6)) / (3.0 * calculate_distance(point7, point8))
    return mar

def EAR(point1, point2, point3, point4, point5, point6):
    ear = (calculate_distance(point2, point6) + calculate_distance(point3, point5)) / (2 * calculate_distance(point1, point4)) * 1.0
    return ear

def calculate_distance(point1, point2):
    distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return distance

