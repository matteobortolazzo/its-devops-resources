namespace Engine.Services;

public static class PathHelper
{
    public static string GetDocumentPath(string container, string documentId) => $"{GetContainerPath(container)}/{documentId}";
    public static string GetContainerPath(string container) => $"/etc/data/{container}";
}
