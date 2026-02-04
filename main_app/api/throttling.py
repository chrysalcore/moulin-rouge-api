from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class CourseThrottle(AnonRateThrottle):
    scope = "courses_rate"
    
class CommentThrottle(UserRateThrottle):
    scope = "comments_rate"

class AddThrottle(UserRateThrottle):
    scope = "add_rate"
    
class ListThrottle(AnonRateThrottle):
    scope = "list_rate"

class DetailThrottle(UserRateThrottle):
    scope = "detail_rate"