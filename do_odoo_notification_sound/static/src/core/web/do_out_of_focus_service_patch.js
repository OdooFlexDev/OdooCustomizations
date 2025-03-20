/* @odoo-module */

import { OutOfFocusService, outOfFocusService } from "@mail/core/common/out_of_focus_service";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { url } from "@web/core/utils/urls";

patch(OutOfFocusService.prototype, {

    async _playSound() {
        if (this.canPlayAudio && this.multiTab.isOnMainTab()) {
            if (!this.audio) {
                this.audio = new Audio();
                this.audio.src = this.audio.canPlayType("audio/ogg; codecs=vorbis")
                    ? url("/do_odoo_notification_sound/static/src/audio/notification_1.mp3")
                    : url("/do_odoo_notification_sound/static/src/audio/notification_2.mp3");
            }
            this.audio.volume = 1.0;
            try {
                await this.audio.play();
            } catch {
                // Ignore errors due to the user not having interracted
                // with the page before playing the sound.
            }
        }
    },
});
