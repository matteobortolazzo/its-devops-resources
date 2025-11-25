using System.Net;
using System.Text.Json.Nodes;
using Gateway.Extensions;
using Gateway.Interpreter;
using Gateway.Services;
using Microsoft.AspNetCore.Mvc;
using Shared;

namespace Gateway.Features.Containers;

[Serializable]
public record SqlRequest(string Sql);

public static class ContainerQueryUseCase
{
    public static RouteGroupBuilder MapQueryContainer(this RouteGroupBuilder containerEndpoints)
    {
        containerEndpoints.MapPost("/{container}/query", async (
                HttpContext httpContext,
                DockerService dockerService,
                EngineService engineService,
                ContainerService containerService,
                QueryService queryService,
                Parser parser,
                [FromRoute] string container,
                [FromBody] SqlRequest request) =>
            {
                var partitionKeyPath = await containerService.GetPartitionKeyPathAsync(container);
                if (partitionKeyPath == null)
                {
                    return TypedResults.Problem(
                        statusCode: (int)HttpStatusCode.NotFound,
                        title: "Container not found");
                }

                Node ast;
                try
                {
                    ast = parser.Parse(request.Sql);
                }
                catch (Exception e)
                {
                    return TypedResults.Problem(
                        statusCode: (int)HttpStatusCode.BadRequest,
                        title: e.Message);
                }
                
                var partitionKeyValue = queryService.GetPartitionKeyValue(ast, partitionKeyPath!);
                if (partitionKeyValue == null)
                {
                    return TypedResults.Problem(
                        statusCode: (int)HttpStatusCode.BadRequest,
                        title: "WHERE clause must contain partition key");
                }

                // TODO: Remove the partition key filter from AST, as it's not needed by the engine
                
                await dockerService.StartEngineContainerAsync(partitionKeyValue);

                var response = await engineService.GetClient(partitionKeyValue)
                    .PostAsJsonAsync($"{container}/query", ast);
                return await httpContext.ProxyAsync(response);
            })
            .WithName("Query");

        return containerEndpoints;
    }
}