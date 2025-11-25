<script lang="ts">
	import type { GitTree } from '$lib/models/api.model';

	export let tree: GitTree[];
	export let url: string;
</script>

<div class="table-container">
	<table class="table table-hover">
		<thead>
			<tr>
				<th></th>
				<th>Name</th>
			</tr>
		</thead>
		<tbody>
			{#each tree as row}
				<tr>
					<td>{row.type === 'tree' ? '📁' : '📄'}</td>
					<td><a href={`${url}/${row.name}`}>{row.name}</a></td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>
