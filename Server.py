from concurrent import futures
import time
import grpc

import array_pb2
import array_pb2_grpc

advs = []

class Board(array_pb2_grpc.BoardServicer):
    def AddAdvert(self, request, context):
        advs.append(array_pb2.Advert(title=request.title if len(request.title) > 0 else "*none*",
                                     text=request.text if len(request.text) > 0 else "*none*",
                                     userName=request.userName if len(request.userName) > 0 else "*none*",
                                     userEmail=request.userEmail if len(request.userEmail) > 0 else "*none*",
                                     createdTime=request.createdTime if len(request.createdTime) > 0 else "*none*"))

        return array_pb2.AddAdvertReply(message="%s\nAdvert %s was created from %s on %s" % (
            len(advs), request.title, request.userName, request.createdTime))

    def GetCountOfAdverts(self, request, context):
        return array_pb2.GetCountOfAdvertsReply(count=len(advs))

    def GetAdverts(self, request, context):
        return array_pb2.GetAdvertsReply(adverts=advs)

    def ClearAdverts(self, request, context):
        count = len(advs)
        advs.clear()
        return array_pb2.ClearReply(count = count)

def serv():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    array_pb2_grpc.add_BoardServicer_to_server(Board(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    time.sleep(60 * 60 * 24)


if __name__ == '__main__':
    serv()
