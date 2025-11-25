using Engine.Features;
using Engine.Services;

var builder = WebApplication.CreateBuilder(args);
builder.Logging.ClearProviders();
builder.Logging.AddConsole();

builder.Services.AddSingleton<QueryExecutor>();

var app = builder.Build();

app.MapGroup("{container}")
    .MapGetDocument()
    .MapUpsertDocument()
    .MapQueryContainer();

app.Run();