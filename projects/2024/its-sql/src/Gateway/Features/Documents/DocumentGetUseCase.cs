using System.Net;
using System.Text.Json.Nodes;
using Gateway.Extensions;
using Gateway.Services;
using Microsoft.AspNetCore.Mvc;

namespace Gateway.Features.Documents;

public static class DocumentGetUseCase
{
    public static RouteGroupBuilder MapGetDocument(this RouteGroupBuilder documentEndpoints)
    {
        documentEndpoints.MapGet("{documentId}", async (
                HttpContext httpContext,
                DockerService dockerService,
                EngineService engineService,
                ContainerService containerService,
                [FromRoute] string container,
                [FromRoute] string documentId,
                [FromQuery] string partitionKeyValue) =>
            {
                var partitionKeyPath = await containerService.GetPartitionKeyPathAsync(container);
                if (partitionKeyPath == null)
                {
                    return TypedResults.Problem(
                        statusCode: (int)HttpStatusCode.NotFound,
                        title: "Container not found");
                }

                await dockerService.StartEngineContainerAsync(partitionKeyValue);

                var response = await engineService.GetClient(partitionKeyValue)
                    .GetAsync($"{container}/{documentId}");
                return await httpContext.ProxyAsync(response);
            })
            .WithName("GetDocument");

        return documentEndpoints;
    }
}