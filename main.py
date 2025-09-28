import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.schema import schema

app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the GraphQL API. Access the GraphQL playground at /graphql"}