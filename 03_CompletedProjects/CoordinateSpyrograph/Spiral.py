import math

# Tommy Trojan approx coords
center_lat = 34.0205663
center_lon = -118.2880217

R = 36
r = 9
a = 30

points = []

t = 0
while t <= 8 * math.pi:   # 8π gives full closed curve
    x = (R+r)*math.cos((r/R)*t) - a*math.cos((1+r/R)*t)
    y = (R+r)*math.sin((r/R)*t) - a*math.sin((1+r/R)*t)

    # scale down
    scale = 0.00001
    lat = center_lat + (y * scale)
    lon = center_lon + (x * scale)

    points.append(f"{lon},{lat}")

    t += 0.01

# create KML
with open("spiro.kml", "w") as f:
    f.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<Placemark>
<name>Spirograph</name>
<LineString>
<coordinates>
""")

    f.write(" ".join(points))

    f.write("""
</coordinates>
</LineString>
</Placemark>
</Document>
</kml>
""")

print("KML file created: spiro.kml")