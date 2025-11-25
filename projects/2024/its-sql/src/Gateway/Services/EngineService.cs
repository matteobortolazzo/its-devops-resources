namespace Gateway.Services;

public class EngineService(
    IHttpClientFactory httpClientFactory,
    DockerService dockerService)
{
    public HttpClient GetClient(string partitionKeyValue)
    {
        var httpClient = httpClientFactory.CreateClient();
        var containerName = DockerService.GetEngineContainerName(partitionKeyValue);
        httpClient.BaseAddress = new Uri($"http://{containerName}:8080");
        return httpClient;
    }
}