using System.Text.Json;
using System.Text.Json.Nodes;
using Engine.Services;
using Microsoft.AspNetCore.Mvc;

namespace Engine.Features;

public static class UpsertUseCase
{
    public static RouteGroupBuilder MapUpsertDocument(this RouteGroupBuilder containerEndpoints)
    {
        containerEndpoints.MapPut("/", async (
                [FromRoute] string container,
                [FromBody] JsonObject document) =>
            {
                var containerPath = PathHelper.GetContainerPath(container);
                if (!Directory.Exists(containerPath))
                {
                    Directory.CreateDirectory(containerPath);
                }

                var id = document["id"]!.ToString();
                var json = JsonSerializer.Serialize(document);
                await File.WriteAllTextAsync($"{containerPath}/{id}.json", json);
                return TypedResults.Ok();
            })
            .WithName("UpsertDocument");

        return containerEndpoints;
    }
}