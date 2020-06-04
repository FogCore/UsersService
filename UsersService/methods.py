import bcrypt
from pymongo import MongoClient
from UsersService import users_service_pb2, users_service_pb2_grpc


class UsersAPI(users_service_pb2_grpc.UsersAPIServicer):
    client = MongoClient('mongodb://users_service:users_service_pwd@UsersServiceDB:27017/users_service')
    db = client.users_service
    users_collection = db.users

    # Checks the existence of a user with the specified username
    def IsExist(self, request, context):
        if request.username:
            user = self.users_collection.find_one({'username': request.username})
            if user:
                return users_service_pb2.Response(code=200, message='An account with this username already exists.')
            else:
                return users_service_pb2.Response(code=404, message='An account with this username not found.')
        else:
            return users_service_pb2.Response(code=422, message='Username parameter is missing.')

    # Creates a new user
    def Create(self, request, context):
        if request.first_name and request.last_name and request.username and request.password:
            if self.users_collection.find_one({'username': request.username}):
                status = users_service_pb2.Response(code=409, message="That username is taken. Please choose a different one.")
                return users_service_pb2.ResponseWithUser(status=status)
            else:
                hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user = {'first_name': request.first_name,
                        'last_name': request.last_name,
                        'username': request.username,
                        'password': hashed_password,
                        'admin': False}
                self.users_collection.insert_one(user)
                status = users_service_pb2.Response(code=201, message="User account has been created successfully.")
                data = users_service_pb2.User(username=user['username'],
                                              first_name=user['first_name'],
                                              last_name=user['last_name'],
                                              admin=user['admin'])
                return users_service_pb2.ResponseWithUser(status=status, user=data)
        else:
            status = users_service_pb2.Response(code=422, message='First name, last name, username and password parameters are required.')
            return users_service_pb2.ResponseWithUser(status=status)

    # Verifies username and password
    def Verify(self, request, context):
        if request.username and request.password:
            user = self.users_collection.find_one({'username': request.username})
            if user and bcrypt.checkpw(request.password.encode('utf-8'), user['password'].encode('utf-8')):
                status = users_service_pb2.Response(code=200, message="Username and password are correct.")
                data = users_service_pb2.User(username=user['username'],
                                              first_name=user['first_name'],
                                              last_name=user['last_name'],
                                              admin=user['admin'])
                return users_service_pb2.ResponseWithUser(status=status, user=data)
            else:
                status = users_service_pb2.Response(code=401, message="Incorrect username or password.")
                return users_service_pb2.ResponseWithUser(status=status)
        else:
            status = users_service_pb2.Response(code=422, message="Username and password parameters are required.")
            return users_service_pb2.ResponseWithUser(status=status)

    # Returns information about the user
    def Info(self, request, context):
        if request.username:
            user = self.users_collection.find_one({'username': request.username})
            if user:
                status = users_service_pb2.Response(code=200, message="User with this username exists.")
                data = users_service_pb2.User(first_name=user['first_name'],
                                              last_name=user['last_name'],
                                              username=user['username'],
                                              admin=user['admin'])
                return users_service_pb2.ResponseWithUser(status=status, user=data)
            else:
                status = users_service_pb2.Response(code=404, message="User with this username not found.")
                return users_service_pb2.ResponseWithUser(status=status)
        else:
            status = users_service_pb2.Response(code=422, message="Username parameter is required.")
            return users_service_pb2.ResponseWithUser(status=status)
