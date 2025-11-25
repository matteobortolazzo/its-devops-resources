using System.Net;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using Gateway.Extensions;
using Gateway.Services;
using Microsoft.AspNetCore.Mvc;

namespace Gateway.Features.Documents;

public static class DocumentUpsertUseCase
{
    public static RouteGroupBuilder MapUpsertDocument(this RouteGroupBuilder documentEndpoints)
    {
        documentEndpoints.MapPut("/", async (
                HttpContext httpContext,
                DockerService dockerService,
                EngineService engineService,
                ContainerService containerService,
                [FromRoute] string container,
                [FromBody] JsonObject document) =>
            {
                var partitionKeyPath = await containerService.GetPartitionKeyPathAsync(container);
                if (partitionKeyPath == null)
                {
                    return TypedResults.Problem(
                        statusCode: (int)HttpStatusCode.NotFound,
                        title: "Container not found");
                }

                var partitionKeyValue = document[partitionKeyPath!]!.GetValue<string>();

                await dockerService.StartEngineContainerAsync(partitionKeyValue);

                var body = JsonSerializer.Serialize(document);
                var content = new StringContent(body, Encoding.UTF8, "application/json");
                var response = await engineService.GetClient(partitionKeyValue).PutAsync(container, content);
                return await httpContext.ProxyAsync(response);
            })
            .WithName("UpsertDocument");

        return documentEndpoints;
    }
}