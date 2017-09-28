from datetime import datetime
from . import models


# class CheckSessionMiddleware():
#
#     def process_request(request):
#         try:
#             sessid = request.COOKIE.get('sessid')
#             session = models.Session.objects.get(
#                 key=sessid,
#                 expires__gt=datetime.now(),
#             )
#             request.session = session
#             request.user = session.user
#         except models.Session.DoesNotExist:
#             request.session = None
#             request.user = None
