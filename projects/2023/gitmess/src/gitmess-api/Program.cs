using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Web;

string GetPath(string path) =>
    Path.Combine("/data/git/repositories", path);

GitTree GetTree(string line)
{
    line = Regex.Replace(line, @"\s+", " ");
    var parts = line.Split(' ');
    return new GitTree(parts[1], parts[3]);
}

GitTree[] GetTrees(string path, string branch)
{
    var output = RunGitCommand($"ls-tree {branch}", path);
    return output
        .Split("\n")
        .Where(line => !string.IsNullOrEmpty(line))
        .Select(GetTree)
        .OrderByDescending(item => item.Type)
        .ThenBy(item => item.Name)
        .ToArray();
}

string RunGitCommand(string arguments, string workingDirectory)
{
    var processStartInfo = new ProcessStartInfo
    {
        FileName = "git",
        Arguments = arguments,
        RedirectStandardOutput = true,
        RedirectStandardError = true,
        UseShellExecute = false,
        CreateNoWindow = true,
        WorkingDirectory = workingDirectory
    };

    using var process = new Process { StartInfo = processStartInfo };
    process.Start();

    var output = process.StandardOutput.ReadToEnd();
    var error = process.StandardError.ReadToEnd();
    process.WaitForExit();

    return string.IsNullOrEmpty(error) ? output : error;
}

const string CorsPolicy = "_allowAny";
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddCors(options =>
{
    options.AddPolicy(CorsPolicy, builder => builder
        .AllowAnyOrigin()
        .AllowAnyMethod()
        .AllowAnyHeader());
});

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();

app.UseCors(CorsPolicy);
app.UseHttpsRedirection();

// Endpoints
var group = app.MapGroup("repositories");
group.MapGet("/", () =>
{
    return Directory.GetDirectories(GetPath(""))
        .Select(dir => new GitRepository(Path.GetFileName(dir)));
});
group.MapGet("/{repo}/tree/{branch}/{path?}", (string repo, string branch = "main", string? path = null) =>
{
    path = HttpUtility.UrlDecode(path);

    var repoPath = GetPath(repo);

    RunGitCommand($"checkout {branch}", repoPath);

    var isRepo = string.IsNullOrWhiteSpace(path);
    if (isRepo)
    {
        var repoItems = GetTrees(repoPath, branch);
        return new GetTreeResponse(repoItems, null);
    }

    var currentPath = GetPath(Path.Combine(repo, path!));
    var currentLine = RunGitCommand($"ls-tree {branch} {path}", repoPath);
    var currentTree = GetTree(currentLine);

    var content = currentTree.Type == "blob" ? RunGitCommand($"show {branch}:{path}", repoPath) : null;
    var items = currentTree.Type == "tree" ? GetTrees(currentPath, branch) : null;
    return new GetTreeResponse(items, content);
});
group.MapPost("/{repo}", (string repo) =>
{
    Directory.CreateDirectory(GetPath(repo));
    RunGitCommand("init", GetPath(repo));
});

app.Run();

record GitRepository(string Name);
record GetTreeResponse(GitTree[]? Tree, string? Content);
record GitTree(string Type, string Name);
