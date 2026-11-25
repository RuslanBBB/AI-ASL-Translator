import math

def normalize_landmarks(hand):
    wrist = hand[0]
    middle_base = hand[9]

    dx = middle_base.x - wrist.x
    dy = middle_base.y - wrist.y
    dz = middle_base.z - wrist.z

    scale = math.sqrt(dx**2 + dy**2)

    if scale < 1e-6:
        return None

    features = []

    for point in hand:
        x = (point.x - wrist.x) / scale
        y = (point.y - wrist.y) / scale
        z = (point.z - wrist.z) / scale

        features.append(x)
        features.append(y)
        features.append(z)

    return features