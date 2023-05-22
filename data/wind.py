import json
import math
import sys

f = open( sys.argv[1] , 'rb' )
data = json.load(f)
f.close()

features = []
for index, velu in enumerate(data['Velocity_U']):
    velv = data['Velocity_V'][index]
    angle = math.atan2(velv, velu) * 180 / math.pi
    speed = math.sqrt(math.pow(velu, 2) + math.pow(velv, 2))
    numda = data['numda_Flow_vector'][index]
    phi = data['phi_Flow_vector'][index]
    #print(index, velu, velv, angle, speed,numda, phi)
    feature = {
        'type': 'Feature',
        'properties': {
            'type': 'speed',
            'Velocity_U': velu,
            'Velocity_V': velv,
            'angle': angle,
            'speed': speed
        },
        'geometry': {
            'type': 'Point',
            'coordinates': [ numda, phi ]
        }
    }
    features.append(feature)

geo = {
    'type': 'FeatureCollection',
    'features': features
    }

print(json.dumps(geo, sort_keys=True, indent=4))
