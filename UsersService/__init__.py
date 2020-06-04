import grpc
from concurrent import futures
from UsersService.methods import UsersAPI
from UsersService import users_service_pb2_grpc

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
users_service_pb2_grpc.add_UsersAPIServicer_to_server(UsersAPI(), server)
server.add_insecure_port('[::]:50050')
