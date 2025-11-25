using System.Text.Json;
using System.Text.Json.Nodes;
using Engine.Services;
using Microsoft.AspNetCore.Mvc;
using Shared;

namespace Engine.Features;

public static class QueryUseCase
{
    public static RouteGroupBuilder MapQueryContainer(this RouteGroupBuilder containerEndpoints)
    {
        containerEndpoints.MapPost("/query", async (
                QueryExecutor queryExecutor,
                [FromRoute] string container,
                [FromBody] Node ast) =>
            {
                var containerPath = PathHelper.GetContainerPath(container);
                var tasks = Directory.GetFiles(containerPath)
                    .Select(async fileName =>
                    {
                        var content = await File.ReadAllTextAsync(fileName);
                        return JsonSerializer.Deserialize<JsonObject>(content);
                    });
                var results = await Task.WhenAll(tasks);
                if (results.Length == 0)
                {
                    return TypedResults.Ok(Array.Empty<JsonObject>());
                }

                var result = queryExecutor.Filter(results, ast);
                return (IResult)TypedResults.Ok(result);
            })
            .WithName("Query");

        return containerEndpoints;
    }
}