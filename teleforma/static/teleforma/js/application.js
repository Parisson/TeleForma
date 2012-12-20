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


$(window).ready(function() {
	var pageHeight = $(window).height();
	var navHeight = pageHeight - 140;
	$('#desk_center').css({"max-height": navHeight + 'px'});
});
