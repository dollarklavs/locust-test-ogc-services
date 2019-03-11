from ast import literal_eval
from operator import itemgetter

request_aada = {
            "service":"WFS", 
            "version":"2.0.0", 
            "request":"GetFeature", 
            "typeName":"havvind:AabenDoerAnsoegningsomraade", 
            "outputFormat":"gml32", 
            "BBOX":"" 
          }

ranges = (
            [777994, 240348, -100000],
            [6478047, 5355048, -210000],
            [1262354, 482528, -142000],
            [7039546, 5916547, -210000])

# for e in range(1, 6):
    # get_startstep = itemgetter(0, 2)
    # startstep = list(map(get_startstep, ranges))
    # if e == 1:
        # ll = startstep[0][0]
        # lr = startstep[1][0]
        # ul = startstep[2][0]
        # ur = startstep[3][0]
    # else:
        # ll = startstep[0][0] + (e * startstep[0][1])
        # lr = startstep[1][0] + (e * startstep[1][1])
        # ul = startstep[2][0] + (e * startstep[2][1])
        # ur = startstep[3][0] + (e * startstep[3][1])
    # bbox = "{},{},{},{}".format(ll, lr, ul, ur)
    # request_aada["BBOX"] = bbox
    # print(request_aada, '\n')


# simulate zooming inn (decreasing the bounding box)
steps = range(1, 6)
ranges = (
    [777994, 240348, -100000],
    [6478047, 5355048, -210000],
    [1262354, 482528, -142000],
    [7039546, 5916547, -210000])
def zoom(ranges, steps, request, reverse=False):
    if reverse:
        steps = reversed(steps)
    
    for step in steps:
        get_startstep = itemgetter(0, 2)
        startstep = list(map(get_startstep, ranges))
        if step == 1:
            ll = startstep[0][0]
            lr = startstep[1][0]
            ul = startstep[2][0]
            ur = startstep[3][0]
        else:
            ll = startstep[0][0] + (step * startstep[0][1])
            lr = startstep[1][0] + (step * startstep[1][1])
            ul = startstep[2][0] + (step * startstep[2][1])
            ur = startstep[3][0] + (step * startstep[3][1])
        bbox = "{},{},{},{}".format(ll, lr, ul, ur)
        request["BBOX"] = bbox
    return ll, lr, ul, ur
    
def pan(bbox, steps, request, distance, reverse=False):
    steps = range(1, steps + 1)
    if reverse:
        steps = reversed(steps)
        
    for step in steps:
        bbox = tuple(int(e) + (step * distance) for e in bbox)
        bbox = "{},{},{},{}".format(*bbox)
        request["BBOX"] = bbox
        # self.client.post("", request)

new_bbox = zoom(ranges, steps, request_aada) 
print(new_bbox, type(new_bbox[0]))       
# pan(new_bbox, 8, self.request_aada, 5000)







