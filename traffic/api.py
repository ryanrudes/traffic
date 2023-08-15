from .event import Event, Schedule
from .weather import RoadCondition
from .roadway import Roadway
from .camera import Camera
from .alert import Alert
from .sign import Sign

import requests

class API:
    def __init__(self, key: str):
        self.key = key
        
    def get_events(self) -> [Event]:
        """Returns all event types."""
        json = self.request("getevents")
        events = []
        
        for data in json:
            schedule = Schedule(
                id = data["Schedule"]["ScheduleId"],
                start = data["Schedule"]["Start"],
                end = data["Schedule"]["End"],
                continuous = data["Schedule"]["Continuous"],
                active_days = data["Schedule"]["ActiveDays"],
            )
            
            event = Event(
                id = data["ID"],
                region = data["RegionName"],
                county = data["CountyName"],
                severity = data["Severity"],
                roadway = data["RoadwayName"],
                direction = data["DirectionOfTravel"],
                description = data["Description"],
                location = data["Location"],
                lanes_affected = data["LanesAffected"],
                lanes_status = data["LanesStatus"],
                navteq_id = data["NavteqLinkId"],
                start_location = data["PrimaryLocation"],
                end_location = data["SecondaryLocation"],
                start_city = data["FirstArticleCity"],
                end_city = data["SecondCity"],
                event_type = data["EventType"],
                event_subtype = data["EventSubType"],
                polyline = data["MapEncodedPolyline"],
                last_updated = data["LastUpdated"],
                latitude = data["Latitude"],
                longitude = data["Longitude"],
                start_date = data["StartDate"],
                end_date = data["PlannedEndDate"],
                reported = data["Reported"],
                schedule = schedule,
            )
            
            events.append(event)
            
        return events

    def get_roadways(self) -> [Roadway]:
        """Returns all roadway names."""
        json = self.request("getroadways")
        roadways = []
        
        for data in json:
            roadway = Roadway(
                name = data["RoadwayName"],
                sort_order = data["SortOrder"],
            )
            
            roadways.append(roadway)
            
        return roadways

    def get_cameras(self) -> [Camera]:
        """Returns all cameras."""
        json = self.request("getcameras")
        cameras = []
        
        for data in json:
            camera = Camera(
                id = data["ID"],
                name = data["Name"],
                direction = data["DirectionOfTravel"],
                roadway = data["RoadwayName"],
                image_url = data["Url"],
                video_url = data["VideoUrl"],
                disabled = data["Disabled"],
                blocked = data["Blocked"],
                latitude = data["Latitude"],
                longitude = data["Longitude"],
            )
            
            cameras.append(camera)
            
        return cameras
    
    def get_signs(self) -> [Sign]:
        """Returns all VMS."""
        json = self.request("getmessagesigns")
        signs = []
        
        for data in json:
            sign = Sign(
                id = data["ID"],
                name = data["Name"],
                roadway = data["Roadway"],
                direction = data["DirectionOfTravel"],
                messages = data["Messages"],
                latitude = data["Latitude"],
                longitude = data["Longitude"],
            )
            
            signs.append(sign)
            
        return signs
    
    def get_alerts(self) -> [Alert]:
        """Returns all traffic alerts."""
        json = self.request("getalerts")
        alerts = []
        
        for data in json:
            alert = Alert(
                id = data["ID"],
                message = data["Message"],
                notes = data["Notes"],
                areas = data["AreaNames"],
            )
            
            alerts.append(alert)
            
        return alerts
    
    def get_road_conditions(self) -> [RoadCondition]:
        """Returns all winter road conditions."""
        json = self.request("getwinterroadconditions")
        road_conditions = []
        
        for data in json:
            road_condition = RoadCondition(
                condition = data["Condition"],
                area = data["AreaName"],
                location = data["LocationDescription"],
                roadway = data["RoadwayName"],
                polyline = data["Polyline"],
                last_updated = data["LastUpdated"]
            )
    
    def request(self, path: str):
        url = f"https://511ny.org/api/{path}?key={self.key}&format=json"
        response = requests.get(url)
        return response.json()