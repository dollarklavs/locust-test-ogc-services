from locust import HttpLocust, TaskSet, task
from operator import itemgetter

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
                "typeNames":"am:AManagementRestrictionOrRegulationZone",
                "BBOX":"" 
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
            self.request_am_pmpa_inspire["BBOX"] = bbox
            self.client.post("", self.request_am_pmpa_inspire)
    
        
        
    @task(2)    
    def post_to_wfs_aadp(self):
            self.client.post("", self.request_am_pmpa_inspire)


    
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 900
    
    
# http://load191.kmsext.dk:8081/havvind/ows?service=WFS&version=1.1.0&request=GetFeature&typeName=havvind:AabenDoerAnsoegningsomraade&outputFormat=gml32&maxFeatures=50
# {"service":"WFS", "version":"2.0.0", "request":"GetFeature", "typeName":"havvind:AabenDoerAnsoegningsomraade", "outputFormat":"gml32"}