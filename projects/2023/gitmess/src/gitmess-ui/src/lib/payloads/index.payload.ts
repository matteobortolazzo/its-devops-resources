import type { GitRepository } from "$lib/models/api.model";

export interface IndexPayload {
	repositories: GitRepository[];
}
