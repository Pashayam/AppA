from flask import Flask
from flask_graphql import GraphQLView
import graphene
import grpc
import data_pb2
import data_pb2_grpc

app = Flask(__name__)


class Query(graphene.ObjectType):
    phone = graphene.String(number=graphene.String(default_value=""))
    key = graphene.String(code=graphene.String(default_value=""))

    def resolve_key(self, info, code):
        if code == "143":
            return "true"
        else:
            return "false"


    def resolve_phone(self, info, number):
        channel = grpc.insecure_channel('localhost:8080')
        stub = data_pb2_grpc.DataNumberStub(channel)
        result = data_pb2.Text(data=number)
        response = stub.getPhoneNumber(result)
        print(response.data)
        return response.data





schema = graphene.Schema(query=Query)


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

if __name__ == '__main__':
    app.run()
