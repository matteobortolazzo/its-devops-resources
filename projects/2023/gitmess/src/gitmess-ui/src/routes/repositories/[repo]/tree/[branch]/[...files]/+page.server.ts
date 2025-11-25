
import { getRepositoryTree } from "$lib/api";
import type { RepoPayload } from "$lib/payloads/repo.payload";

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }): Promise<RepoPayload> {
  const path = encodeURIComponent(params.files);
  const response = await getRepositoryTree(params.repo, params.branch, path);
  return {
    response
  };
}
