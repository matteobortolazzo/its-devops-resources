using Gateway.Services;
using Microsoft.AspNetCore.Mvc;

namespace Gateway.Features.Containers;

[Serializable]
public record CreateContainerRequest(string Container, string PartitionKeyPath);

public static class ContainerCreateUseCase
{
    public static RouteGroupBuilder MapCreateContainer(this RouteGroupBuilder containerEndpoints)
    {
        containerEndpoints.MapPost("/", async (
            ContainerService containerService,
            [FromBody] CreateContainerRequest request) =>
        {
            await containerService.CreateContainerAsync(request.Container, request.PartitionKeyPath);
            return TypedResults.Created();
        });
            
        return containerEndpoints;
    }
}