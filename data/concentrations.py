import json
import sys
from colour import Color

f = open( sys.argv[1] , 'rb' )
data = json.load(f)
f.close()

colors = list(Color('#2166ac').range_to(Color('#b2182b'), 100))
maxcc = max(data['Noro_concentration'])
#print(colors)
#print(maxcc)

features = []
for index, cc in enumerate(data['Noro_concentration']):
    numda = data['numda_Noro'][index]
    phi = data['phi_Noro'][index]
    score = cc / maxcc
    coloridx = round(score * 100)
    color = colors[coloridx if coloridx < 100 else 99]
    #print(index, cc, score, color, numda, phi)
    feature = {
        'type': 'Feature',
        'properties': {
            'type': 'concentration',
            'concentration': cc,
            'color': str(color),
            'score': score
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
