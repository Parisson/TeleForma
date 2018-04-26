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

$(document).ready(function(){
     if($('.home').size()){
         $('.course').each(function(){
             var $course = $(this);
             var course_url = $course.find('.course_title a').attr('href');
             $course.find('.course_content .listing tbody').each(function(){
                 var $tbody = $(this);
                 if($tbody.find('tr').size()>=2) {
                     $tbody.find('tr:not(:first)').remove();
                     $tbody.append('<tr><td><a href="'+course_url+'">Voir la suite</a></td><td></td><td></td></tr>')
                 }
             });
         })
     }
});