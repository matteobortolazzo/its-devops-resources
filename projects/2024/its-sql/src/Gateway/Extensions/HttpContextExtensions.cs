namespace Gateway.Extensions;

public static class HttpContextExtensions
{
    public static async Task<IResult> ProxyAsync(this HttpContext httpContext, HttpResponseMessage response)
    {
        httpContext.Response.StatusCode = (int)response.StatusCode;
        httpContext.Response.ContentType = response.Content.Headers.ContentType?.ToString();
        await response.Content.CopyToAsync(httpContext.Response.Body);
        return TypedResults.Empty;
    }
}