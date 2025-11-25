<script lang="ts">
	import { page } from '$app/stores';
	import type { RepoPayload } from '$lib/payloads/repo.payload';
	import GitDirectory from '$lib/components/GitDirectory.svelte';
	import { CodeBlock } from '@skeletonlabs/skeleton';

	export let data: RepoPayload;
</script>

<div class="card p-4">
	<header>
		<h3 class="h3">{$page.params.repo}</h3>
		<h4 class="h4">{$page.params.branch}</h4>
	</header>

	<article class="mt-4">
		{#if data.response.tree}
			<GitDirectory url={$page.url.toString()} tree={data.response.tree} />
		{/if}
		{#if data.response.content}
			<CodeBlock language="ts" code={data.response.content}></CodeBlock>
		{/if}
	</article>
</div>
