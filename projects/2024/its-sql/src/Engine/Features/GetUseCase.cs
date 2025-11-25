using System.Net;
using Engine.Services;
using Microsoft.AspNetCore.Mvc;

namespace Engine.Features;

public static class GetUseCase
{
    public static RouteGroupBuilder MapGetDocument(this RouteGroupBuilder containerEndpoints)
    {
        containerEndpoints.MapGet("{documentId}", async (
                HttpContext httpContext,
                [FromRoute] string container,
                [FromRoute] string documentId) =>
            {
                var documentPath = PathHelper.GetDocumentPath(container, documentId);
                if (File.Exists(documentPath))
                {
                    return (IResult)TypedResults.NotFound();
                }

                httpContext.Response.StatusCode = (int)HttpStatusCode.OK;
                httpContext.Response.ContentType = "application/json";
                await using var fileStream = new FileStream(documentPath, FileMode.Open, FileAccess.Read);
                await fileStream.CopyToAsync(httpContext.Response.Body);
                return TypedResults.Empty;
            })
            .WithName("GetDocument");

        return containerEndpoints;
    }
}