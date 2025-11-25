<script lang="ts">
	import type { IndexPayload } from '$lib/payloads/index.payload';

	export let data: IndexPayload;
</script>

<div class="card p-4">
	<header>
		<h3 class="h3">Repos</h3>
	</header>
	<article class="mt-4">
		<nav class="list-nav">
			<ul>
				{#each data.repositories as repository}
					<li>
						<a href="/repositories/{repository.name}/tree/main">
							<span class="badge">📁</span>
							<span class="flex-auto">{repository.name}</span>
						</a>
					</li>
				{/each}
			</ul>
		</nav>
	</article>
</div>
