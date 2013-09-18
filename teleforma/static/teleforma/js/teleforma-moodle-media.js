/*
 * Copyright (C) 2007-2013 Parisson SARL
 * Copyright (c) 2011 Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 *
 * This file is part of Telecaster.
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
 *          Olivier Guilyardi <olivier@samalyse.com>
 *          Guillaume Pellerin <yomguy@parisson.com>
 */

/**
 * Class for telemeta global functions.
 * Note that the dollar sign is a reserved keyword in some browsers
 * (see http://davidwalsh.name/dollar-functions)
 * which might be in conflict with jQuery dollar sign.
 */


/*****************************************************************************
 * json(param, method, onSuccesFcn(data, textStatus, jqXHR), onErrorFcn(jqXHR, textStatus, errorThrown))
 * global function to senbd/retrieve data with the server
 *
 * param: the data to be sent or retrieved.
 *   param will be converted to string, escaping quotes newlines and backslashes if necessary.
 *   param can be a javascript string, boolean, number, dictionary and array.
 *       If dictionary or array, it must contain only the above mentioned recognized types.
 *       So, eg, {[" a string"]} is fine, {[/asd/]} not
 *
 * method: the json method, eg "telemeta.update_marker". See base.py
 *
 * onSuccesFcn(data, textStatus, jqXHR) OPTIONAL --IF MISSING, NOTHING HAPPENS --
 *    A function to be called if the request succeeds with the same syntax of jQuery's ajax onSuccess function.
 *    The function gets passed three arguments
 *       The data returned from the server, formatted according to the dataType parameter;
 *       a string describing the status;
 *       and the jqXHR (in jQuery 1.4.x, XMLHttpRequest) object
 *
 * onErrorFcn(jqXHR, textStatus, errorThrown) OPTIONAL. --IF MISSING, THE DEFAULT ERROR DIALOG IS SHOWN--
 *     A function to be called if the request fails with the same syntax of jQuery ajax onError function..
 *     The function receives three arguments:
 *       The jqXHR (in jQuery 1.4.x, XMLHttpRequest) object,
 *       a string describing the type of error that occurred and
 *       an optional exception object, if one occurred.
 *       Possible values for the second argument (besides null) are "timeout", "error", "abort", and "parsererror".
 * ****************************************************************************/

var json = function(param,url,method,onSuccessFcn,onErrorFcn){
    //this function converts a javascript object to a string
    var toString_ = function(string){
        if(typeof string == "string"){
            //escapes newlines quotes and backslashes
            string = string.replace(/\\/g,"\\\\")
            .replace(/\n/g,"\\n")
            .replace(/"/g,"\\\"");
        }
        var array; //used for arrays and objects (see below)
        if(typeof string == "boolean" || typeof string== "number" || typeof string == "string"){
            string = '"'+string+'"';
        }else if(string instanceof Array){
            array = [];
            for(var i = 0;i <string.length ; i++){
                array.push(toString_(string[i])); //recursive invocation
            }
            string='[';
            string+=array.join(",");
            string+=']';
        }else{
            array = [];
            for(var k in string){
                array.push(toString_(k)+":"+toString_(string[k])); //recursive invocation
            }
            string='{';
            string+=array.join(",");
            string+='}';
        }
        return string;
    };

    //creating the string to send.
    var param2string = toString_(param);
    var data2send = '{"id":"jsonrpc", "params":';
    data2send+=param2string;
    data2send+=', "method":"'
    data2send+=method;
    data2send+='","jsonrpc":"1.0"}';

    var $J = jQuery;
    
    $J.ajax({
        type: "POST",
        url: url + '/json/',
        contentType: "application/json",
        data: data2send,
        dataType: "json",
        success: function(data, textStatus, jqXHR){
            if(onSuccessFcn){
                onSuccessFcn(data, textStatus, jqXHR);
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            if(onErrorFcn){
                onErrorFcn(jqXHR, textStatus, errorThrown);
                return;
            }
            //default:
            var details = "\n(no further info available)";
            if(jqXHR) {
                details="\nThe server responded witha status of "+jqXHR.status+" ("+
                jqXHR.statusText+")\n\nDetails (request responseText):\n"+jqXHR.responseText;
            }
            alert("ERROR: "+details);

        }
    });

};


function get_course_media_urls(host, id){
    var data = json([id],'http://' + host, "teleforma.get_course_media_urls",
        function(data){
            var res = data.result;
            for(var i=0; i<res.length; i++){
                var media_dict = res[i];
                var session = media_dict['session'];
                var section = '#section-' + session;
                var video_id = 'video-' + i.toString();
                var s = '<br /><center><video id="' + video_id + '" class="video-js vjs-default-skin" width="640" height="360" controls preload="none" poster="' + media_dict['poster'] + '">';
                var urls = media_dict['urls'];
                for (var j=0; j<urls.length; j++){
                    url = urls[j];
                    if (url['mime_type'].indexOf("video") != -1){
                        s += '<source src="'+url['url']+'" type="'+url['mime_type']+'">\n';
                    };
                };
                s += '</video></center><br />\n';
                $(section).append(s);
                _V_(video_id, {}, function(){});
            };
        },
        function(){
            s = '<span class="warning">NOT connected</span>';
            $('#layout').html(s);
        }
    );
    
};

