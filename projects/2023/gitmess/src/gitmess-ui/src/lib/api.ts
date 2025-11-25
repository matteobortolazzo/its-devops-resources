import type { GetTreeResponse, GitRepository } from "./models/api.model";

//const API_URL = 'http://localhost:8080';
const API_URL = 'http://gitmess-api:8080';

export async function getRepositories(): Promise<GitRepository[]> {
	const response = await fetch(`${API_URL}/repositories`);
	return await response.json();
}

export async function getRepositoryTree(repo: string, branch: string, path: string | null): Promise<GetTreeResponse> {
	let url = `${API_URL}/repositories/${repo}/tree/${branch}`;
	if (path && path.length > 0) {
		url = `${url}/${path}`;
	}
	const response = await fetch(url);
	return await response.json();
}
