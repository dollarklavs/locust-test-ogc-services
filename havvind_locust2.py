from locust import HttpLocust, TaskSet, task
from operator import itemgetter
import time
import random

class UserBehavior(TaskSet):
    request_aada = {
                "service":"WFS", 
                "version":"2.0.0", 
                "request":"GetFeature", 
                "typeName":"havvind:AabenDoerAnsoegningsomraade", 
                "outputFormat":"gml32", 
                "BBOX":"" 
              }

    request_aadp = {
                "service":"WFS", 
                "version":"2.0.0", 
                "request":"GetFeature", 
                "typeName":"havvind:AabenDoerProcedureomraade", 
                "outputFormat":"gml32"
              }              
           
           
    @task(1)
    def post_to_wfs_aada(self):
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
                self.client.post("", request)
            return ll, lr, ul, ur
            
        def pan(bbox, steps, request, distance, reverse=False):
            version_choices = ["2.0.0", "1.1.0"]
            steps = range(1, steps + 1)
            if reverse:
                steps = reversed(steps)
                
            for step in steps:
                bbox = [e + (step * distance) for e in bbox]
                bbox_str = "{},{},{},{}".format(*bbox)
                request["BBOX"] = bbox_str
                version = random.choice(version_choices)
                request["version"] = version
                self.client.post("", request)
        
        new_bbox = zoom(ranges, steps, self.request_aada)
        pan(new_bbox, 8, self.request_aada, 5000)
        time.sleep(10)
        new_bbox = zoom(ranges, steps, self.request_aada, True)
        pan(new_bbox, 8, self.request_aada, 15000)
        time.sleep(3)
        pan(new_bbox, 8, self.request_aada, 15000, True)
        
    @task(2)    
    def post_to_wfs_aadp(self):
            self.client.post("", self.request_aadp)


    
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
    
