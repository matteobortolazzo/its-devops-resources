# Repository Guidelines
## Project Structure & Module Organization
The backend lives in `src/pokebattle-api`, a .NET Aspire solution where `pokebattle-api.AppHost` orchestrates the minimal API (`pokebattle-api.ApiService`) and the Blazor Web experience (`pokebattle-api.Web`). Angular code for the production-facing SPA resides in `src/pokebattle-ui/src`, with CLI config alongside `package.json` and build output under `dist/`. Build artifacts created in `bin/`, `obj/`, or `node_modules/` stay untracked, while environment-specific settings live in the respective `appsettings*.json` files.

## Build, Test, and Development Commands
- `dotnet restore src/pokebattle-api/pokebattle-api.sln` installs backend dependencies; run after pulling new packages.
- `dotnet build src/pokebattle-api/pokebattle-api.sln` validates all projects compile.
- `dotnet run --project src/pokebattle-api/pokebattle-api.AppHost` boots the Aspire host, wiring the API and Blazor frontend with health checks.
- `npm install` inside `src/pokebattle-ui` pulls Angular dependencies; rerun whenever `package.json` changes.
- `npm run start` serves the SPA on `http://localhost:4200`; use `npm run build` for production bundles and `npm run test` for Karma/Jasmine suites.

## Coding Style & Naming Conventions
C# code follows .NET defaults: 4-space indentation, PascalCase for types, camelCase for locals, and suffix interfaces with `I`. Keep file-scoped namespaces and favor expression-bodied members when they improve readability. TypeScript uses Angular conventions (2-space indentation, kebab-case file names, SCSS modules per component). Prefer strongly typed services, group feature modules under `src/app`, and scaffold assets with `npx ng generate` to inherit structure. Run `dotnet format` before submitting and let your IDE or the Angular language service handle TypeScript formatting.

## Testing Guidelines
Back-end tests should live alongside the solution as `*.Tests` projects using xUnit or MSTest; invoke them with `dotnet test src/pokebattle-api/pokebattle-api.sln`. Seed new feature work with minimal API integration tests centered on `HttpClient` flows or Aspire diagnostics. Angular specs belong in `*.spec.ts` files next to the component they exercise; run locally with `npm run test -- --watch` and fail builds on coverage regressions configured through `karma-coverage`. Document any manual QA steps in your pull request when automated coverage falls short.

## Commit & Pull Request Guidelines
Adopt Conventional Commits (`feat:`, `fix:`, `chore:`) and keep subjects under 72 characters. Each PR should include a concise summary, linked issue or task id, and screenshots or GIFs for visual changes. Call out noteworthy configuration changes (`appsettings*.json`, `environment.ts`) and state which commands/tests were executed. Request review once CI passes and resolve all TODOs before merging.
