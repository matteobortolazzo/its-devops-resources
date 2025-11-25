FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build-env
WORKDIR /App

# Copy everything
COPY . ./

# Restore and build
RUN dotnet restore
RUN dotnet publish -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /App
COPY --from=build-env /App/out .

# Create volume for repositories
VOLUME /data/git/repositories

# Create a user that can write on the volume
RUN useradd -m apiuser -u 1001
RUN mkdir /data && mkdir /data/git/ && mkdir /data/git/repositories/ 
RUN chown -R 1001:1001 /data/git/repositories

# Install git
RUN apt-get update && apt-get install -y git

# Start API
USER apiuser
EXPOSE 8080
ENTRYPOINT ["dotnet", "GitMess.Api.dll"]
