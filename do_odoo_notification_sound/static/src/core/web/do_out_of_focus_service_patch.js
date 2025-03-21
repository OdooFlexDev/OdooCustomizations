/* @odoo-module */

import { OutOfFocusService, outOfFocusService } from "@mail/core/common/out_of_focus_service";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { url } from "@web/core/utils/urls";
import { session } from "@web/session";


patch(OutOfFocusService.prototype, {

    async _playSound() {

        if (this.canPlayAudio && this.multiTab.isOnMainTab()) {
            if (!this.audio) {
                const userName = session.name || "User";
                console.log("===usernak===",userName,session.uid)
                const text = `Hi ${userName}, Check your inbox! You have a new message.`;
                const utterance = new SpeechSynthesisUtterance(text);

                const voices = window.speechSynthesis.getVoices();
                utterance.voice = voices.find(voice => voice.name === 'Alex') || voices[0];

                window.speechSynthesis.speak(utterance);
            }
        }
    },
});


// patch(OutOfFocusService.prototype, {

//     async _playSound() {
//         if (this.canPlayAudio && this.multiTab.isOnMainTab()) {
//             if (!this.audio) {
//                 this.audio = new Audio();
//                 this.audio.src = this.audio.canPlayType("audio/ogg; codecs=vorbis")
//                     ? url("/do_odoo_notification_sound/static/src/audio/notification_1.mp3")
//                     : url("/do_odoo_notification_sound/static/src/audio/notification_2.mp3");
//             }
//             this.audio.volume = 1.0;
//             try {
//                 await this.audio.play();
//             } catch {
//                 // Ignore errors due to the user not having interracted
//                 // with the page before playing the sound.
//             }
//         }
//     },
// });
