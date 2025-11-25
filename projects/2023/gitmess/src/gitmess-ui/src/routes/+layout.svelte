<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';

	// Highlight JS
	import hljs from 'highlight.js/lib/core';
	import 'highlight.js/styles/github-dark.css';
	import { storeHighlightJs } from '@skeletonlabs/skeleton';
	import xml from 'highlight.js/lib/languages/xml'; // for HTML
	import css from 'highlight.js/lib/languages/css';
	import javascript from 'highlight.js/lib/languages/javascript';
	import typescript from 'highlight.js/lib/languages/typescript';
	import markdown from 'highlight.js/lib/languages/markdown';
	import csharp from 'highlight.js/lib/languages/csharp';
	import yaml from 'highlight.js/lib/languages/yaml';

	hljs.registerLanguage('xml', xml); // for HTML
	hljs.registerLanguage('css', css);
	hljs.registerLanguage('js', javascript);
	hljs.registerLanguage('ts', typescript);
	hljs.registerLanguage('md', markdown);
	hljs.registerLanguage('cs', csharp);
	hljs.registerLanguage('yml', yaml);
	hljs.registerLanguage('yaml', yaml);
	storeHighlightJs.set(hljs);

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<a href="/">
				<strong class="text-xl uppercase">GitMess</strong>
			</a>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<div class="max-w-2xl mx-auto pt-8">
		<slot />
	</div>
</AppShell>
