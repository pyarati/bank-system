from app import api
from app.views.user import UserResources, UserResourcesId, UserTypeResource, UserTypeResourceId


api.add_resource(UserResources, '/user')
api.add_resource(UserResourcesId, '/user/<int:user_id>')
api.add_resource(UserTypeResource, '/usertype')
api.add_resource(UserTypeResourceId, '/usertype/<int:user_type_id>')
