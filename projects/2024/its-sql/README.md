# Distributed Document SQL

## Introduction

This is a example of distributed `JSON` document database using a SQL-like query language created during a school lesson.

It takes inspiration from `CosmosDB`. There are containers, and containers have documents.
The distribution is achieved by using a partition key to split the data between different engines.

Everything run locally using `Docker` and `Docker Compose` so it's not actually distributed in the current state.

The project is divided in two main components:
- `Gateway`
- `Engine`

### Engine

- Responsible to store and query the data.
- One for each partition key value (independently of container)
- Each engine has a volume mounted to store the data
- Hidden from the clients

### Gateway

- Responsible to route the requests to the correct engine
- Creates engine containers when needed
- Exposed to the clients
- Use SQLite to store container metadata

## Run the project

From the root of the project, run the following commands:

```bash
docker build -t ddsql_engine -f src/Engine/Dockerfile  .      
docker compose up
```

The `Gateway` will be available at `http://localhost:8080`.

The `OpenAPI` definition can be found at [/openapi/v1.json](http://localhost:8080/openapi/v1.json) and
a `Swagger UI` at [/swagger](http://localhost:8080/swagger).

## Key takeaways

### API structures

Both projects are `NET9` *minimal API*. The use extension methods for `RouteGroupBuilder` to split the logic in different files, and to take ruoting more readable:

```csharp
app.MapGroup("containers")
    .MapCreateContainer()
    .MapGetContainers()
    .MapQueryContainer();

app.MapGroup("containers/{container}/documents")
    .MapUpsertDocument()
    .MapGetDocument();
```

### Query parser

The query is converted to an *AST* (Abstract Syntax Tree) so that:
- The `Gateway` can extract the partition key value from the query
- The `Engine` can execute the query

The gateway, after finding the partition key value, send the *AST* to the correct execute it.

### Proxy code

The `Gateway` uses `HttpClient` to communicate with the `Engine`. 
The `Gateway` doesn't need to deserialize the answer, so it write the response stream directly to the client.

```csharp
public static async Task<IResult> ProxyAsync(this HttpContext httpContext, HttpResponseMessage response)
{
    httpContext.Response.StatusCode = (int)response.StatusCode;
    httpContext.Response.ContentType = response.Content.Headers.ContentType?.ToString();
    await response.Content.CopyToAsync(httpContext.Response.Body);
    return TypedResults.Empty;
}
```

### Hashing

It uses `SHA256` to hash the partition key value and used to find the correct engine.