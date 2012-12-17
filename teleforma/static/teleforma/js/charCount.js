/*
 * 	Character Count Plugin - jQuery plugin
 * 	Dynamic character count for text areas and input fields
 *	written by Alen Grakalic	
 *	http://cssglobe.com/post/7161/jquery-plugin-simplest-twitterlike-dynamic-character-count-for-textareas
 *
 *	Copyright (c) 2009 Alen Grakalic (http://cssglobe.com)
 *	Dual licensed under the MIT (MIT-LICENSE.txt)
 *	and GPL (GPL-LICENSE.txt) licenses.
 *
 *	Built for jQuery library
 *	http://jquery.com
 *
 */
 

(function($) {

	$.fn.charCount = function(options){
	  
		// default configuration properties
		var defaults = {	
			necessary: 500,		
			css: 'counter',
			counterElement: 'span',
			cssDeceed: 'deceed',
			cssExceed: 'exceed',
			counterText: ''
		}; 
			
		var options = $.extend(defaults, options); 

		function calculate(obj){
			var count = $(obj).val().length;
			if(count >= options.necessary){
				$(obj).next().removeClass(options.css);
				$(obj).next().removeClass(options.cssDeceed);
				$(obj).next().addClass(options.cssExceed);
			} else {
				$(obj).next().removeClass(options.css);
				$(obj).next().removeClass(options.cssExceed);
				$(obj).next().addClass(options.cssDeceed);
			}
			
			$(obj).next().html(options.counterText + count + ' / ' + options.necessary);
			var percent = parseInt(count / options.necessary * 100);
			if ( percent >= 100 ) {
				percent = 100;
			}
			var color = '#' + rainbow.colourAt(percent);
			$('#answer-progress').html(percent);
			$('#progressbar-answer').progressbar({ value: percent });
			$('#progressbar-answer div').css({"background": color});
		};
				
		this.each(function() {  			
			$(this).after('<'+ options.counterElement +' id="counter" class="' + options.css + '">'+ options.counterText +'</'+ options.counterElement +'>');			
			calculate(this);
			$(this).keyup(function(){calculate(this)});
			$(this).change(function(){calculate(this)});
		});
	  
	};

})(jQuery);
