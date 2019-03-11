# koer fra cml som fx: locust -f C:\Users\b031513\Documents\locust_tests\haeldnings_wms.py --host=http://kmsload106.kmsext.dk/cgi-bin/mapserv-7.fcgi

from locust import HttpLocust, TaskSet, task
from operator import itemgetter
import time
import random

INPUT_BBOX = (650000,6180000,650500,6180500)
INTERVAL = 10
DISTANCE = 750

class UserBehavior(TaskSet):
    input_bbox = (650000,6180000,650500,6180500) # start bbox
    # dictionary of valid key value pairs sent as a POST to the host
    request_haeld = {
                "service":"WMS", 
                "version":"1.3.0",
                "CRS":"EPSG:25832",
                "request":"GetMap",
                "BBOX":"",
                "map":"/data4/mapserver/data/_maps_jolni/pgv_haeldningsdata.map",
                "LAYERS":"pgv_haeldningsdata_2018a",
                "FORMAT":"image/png",
                "WIDTH":"500",
                "HEIGHT":"500"
              }              


# decorator task(weight), define the weight of the function              
    @task(1)
    def post_to_service(self):
    
        def pan(bbox, interval, request, distance, axis='EW', reverse=False):
            """simulates a user panning across a OGC service that supports BBOX queries.
            """
            direction = ['ll_x','ur_x'] if axis == 'EW' else ['ll_y','ur_y']
            distance = -(distance + 1) if reverse else distance + 1
            steps = range(0, distance, interval)
            pause = random.choice([0.1, 5, 1, 1])
            print('input bbox is: {}'.format(bbox))
            bbox = {'ll_x':bbox[0], 
                    'll_y':bbox[1], 
                    'ur_x':bbox[2], 
                    'ur_y':bbox[3]}
            original_values = {pos : coord 
                           for pos, coord 
                           in bbox.items() 
                           if pos in direction}
            
            for step in steps:
                print(step)
                bbox = {pos : (original_values[pos] + step 
                               if pos in direction 
                               else coord) 
                               for pos, coord in bbox.items()}
                bbox_str = "{ll_x},{ll_y},{ur_x},{ur_y}".format(**bbox)
                request["BBOX"] = bbox_str
                resp = self.client.post("", request)
                # bbox.update(original_values)
                print(resp.request.body)
                time.sleep(pause)
                
            return bbox['ll_x'], bbox['ll_y'], bbox['ur_x'], bbox['ur_y']

        new_bbox = pan(INPUT_BBOX, 
                INTERVAL, 
                self.request_haeld, 
                DISTANCE, 
                axis='EW', 
                reverse=False)
        time.sleep(10)
        print('the 2 bbox is: {}\n\n\n\n\n'.format(new_bbox))
        new_bbox3 = pan(new_bbox, INTERVAL, self.request_haeld, DISTANCE, axis='NS', reverse=False)
        print('the 3 bbox is: {}\n\n\n\n\n'.format(new_bbox3))
        new_bbox4 = pan(new_bbox3, INTERVAL, self.request_haeld, DISTANCE, axis='EW', reverse=True)
        print('the 4 bbox is: {}\n\n\n\n\n'.format(new_bbox4))
        new_bboxl = pan(new_bbox4, INTERVAL, self.request_haeld, DISTANCE, axis='NS', reverse=True)
        print('the 1-l bbox is: {}\n\n\n\n\n'.format(new_bboxl))
    
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
    
