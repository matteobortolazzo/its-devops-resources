using Microsoft.Data.Sqlite;

namespace Gateway.Services;

[Serializable]
public record ContainerListDto(string Name, string PartitionKeyPath);

public class ContainerService(ILogger<ContainerService> logger)
{
    private const string ConnectionString = "Data Source=/etc/data/gateway.db";

    private const string CreateTableQuery = @"
                CREATE TABLE IF NOT EXISTS Containers (
                    Name TEXT PRIMARY KEY,
                    PartitionKeyPath TEXT NOT NULL
                );
                ";

    private const string InsertContainerQuery = @"
                INSERT INTO Containers (Name, PartitionKeyPath)
                VALUES ($name, $partitionKeyPath);
                ";

    private const string GetPartitionKeyPathQuery = @"
                SELECT PartitionKeyPath
                FROM Containers
                WHERE Name = $container;
                ";

    public async Task EnsureDatabaseExistsAsync()
    {
        await using var connection = new SqliteConnection(ConnectionString);
        connection.Open();


        await using var command = new SqliteCommand(CreateTableQuery, connection);
        command.ExecuteNonQuery();

        logger.LogInformation("Ensure database exists");
    }

    public async Task CreateContainerAsync(string name, string partitionKeyPath)
    {
        await using var connection = new SqliteConnection(ConnectionString);
        connection.Open();

        await using var command = new SqliteCommand(InsertContainerQuery, connection);
        command.Parameters.AddWithValue("$name", name);
        command.Parameters.AddWithValue("$partitionKeyPath", partitionKeyPath);
        await command.ExecuteNonQueryAsync();
    }

    public async Task<ContainerListDto[]> GetContainersAsync()
    {
        await using var connection = new SqliteConnection(ConnectionString);
        connection.Open();

        await using var command = new SqliteCommand("SELECT Name, PartitionKeyPath FROM Containers", connection);

        var containers = new List<ContainerListDto>();

        await using var reader = await command.ExecuteReaderAsync();
        while (reader.Read())
        {
            var name = reader.GetString(0);
            var partitionKeyPath = reader.GetString(1);
            containers.Add(new ContainerListDto(name, partitionKeyPath));
        }

        return containers.ToArray();
    }

    public async Task<string?> GetPartitionKeyPathAsync(string container)
    {
        await using var connection = new SqliteConnection(ConnectionString);
        connection.Open();

        await using var command = new SqliteCommand(GetPartitionKeyPathQuery, connection);
        command.Parameters.AddWithValue("$container", container);
        return (string?)await command.ExecuteScalarAsync();
    }
}