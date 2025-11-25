using Gateway.Services;

namespace Gateway.Features.Containers;

public static class ContainerListUseCase
{
    public static RouteGroupBuilder MapGetContainers(this RouteGroupBuilder containerEndpoints)
    {
        containerEndpoints.MapGet("/", async (
            ContainerService containerService) =>
        {
            var results = await containerService.GetContainersAsync();
            return TypedResults.Ok(results);
        });

        return containerEndpoints;
    }
}