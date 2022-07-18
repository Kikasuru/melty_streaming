<script lang="ts">
	export let flipped: boolean;

	let waiting = true;
	let gameMode = 0;
	let selectMode = 0;
	let char = 0;
	let moon = 0;
	let heat = 0;

	let nameImg = '';
	let mug0Img = '';
	let mug1Img = '';
	let moonImg = '';

	export function updateData(data, player: number): void {
		// If we're still waiting for melty, don't do anything.
		if ( typeof data.waiting !== 'undefined' && data.waiting ) {
			waiting = true;
			return;
		}

		waiting = false;

		gameMode = data.gamemode;
		selectMode = data[`p${player}selmode`];
		char = data[`p${player}char`];
		moon = data[`p${player}moon`];
		heat = data[`p${player}heat`];

		// Format the character ID for images.
        let charId = char.toString().padStart(2, "0");

		nameImg = `url("assets/name/vs_name00_${charId}.png")`
		mug0Img = `url("assets/mug/cut_${charId}00.png")`
		// Only apply the second mugshot if the player is using a puppet character.
		if ( [0x04, 0x22, 0x23].includes( char ) ) mug1Img = `url("assets/mug/cut_${charId}01.png")`
		else mug1Img = 'none'
		moonImg = `url("assets/moon/moon_${moon}.png")`
	}
</script>

<main class="border" class:flipped={ flipped }>
	{#if !waiting}
		<div
			id="mugheat"
			class="heat"
			class:flipped={ flipped }
			class:heatmode={ ( heat === 1 || heat === 2 ) && gameMode === 1 }
			class:bloodheatmode={ heat === 3 && gameMode === 1 }
			style="background-image:{mug0Img}"
		></div>

		<div
			id="mugptnr"
			class="charmug partner"
			class:selected={ selectMode > 0 && [0x04, 0x22, 0x23].includes( char ) }
			style="background-image:{mug1Img}"
		></div>
		<div
			id="mug"
			class="charmug"
			class:selected={ selectMode > 0 }
			style="background-image:{mug0Img}"
		></div>

		<div id="banner" class="charnamebanner" class:selected={ selectMode > 0 }>
			<div
				id="name"
				class="charname"
				class:flipped={ flipped }
				style="background-image:{nameImg}"
			></div>
			{#if selectMode > 1}
				<div
					id="moon"
					class="charmoon"
					class:flipped={ flipped }
					class:selected={ selectMode > 1 }
					style="background-image:{moonImg}"
				></div>
			{/if}
		</div>
	{/if}
</main>

<style lang="scss">
	.border {
		position: absolute;
		width: 12.5%;
		height: 100%;
		top: 0;
		background-color: #000000;
		overflow: hidden;
		
		&.flipped {right: 0; transform: scaleX(-1);}

		.charnamebanner {
			position: absolute;
			width: 128px;
			height: 1536px;
			background-image: url("name_banner.png");
			transition: transform 0.5s;
			right: 0;
			transform: translateY(-384px);

			&.selected {transform: translateY(0px);}
		}

		.charname {
			position: absolute;
			width: 48px;
			height: 512px;
			bottom: 512px;
			right: 0;
			&.flipped {transform: scaleX(-1);}
		}

		.charmug {
			position: absolute;
			width: 900px;
			height: 1024px;
			bottom: 0;
			transition: transform 0.5s;
			transform: translateX(-900px);
			&.partner {transition: transform 0.6s;}
			&.selected {transform: translateX(0px);}
		}

		.heat {
			position: absolute;
			width: 900px;
			height: 1024px;
			bottom: 0;
			filter: brightness(0);

			&.heatmode {animation: 0.5s linear 0s infinite running heat; color: #6A00FF;}
			&.bloodheatmode {animation: 0.5s linear 0s infinite running heat; color: #FFFD78;}
			&.flipped {z-index: -1;}
		}

		@keyframes heat {
			from {
				filter: brightness(0)
					/* Top */
					drop-shadow(-1px -1px 0px)
					drop-shadow( 0px -1px 0px)
					drop-shadow( 1px -1px 0px)

					/* Middle */
					drop-shadow(-1px  0px 0px)
					drop-shadow( 1px  0px 0px)

					/* Bottom */
					drop-shadow(-1px  1px 0px)
					drop-shadow( 0px  1px 0px)
					drop-shadow( 1px  1px 0px)

					opacity(100%);
			}

			to {
				filter: brightness(0)
					/* Top */
					drop-shadow(-10px -10px 0px)
					drop-shadow(  0px -10px 0px)
					drop-shadow( 10px -10px 0px)

					/* Middle */
					drop-shadow(-10px   0px 0px)
					drop-shadow( 10px   0px 0px)

					/* Bottom */
					drop-shadow(-10px  10px 0px)
					drop-shadow(  0px  10px 0px)
					drop-shadow( 10px  10px 0px)

					opacity(0%);
			}
		}

		.charmoon {
			position: absolute;
			width: 96px;
			height: 96px;
			top: 0;
			right: 0;
			background-image: none;
			filter: drop-shadow(0px 0px 8px white);
			transition: filter 0.5s;
			
			&.selected {filter: drop-shadow(0px 0px 0px white);}
			&.flipped {transform: scaleX(-1);}
		}
	}
</style>