import { getRepositories } from "$lib/api";
import type { IndexPayload } from "$lib/payloads/index.payload";

/** @type {import('./$types').PageServerLoad} */
export async function load(): Promise<IndexPayload> {
	const repositories = await getRepositories();
	return {
		repositories
	};
}
