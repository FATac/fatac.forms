var langList = ["ca", "es", "en", "fr", "it", "de", "ar", "zh", "pt"]

function getCurrentInputValue() {
	if (window['currentInput'] != undefined) return window['currentInput'].value;
	else return null;
}
function setCurrentInputValue(value) {
	if (window['currentInput'] != undefined) $(window['currentInput']).val(value);
}

function seekObject(obj, c) {
	currentInput = $(obj).parent().children('.objectinput');
	window.open('./seek?objectSelect=true&classSelect='+c);
}

function createObject(obj, c) {
	currentInput = $(obj).parent().children('.objectinput');
	window.open("./uploadData?r=true&c="+c);
}

function mediaUrlPreview(url) {
	$("#mediaurl").val(url);
	if (url!='')
		$("#preview").html("<iframe src='"+url+"' width='600' height='400' name='mediaFrame'></iframe>");
	else
		$("#preview").html("<iframe width='600' height='400' name='mediaFrame'></iframe>");
}

function setMediaUrl(url) {
	if (window['mediaurl'] != undefined) window['mediaurl'].value = url;
}

function showMediaSelector(obj) {
	currentInput = obj
	$('#uploadMediaLink').trigger('click');
}

function autocompleteLanguages(control) {
	if (control.value == "") return;
	control.value = control.value.toLowerCase();
	for (var i=0;i<langList.length;i++) {
		if  (langList[i].match("^"+control.value)) {
			control.value = langList[i]; return; 
		}
	}
	
	control.value = "";
	return;
}

function deleteObject(id) {
	deleteOverlay.show();
}

function deleteObjectConfirmed(id,loc) {
	if (loc == null || loc == '')
		window.location.href = './deleteObject?objectId=' + id;
	else
		window.location.href = './deleteObject?objectId=' + id + '&loc=' + loc;
}

function callExpander() {
	$("a").css("cursor","pointer");
	$('textarea.expand').autoResize({
	    // On resize:
	    onResize : function() {
	        $(this).css({opacity:0.8});
	    },
	    // After resize:
	    animateCallback : function() {
	        $(this).css({opacity:1});
	    },
	    // Quite slow animation:
	    animateDuration : 300,
	    // More extra space:
	    extraSpace : 5
	});
}

function addControl(name) {
	var cntrl = $("#"+name+"_cntrl div:last-child").clone().hide();
	$("#"+name+"_cntrl").append(cntrl.fadeIn(800, callExpander));
}

function removeControl(name, obj) {
	if ($("#"+name+"_cntrl > div").size() > 1) {
		$(obj).parent().fadeOut(500, function() { $(obj).parent().remove(); });
	}
}

function getObjectInputValue(obj) {
	return $(obj).parent().children('.objectinput').val();
}

function goToObject(id, pos) {
	if (id == undefined || id.trim() == '') return;
	var locator = "";
	var target = "";
	if (document.myform.locator != undefined) locator = document.myform.locator.value;
	else target = 'target="gotowin"';
	if (pos!=null)
		$("#mydiv").html('<form action="/fatac/updateExisting" '+target+' name="myform2" method="post"><input type="hidden" name="locator" value="'+locator+'"><input type="hidden" name="id" value="'+id+'"><input type="hidden" name="pos" value="'+pos+'"></form>');
	else
		$("#mydiv").html('<form action="/fatac/updateExisting" '+target+' name="myform2" method="post"><input type="hidden" name="locator" value="'+locator+'"><input type="hidden" name="id" value="'+id+'"></form>');
	document.myform2.submit();
}

(function($){
    
    $.fn.autoResize = function(options) {
        
        // Just some abstracted details,
        // to make plugin users happy:
        var settings = $.extend({
            onResize : function(){},
            animate : true,
            animateDuration : 150,
            animateCallback : function(){},
            extraSpace : 20,
            limit: 1000
        }, options);
        
        // Only textarea's auto-resize:
        this.filter('textarea').each(function(){
            
                // Get rid of scrollbars and disable WebKit resizing:
            var textarea = $(this).css({resize:'none','overflow-y':'hidden'}),
            
                // Cache original height, for use later:
                origHeight = textarea.height(),
                
                // Need clone of textarea, hidden off screen:
                clone = (function(){
                    
                    // Properties which may effect space taken up by chracters:
                    var props = ['height','width','lineHeight','textDecoration','letterSpacing'],
                        propOb = {};
                        
                    // Create object of styles to apply:
                    $.each(props, function(i, prop){
                        propOb[prop] = textarea.css(prop);
                    });
                    
                    // Clone the actual textarea removing unique properties
                    // and insert before original textarea:
                    return textarea.clone().removeAttr('id').removeAttr('name').css({
                        position: 'absolute',
                        top: 0,
                        left: -9999
                    }).css(propOb).attr('tabIndex','-1').insertBefore(textarea);
					
                })(),
                lastScrollTop = null,
                updateSize = function() {
					
                    // Prepare the clone:
                    clone.height(0).val($(this).val()).scrollTop(10000);
					
                    // Find the height of text:
                    var scrollTop = Math.max(clone.scrollTop(), origHeight) + settings.extraSpace,
                        toChange = $(this).add(clone);
						
                    // Don't do anything if scrollTip hasen't changed:
                    if (lastScrollTop === scrollTop) { return; }
                    lastScrollTop = scrollTop;
					
                    // Check for limit:
                    if ( scrollTop >= settings.limit ) {
                        $(this).css('overflow-y','');
                        return;
                    }
                    // Fire off callback:
                    settings.onResize.call(this);
					
                    // Either animate or directly apply height:
                    settings.animate && textarea.css('display') === 'block' ?
                        toChange.stop().animate({height:scrollTop}, settings.animateDuration, settings.animateCallback)
                        : toChange.height(scrollTop);
                };
            
            // Bind namespaced handlers to appropriate events:
            textarea
                .unbind('.dynSiz')
                .bind('keyup.dynSiz', updateSize)
                .bind('keydown.dynSiz', updateSize)
                .bind('change.dynSiz', updateSize);
            
        });
        
        // Chain:
        return this;
        
    };
    
})(jQuery);

jQuery(document).ready(function() {
	callExpander();
	
	jQuery(function ($) { 
	    $('#uploadMediaLink') 
	        .prepOverlay({
	        	subtype: 'ajax', 
	            filter: '#content > *',
	            api: true,
	            config: { onLoad: function() { 
	            			$("#mediaurl").val(getCurrentInputValue());
	            		}
	            	}
	        }); 
	});
	
	deleteOverlay  = $("#confirmDelete").overlay({
			top: 260,
			mask: {
				color: '#fff',
				loadSpeed: 200
			},

			closeOnClick: true
		});

});