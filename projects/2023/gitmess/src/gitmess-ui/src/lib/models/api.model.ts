export interface GitTree {
	type: 'blob' | 'tree';
	name: string;
}


export interface GetTreeResponse {
	tree?: GitTree[];
	content?: string;
}

export interface GitRepository {
	name: string;
}
