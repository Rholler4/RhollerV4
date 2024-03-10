import math

angle1 = int(input("Provide angle: "))
distance1 = int(input("Provide distance: "))

#  Convert Dec to Rad:
angle1 = math.radians(angle1)
distance1 = math.radians(distance1)

x1 = distance1 * math.cos(angle1)
y1 = distance1 * math.sin(angle1)


print(math.cos(angle1))
print(x1)
print(y1)
