/*
 * Copyright (C) 2007-2012 Parisson SARL
 *
 * This file is part of TimeSide.
 *
 * TimeSide is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * TimeSide is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Authors: Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
            Guillaume Pellerin <yomguy@parisson.com>
 */

/**
 * Class for managing conferences in teleforma.
 * Requires jQuery
 */


var rainbow = new Rainbow();
rainbow.setSpectrum('#bb0000', '#e65911', '#f3ad17', 'green');


function pad(num) {
        var s = num + "";
        while (s.length < 2) s = "0" + s;
        return s;
}

$(window).ready(function () {
        var pageHeight = $(window).height();
        var navHeight = pageHeight - 125;
        $('#desk_center').css({ "max-height": navHeight + 'px' });
        launchTimer();
});


var launchTimer = function () {
        // chronometer
        $('.autotimer').each(function () {
                window.timer = new Timer();
                $timerSpan = $(this);
                var value = $timerSpan.text()
                // convert text value of timer to seconds
                var timeArray = value.split(':');
                var seconds = parseInt(timeArray[0], 10) * 3600 + parseInt(timeArray[1], 10) * 60 + parseInt(timeArray[2], 10);
                window.timer.start({ precision: 'seconds', startValues: { seconds: seconds } });
                window.timer.addEventListener('secondsUpdated', function (e) {
                        var timeValues = window.timer.getTimeValues();
                        var hours = timeValues.days * 24 + timeValues.hours
                        $timerSpan.html(pad(hours) + ':' + pad(timeValues.minutes) + ':' + pad(timeValues.seconds));
                });
        });
}

function onLoadSeminar(seminarId, username) {
        // send a request when user load a seminar
        json([seminarId, username], 'teleforma.seminar_load', function () { return null; });
}

function onUnloadSeminar(seminarId, username) {
        try {
                var params = JSON.stringify({ "id": "jsonrpc", "params": [seminarId, username], "method": "teleforma.seminar_unload", "jsonrpc": "1.0" })
                navigator.sendBeacon("json/", params);
        }
        catch {
                // compatibility with old navigators
                json_sync([seminarId, username], 'teleforma.seminar_unload', function () { return null; });
        }
}
