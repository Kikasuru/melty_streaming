/* EDIT THIS IF YOU PLAN ON MAKING A BORDER WITH YOUR OWN HTML/CSS */
function handlePlayer(data, plr)
{
    if (!data.waiting) {
        charId = data[`p${plr}char`].toString().padStart(2, "0");

        // Set the name of this character
        $(`#p${plr}name`).css("background-image",
            `url("assets/name/vs_name00_${charId}.png")`);

        // Character Selected
        if(data[`p${plr}selmode`] > 0) {
            // Set the mugshot of this character
            $(`#p${plr}mug`).css("background-image",
                `url("assets/mug/cut_${charId}00.png")`);
            $(`#p${plr}mugheat`).css("background-image",
                `url("assets/mug/cut_${charId}00.png")`);

            // Set if this mugshot is selected
            $(`#p${plr}mug`).toggleClass("selected", true);
            $(`#p${plr}bnr`).toggleClass("selected", true);

            // If the character is a duo character, set their partner
            if([0x04, 0x22, 0x23].includes(data[`p${plr}char`])) {
                $(`#p${plr}mugptnr`).css("background-image",
                    `url("assets/mug/cut_${charId}01.png")`);
                $(`#p${plr}mugheat`).css("background-image",
                    `url("assets/mug/cut_${charId}00.png"), url("assets/mug/cut_${charId}01.png")`);
                $(`#p${plr}mugptnr`).toggleClass("selected", true);
            }
        } else {
            // Toggle the selected class off
            $(`#p${plr}mug`).toggleClass("selected", false);
            $(`#p${plr}bnr`).toggleClass("selected", false);
            $(`#p${plr}mugptnr`).toggleClass("selected", false);
        }

        // Moon Selected
        if(data[`p${plr}selmode`] > 1) {
            // Set the moon image
            $(`#p${plr}moon`).css("background-image",
                `url("assets/moon/moon_${data[`p${plr}moon`]}.png")`);

            // Set if the moon is selected
            $(`#p${plr}moon`).toggleClass("selected", true);
        } else {
            $(`#p${plr}moon`).toggleClass("selected", false);
            $(`#p${plr}moon`).css("background-image",
                `none`);
        }

        // Check for heat type
        if (data[`p${plr}heat`] !== 0 && data[`gamemode`] === 1) {
            // Heat and Max mode use the same colors
            if (data[`p${plr}heat`] === 1 || data[`p${plr}heat`] === 2) {
                $(`#p${plr}mugheat`).toggleClass("heatmode", true);
            // Only other option is Blood Heat
            } else {
                $(`#p${plr}mugheat`).toggleClass("bloodheatmode", true);
            }
        } else {
            $(`#p${plr}mugheat`).toggleClass("heatmode", false);
            $(`#p${plr}mugheat`).toggleClass("bloodheatmode", false);
        }
    } else {
        // Toggle the selected class off
        $(`#p${plr}mug`).toggleClass("selected", false);
        $(`#p${plr}bnr`).toggleClass("selected", false);
        $(`#p${plr}mugptnr`).toggleClass("selected", false);

        $(`#p${plr}moon`).toggleClass("selected", false);
        $(`#p${plr}moon`).css("background-image",
            `none`);

        // Set the name to none
        $(`#p${plr}name`).css("background-image",
            `none`);

        // Turn off heat modes
        $(`#p${plr}mugheat`).toggleClass("heatmode", false);
        $(`#p${plr}mugheat`).toggleClass("bloodheatmode", false);
    }
}


/* LEAVE THESE ALONE IF YOU DON'T KNOW WHAT YOU'RE DOING */
apiClock = null;
pulling = false;

function clockTick()
{
    if (!pulling) {
        // Pull from the API
        pulling = true;
        axios.get("/state")
        .then(res => {
            handlePlayer(res.data, "1");
            handlePlayer(res.data, "2");
        })
        .catch(err => {
            console.log(err);
        })
        .then(() => {
            // Allow the clock to pull again
            pulling = false;
        });
    }
}

function startClock()
{
    if (apiClock === null) {
        apiClock = setInterval(clockTick, 16);
    }
}

function stopClock()
{
    if (apiClock !== null) {
        clearInterval(apiClock);
        apiClock = null;
    }
}
