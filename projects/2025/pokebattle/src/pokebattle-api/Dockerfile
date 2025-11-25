
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /source

# copy everything else and build app
COPY . .
RUN dotnet test .
RUN dotnet publish -c release -o /app ./pokebattle-api.ApiService

# final stage/image
FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
ENV ASPNETCORE_URLS=http://+:80
COPY --from=build /app ./
EXPOSE 80
ENTRYPOINT ["dotnet", "PokeBattle.ApiService.dll"]
