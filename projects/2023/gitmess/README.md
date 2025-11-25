# GitMess

## Services

- API: https://localhost:5001
- UI: https://localhost:5001
- Git: ssh://localhost:2222

## How to run

1. Start services
```bash
docker compose up`
```

2. Create repo in server

Go to `https://localhost:5001` and use POST `/repository/{name}` to create a new repository. 

3. Set the remote on an existing repo

```bash
git remote add origin ssh://gituser@localhost:2222/data/git/repositories/{name}
git push origin main
```

4. Check on app

Go to `https://localhost:3001` from browser

## Run locally

1. Create folder

```bash
sudo mkdir -p /data/git/repositories
```

2. Allow user to change folder
```bash
sudo chown -R $USER:$USER /data/git/repositories
```

3. Run API

```bash
dotnet restore
dotnet watch --urls=http://localhost:5001
```

4. Run UI 

Change API_URL in `api.ts`.

```bash
npm run dev
```
