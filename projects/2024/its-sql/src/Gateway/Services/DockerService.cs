using System.Security.Cryptography;
using System.Text;
using Docker.DotNet;
using Docker.DotNet.Models;

namespace Gateway.Services;

public class DockerService(
    DockerClient dockerClient,
    ILogger<DockerService> logger)
{
    public async Task StartEngineContainerAsync(string partitionKeyValue)
    {
        var partitionKeyValueHash = GetHash(partitionKeyValue);
        var containerName = GetEngineContainerName(partitionKeyValue);

        var allContainer = await dockerClient.Containers.ListContainersAsync(new ContainersListParameters());
        if (allContainer.Any(container => container.Names[0] == $"/{containerName}"))
        {
            return;
        }

        var volumeName = $"ddsql_engine_{partitionKeyValueHash}_data";

        var allVolumes = await dockerClient.Volumes.ListAsync();
        if (allVolumes.Volumes.All(volume => volume.Name != volumeName))
        {
            var volumeResponse = await dockerClient.Volumes.CreateAsync(new VolumesCreateParameters
            {
                Name = volumeName
            });
            logger.LogInformation("Volume {VolumeName} created at {MountPoint}", 
                partitionKeyValueHash,
                volumeResponse.Mountpoint);
        }

        var containerResponse = await dockerClient.Containers.CreateContainerAsync(new CreateContainerParameters
        {
            Image = "ddsql_engine",
            Name = containerName,
            HostConfig = new HostConfig
            {
                AutoRemove = true,
                Binds = new List<string>
                {
                    $"{volumeName}:/etc/data"
                }
            },
            NetworkingConfig = new NetworkingConfig
            {
                EndpointsConfig = new Dictionary<string, EndpointSettings>
                {
                    {
                        "ddsql_network", new EndpointSettings()
                    }
                }
            },
            Volumes = new Dictionary<string, EmptyStruct>
            {
                { volumeName, new EmptyStruct() }
            },
            User = "root"
        });

        logger.LogInformation("Container {ContainerName} created: {ContainerId}", partitionKeyValueHash,
            containerResponse.ID);

        await dockerClient.Containers.StartContainerAsync(containerResponse.ID, null);
        logger.LogInformation("Container {ContainerName} started", partitionKeyValueHash);
        await Task.Delay(2000);
    }

    public static string GetEngineContainerName(string partitionKeyValue) =>
        $"ddsql_engine_{GetHash(partitionKeyValue)}";

    private static int GetHash(string input)
    {
        var bytes = Encoding.UTF8.GetBytes(input);
        var hash = SHA256.HashData(bytes);
        return BitConverter.ToInt32(hash) & 0x7FFFFFFF; // Ensure positive only
    }
}