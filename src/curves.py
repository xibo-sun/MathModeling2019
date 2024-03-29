# -*- coding: utf-8 -*-

import numpy as np


RMIN = 200


def sovleEquation(a, b, c):
    x1 = (-b + np.sqrt(np.square(b) - 4*a*c)) / (2 * a)
    x2 = (-b - np.sqrt(np.square(b) - 4*a*c)) / (2 * a)
    return x1, x2


def sphericalCoor(p0, p1, n):
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    n1, n2, n3 = n
    try:
        k1 = -(n1*(z1-z0)-n3*(x1-x0))/(n2*(z1-z0)-n3*(y1-y0))
        c1 = ((z1-z0)*np.dot(n, p1) - n3*np.dot(p1-p0, p1))/(n2*(z1-z0)-n3*(y1-y0))
        k2 = -(n1*(y1-y0)-n2*(x1-x0))/(n3*(y1-y0)-n2*(z1-z0))
        c2 = ((y1-y0)*np.dot(n, p1) - n2*np.dot(p1-p0, p1))/(n3*(y1-y0)-n2*(z1-z0))
        a = 1 + k1*k1 + k2*k2
        b = -2*x1 + 2*(c1-y1)*k1 + 2*(c2-z1)*k2
        c = x1*x1 + (c1-y1)**2 + (c2-z1)**2 - RMIN**2
        xr1, xr2 = sovleEquation(a, b, c)
        yr1, yr2 = k1*xr1 + c1, k1*xr2 + c1
        zr1, zr2 = k2*xr1 + c2, k2*xr2 + c2
        pr1 = np.array([xr1, yr1, zr1])
        pr2 = np.array([xr2, yr2, zr2])
        if n2*(z1-z0)-n3*(y1-y0) == 0 or n3*(y1-y0)-n2*(z1-z0) == 0:
            print(p1, p0, n)
    except:
        print(p0, p1, n)
    return pr1, pr2


def tangentialCoord(n, pr, p2):
    n1, n2, n3 = n
    xr, yr, zr = pr
    x2, y2, z2 = p2
    k1 = -(n1*(zr-z2)-n3*(xr-x2))/(n2*(zr-z2)-n3*(yr-y2))
    c1 = ((zr-z2)*np.dot(n, p2)-n3*(np.sum(np.square(pr))-RMIN**2-np.dot(p2, pr)))/(n2*(zr-z2)-n3*(yr-y2))
    k2 = -(n1*(yr-y2)-n2*(xr-x2))/(n3*(yr-y2)-n2*(zr-z2))
    c2 = ((yr-y2)*np.dot(n, p2)-n2*(np.sum(np.square(pr))-RMIN**2-np.dot(p2, pr)))/(n3*(yr-y2)-n2*(zr-z2))
    a = 1 + k1**2 + k2**2
    b = -2*xr + 2*(c1-yr)*k1 + 2*(c2-zr)*k2
    c = xr**2 + (c1-yr)**2 + (c2-zr)**2 - RMIN**2
    xt1, xt2 = sovleEquation(a, b, c)
    yt1, yt2 = k1*xt1 + c1, k1*xt2 + c1
    zt1, zt2 = k2*xt1 + c2, k2*xt2 + c2
    pt1 = np.array([xt1, yt1, zt1])
    pt2 = np.array([xt2, yt2, zt2])
    return pt1, pt2


def theataCos(v1, v2):
    return np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))


def computeDistance(p_before, p_current, p_next):
    pos_before = p_before
    pos_current = p_current
    pos_next = p_next
    vec_current = pos_current - pos_before
    vec_next = pos_next - pos_current

    n = np.cross(vec_current, vec_next)
    distance_current_next = np.sqrt(np.sum(np.square(pos_current-pos_next)))
    theata_cos = theataCos(vec_current, vec_next)

    if theata_cos == 1:
        return distance_current_next, [], [], 0

    pos1_circuit, pos2_circuit = sphericalCoor(pos_before, pos_current, n)

    theata = np.arccos(theata_cos)
    d = np.abs(RMIN * theata_cos)

    if distance_current_next >= np.abs(2 * RMIN * np.sin(theata)):
        if np.linalg.norm(pos1_circuit - pos_next) < np.linalg.norm(pos2_circuit - pos_next):
            pos_circuit = pos1_circuit
        else:
            pos_circuit = pos2_circuit
        D = np.sqrt(np.sum(np.square(pos_circuit - pos_next)))
        theata1 = np.arccos(RMIN / D)
        theata2 = np.arccos(d / D)
        if theata_cos > 0:
            # print("11111")
            angle = theata + theata2 - theata1
            straight_len = D * np.sin(theata1)
            p_tang1, p_tang2 = tangentialCoord(n, pos_circuit, pos_next)
        else:
            # print("22222")
            theata3 = np.arccos(d / RMIN)
            angle = 2*np.pi - theata1 - theata2 - theata3
            straight_len = D * np.sin(theata1)
            p_tang1, p_tang2 = tangentialCoord(n, pos_circuit, pos_next)
        distance = angle * RMIN + straight_len
    else:
        if np.linalg.norm(pos1_circuit - pos_next) > np.linalg.norm(pos2_circuit - pos_next):
            pos_circuit = pos1_circuit
        else:
            pos_circuit = pos2_circuit
        D = np.sqrt(np.sum(np.square(pos_circuit - pos_next)))
        theata1 = np.arccos(RMIN / D)
        theata2 = np.arccos(d / D)
        # print(theata_cos, pos2_circuit, pos1_circuit, D)
        if theata_cos > 0:
            # print("33333")
            angle = 2*np.pi - theata + theata2 - theata1
            straight_len = D * np.sin(theata2)
        else:
            # print("44444")
            theata1 = np.arccos(RMIN / D)
            angle = 3 * np.pi - theata1 - theata2 - theata
            straight_len = D * np.sin(theata1)
        distance = angle * RMIN + straight_len
    # return distance
    p_tang1, p_tang2 = tangentialCoord(n, pos_circuit, pos_next)
    # print(np.linalg.norm(p_tang1-pos_circuit), np.linalg.norm(pos_current-pos_circuit))
    # print(pos_circuit)
    # print(p_tang1, p_tang2)
    # print(theataCos(p_tang1-pos_circuit, pos_current-pos_circuit))
    # print(theataCos(p_tang2-pos_circuit, pos_current-pos_circuit))
    # print(np.cos(angle))
    t1 = theataCos(pos_circuit - p_tang1, pos_circuit - pos_current)
    t2 = theataCos(pos_circuit - p_tang2, pos_circuit - pos_current)
    t = np.cos(angle)
    if np.abs(t1 - t) < np.abs(t2 - t):
        pos_tang = p_tang1
    else:
        pos_tang = p_tang2
    return distance, pos_circuit, pos_tang, angle
