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
           
    request_am_pmpa_inspire = {
                "service":"WFS", 
                "version":"2.0.0", 
                "request":"GetFeature", 
                "typeNames":"am:ManagementRestrictionOrRegulationZone",
                "BBOX":"" 
              }              
    @task(1)
    def post_to_wfs_aada(self):
    # simulate zooming inn (decreasing the bounding box)
        steps = range(1, 6)
        originbbox = (5900000,120000,6500000,1000000)
        def zoom(originbbox, steps, request, reverse=False):
            if reverse:
                steps = reversed(steps)
            
            for step in steps:
                # llx, lly, urx, ury = map(lambda x: x * (1/step), originbbox)
                llx, lly, urx, ury = [(1/step) * coord for coord in originbbox]
                bbox = "{},{},{},{}".format(llx, lly, urx, ury)
                request["BBOX"] = bbox
                responce = self.client.get("/am_pmpa_inspire", params=request)
                print(responce.url)
            return llx, lly, urx, ury
            
        def pan(bbox, steps, request, distance, reverse=False):
            version_choices = ["2.0.0", "1.1.0"]
            version_choices = ["2.0.0"]
            steps = range(1, steps + 1)
            if reverse:
                steps = reversed(steps)
                
            for step in steps:
                bbox = [e + (step * distance) for e in bbox]
                bbox_str = "{},{},{},{}".format(*bbox)
                request["BBOX"] = bbox_str
                version = random.choice(version_choices)
                request["version"] = version
                responce = self.client.get("/am_pmpa_inspire", params=request)
                print(responce.url)
        
        new_bbox = zoom(originbbox, steps, self.request_am_pmpa_inspire)
        pan(new_bbox, 8, self.request_am_pmpa_inspire, 5000)
        time.sleep(random.choice(range(3, 15, 3)))
        new_bbox = zoom(originbbox, steps, self.request_am_pmpa_inspire, reverse=True)
        pan(new_bbox, 8, self.request_am_pmpa_inspire, 15000)
        time.sleep(random.choice(range(6, 18, 2)))
        pan(new_bbox, 8, self.request_am_pmpa_inspire, 15000, reverse=True)
        
#     @task(2)    
#     def post_to_wfs_aadp(self):
#             self.client.post("/am_pmpa_inspire", self.request_am_pmpa_inspire)
# 

## LL (382830.362295 6054705.374469)
## LR (970539.330127 6062664.359428)
## UL (346487.995986 6410774.542683)
## UR (905429.812147 6415847.834646)
## Working bounding box parameter for 3044: BBOX=5900000,120000,6500000,1000000
## Working bounding box parameter for 3044: BBOX=1475000,30000,1625000,250000

##-1877994.66 3932281.56
##836715.13 9440581.95
    
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
    
