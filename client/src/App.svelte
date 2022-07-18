<script lang="ts">
	import get from 'axios'
	import { onMount } from 'svelte';
	import Border from './lib/Border.svelte';

	let player1Border: Border;
	let player2Border: Border;

	let clockActive = false;
	let pulling = false;

	function clockTick()
	{
		if (!pulling) {
			// Pull from the API
			pulling = true;
			get("http://127.0.0.1:8080/state")
			.then(res => {
				player1Border.updateData(res.data, 1);
				player2Border.updateData(res.data, 2);
			})
			.catch(err => {
				console.log(err);
				player1Border.updateData({waiting: true}, 1);
				player2Border.updateData({waiting: true}, 2);
			})
			.finally(() => {
				// Allow the clock to pull again
				pulling = false;
			});
		}
		
		if (clockActive) {
			window.requestAnimationFrame(clockTick);
		}
	}

	function startClock()
	{
		if (!clockActive) {
			clockActive = true;
			window.requestAnimationFrame(clockTick);
		}
	}

	function stopClock()
	{
		clockActive = false;
	}

	onMount(startClock);
</script>

<main>
	<Border flipped={false} bind:this={player1Border}/>
	<Border flipped={true}  bind:this={player2Border}/>
</main>