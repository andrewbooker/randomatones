const timeline = 
[
    {
        when: "2020-09-13",
        heading: "Assembly",
        image: "https://live.staticflickr.com/65535/50353163628_ddc6f6110f_c.jpg", 
        text: "Three units taking shape now. First task for each one is to position the speakers. The middle-sized on is the prototype, so I had already done this. The other two are similar, but each unit has a different combination of speaker sizes for individuality. The plan is to position the multiple units in separate parts of the room, but I actually quite like the way these units look clustered together. It makes me thing the speaker positioning should be random, rather than regular and predictable as they are here. Next task is to take the speakers off, put other bits of wood on for mounting the electronics later, then sand and paint in bright colours. Because why not."
    },
    {
        when: "2020-09-11",
        heading: "Next vertical unit",
        image: "https://live.staticflickr.com/65535/50353163633_0ccf383a40_c.jpg",
        text: "Back to the dry land idea, having enjoyed listening to one of these, time to start putting together more of them. Target is three for now, for which I will see if I can arrange some kind of showing in London. Maybe get a video together first. It strikes me the audio should be a field recording. It will be almost impossible to capture the ambient sound distribution from having three (nevermind several) of these positioned around a room, and a normal stereo recording is going to sound too perfect an impression of the wrong thing. One idea I had is to mount a couple of tiny mics onto each unit and let each make its own room/field recording from its perspective, then mix those in the stereo image depending on where the camera is pointing."
    },
    {
        when: "2020-09-09",
        heading: "Mental notes",
        image: "https://live.staticflickr.com/65535/50354023537_aa2fc0f818_b.jpg",
        orientation: "landscape",
        text: "This looks like a nice spot for it. The acoustics under the first bridge are sweet, and the traffic noise from above might even complement the sounds. What to call it though - Water Music For Randomatones? Randomaquatones? Also somehow I have to get these things to float. My heaviest 12V batteries are 5.5Kg. That's going to need a big tyre."
    },
    {
        when: "2020-09-08",
        heading: "Floating an idea",
        image: "https://live.staticflickr.com/65535/50354023557_eec8ed7162_b.jpg",
        orientation: "landscape",
        text: "An eventful week of blowing up a Raspberry Pi and an amp. Tried a new smaller RPi (model A+) and found it had some glitches, but these could be reproduced simply by adjusting the system volume, so I'm not confident about the analogue output. Needing replacement amp as well I went for a HifiBerry Pi \"hat\", which is entirely digital and will thus bypass all the RPi audio bits which I think are the issue. Also, brilliantly, it takes 12V but will do the step down to 5V itself for the RPi. This will save me having to have an extra unit with wiring issues. Tried it all out after the necessary config changes in the RPi to tell it where its audio has to go. Not only does everything work, the audio is basically clean. Needs a volume control though, without a keybaord or a mouse. Hmm! In a totally unrelated flight of consciousness, I have begun pursuing the crazy idea of making a set of these units that will float. This would be the basic chassis, and one way of making it float might be to use the inner tube of a car tyre. So I've ordered one. I might work on this frame idea a bit more. I'm pleased with my elementary woodworking skills to have made this item, which at least looks like it fits together."
    },
    {
        when: "2020-08-28",
        heading: "Trying out the prototype",
        image: "https://live.staticflickr.com/65535/50353863201_2716b72e24_c.jpg",
        text: "The prototype again, reconstructed with only three vertical posts, as I realised the fourth was unnecessary and in the way. Tried the sound generator, essentially everything works, with some issues. Audio playback has glitches, and there is a lot of interference noise. One issue might be the 12V-5V converter, as I've heard this kind of noise before when combining audio signals from things with different switch mode PSUs. Anyway I tried a USB audio interface just to rule out the RPi onboard DAC. Slightly quieter. Reduced noise significantly by not using 12v-5v stepdown, instead powering the RPi from a regular mains PSU. Got noise at all running it from two separate batteries. Joining the battery grounds made a load of noise reappear. Joining the +ves also made noise appear. Tried a different 12V-5V converter from the car, same result." 
    },
    {
        when: "2020-08-19",
        heading: "Randomatone One",
        image: "https://live.staticflickr.com/65535/50354023587_71db41b9fa_c.jpg", 
        text: "Assembled prototype. You can just see that behind the circuit boards is a massive 12V 20Ah battery, the kind you find in a mobility scooter. This powers the Raspberry Pi via a step-down to 5V, and a 2x20W amp, currently driving two cheap speakers from Halfords. I've been preparing the software for this for some time now and had it working on a regular linux machine, and have tried it out on the RPi by itself over Wifi, not in this assembly yet."
    }
];
