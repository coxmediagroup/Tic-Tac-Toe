// Browser detection for when you get desparate. A measure of last resort.
// http://rog.ie/post/9089341529/html5boilerplatejs

// var b = document.documentElement;
// b.setAttribute('data-useragent',  navigator.userAgent);
// b.setAttribute('data-platform', navigator.platform);

// sample CSS: html[data-useragent*='Chrome/13.0'] { ... }

// Default settings for pnotify
$.pnotify.defaults.history = false;

// remap jQuery to $
(function ($) {


/* trigger when page is ready */
$(document).ready(function () {

	initTinyMCE('textarea.tinymce');
	
	// Default error handling for AJAX calls.
	$.ajaxSetup({
        error: function (resp) {
			err = $.parseJSON(resp.responseText);
			errnotify("Error code: " + err.status, err.message);
        }
    });
	
	// Populate accordion menu
	$.ajax({
		type: 'GET',
		url: '/authoring/api/v1/courses/' + courseId +'/menu/',
		dataType: 'json',
		success: buildMenu,
	});
		
	// Set the height of the menu
	var winSize = $(window).height();
	var extrasSize = 90;
	var theSize = winSize-extrasSize;
	$('#menu-container').height( theSize );
	// Resets the height on win resize
	$(window).resize(function() {
		var winSize = $(window).height();
		var extrasSize = 90;
		var theSize = winSize-extrasSize;
		$('#menu-container').height(theSize);
	});
	
	// open/close Bottom menu
	$('#menu-actions ul').css('display','none').addClass('menu-off');
	$('#menu-actions li').on('click', function(event) {
		event.preventDefault();
		var subMenu = $(this).children('ul');
		if (subMenu.hasClass('menu-off')) {
			$( '#menu-actions li ul' ).slideUp(200).addClass('menu-off');
			$( '#menu-actions li' ).removeClass('active');
			$(this).addClass('active');
			subMenu.delay(200).slideDown(200).removeClass('menu-off');
		}
		else {
			$( '#menu-actions li ul' ).slideUp(200).addClass('menu-off');
			$(this).removeClass('active');
		}
	});
	$( '#menu-actions ul li' ).parent('ul').slideUp(200).addClass('menu-off');


	//*********** Modal windows ***********//
	
	// Save unit/lesson/quiz modal window
	$('.md-modal button.yes').on('click', function (event) {
		var containerDialog = $(this).parents('.md-modal:first');
		var compType = containerDialog.attr('id');
		var compName = containerDialog.find('input').val();
		var allowedTypes = ['quiz', 'unit', 'lesson'];

		if ($.inArray(compType, allowedTypes) === -1) {
			//console.log('Invalid type ' + compType);
			return;
		}
		//console.log('Creating new ' + compType + ' with name ' + compName);
		var selectedComp = getSelectedComponent();

		$.ajax({
			type: 'POST',
			url: '/authoring/api/v1/components/',
			data: {name: compName, type: compType},
			dataType: 'json',
		}).done(
			// update new component in menu tree
			function (newComp) {
				var newCompHtml = '<li><span class="drag"></span>\
					<a href="#" node_id="' + newComp.node_id + '" node_type="'
					+ compType + '">' + compName + '</a>\
					<span class="actions off"></span></li>';
				
				if (compType == 'unit') {
					$('#menu').append(newCompHtml);
				}
				else { // assuming selected comp is an <a> elem
					if ($(selectedComp).siblings('ol').length === 0)
						$('<ol class="menu-container"></ol>').insertAfter(selectedComp);
					$(selectedComp).siblings('ol:first').append(newCompHtml);
				}
		    	addBehaviorToMenuItems();
		    	updateMenu();
		    	initSortables();
		    	var succMsg = toTitleCase(compType) + ' \'' + compName + '\' was succesfully added';
		    	notify(succMsg);
			}
		);
		closeModal();
	});
	
	// 'rename' modal window
	$('#rename button.yes').on('click', function (event) {
		var containerDialog = $(this).parents('.md-modal:first');
		var compID = containerDialog.attr('editing_node_id');
		var aLink = $('a[node_id="' + compID + '"]');
		var newName = containerDialog.find('input').val();
		var oldName = aLink.text();
		containerDialog.removeAttr('editing_node_id');
		
		if (newName !== oldName) {
			aLink.text(newName);
			// let the server know about new name
			$.ajax({
				type: 'POST',
				url: '/authoring/api/v1/components/' + compID + '/',
				data: {name: newName},
				success: function () {
					notify('\'' + oldName + '\' successfully renamed to \'' + newName + '\'');
				}
			});
		}
		closeModal();
	});
	
	// 'delete' modal window
	$('#delete button.yes').on('click', function (event) {
		var containerDialog = $(this).parents('.md-modal:first');
		var compID = containerDialog.attr('editing_node_id');
		var aLink = $('a[node_id="' + compID + '"]');
		containerDialog.removeAttr('editing_node_id');
		aLink.parent().remove();
		updateMenu();
		closeModal();
		var succMsg = toTitleCase(aLink.attr('node_type')) + ' \'' + aLink.text() + '\' was succesfully deleted';
		notify(succMsg);
	});
	
	// Modal window calls
	$('.modal-item').on('click', function(event) {
		var modalItemId = $(this).attr('data-modal');
		$('.overlay').fadeIn(400);
		$( 'body' ).addClass('md-show');
		// set current menu item name
		var aLink = $('span.actions.on').siblings('a:first');
		var modalWin = $('#' + modalItemId);
		modalWin.find('input:first').val(aLink.text());
		modalWin.fadeIn(400).addClass('activeModal');
		modalWin.attr('editing_node_id', aLink.attr('node_id'));
	});
	
	// Close Modal Window  
	$('button.overlay, button.close').on('click', function(event) {
		closeModal();
	});

	// key esc close modal
	$(document).keyup(function (e) {
		if ($('body').hasClass('md-show') && e.keyCode == 27)
			closeModal(); // esc
	});

});



// call jq ui sortable  (UNIT)
function initSortables () {
	$( '#menu' ).sortable({
		placeholder: 'ui-state-highlight',
		stop: updateMenu
    });
	$( '#menu ol' ).sortable({
		placeholder: 'ui-state-highlight',
		connectWith: '#menu ol',
		stop: updateMenu
    });
}

$(window).load(function () {
	initSortables();
});

/*
$(window).resize(function() {
	
});
*/
})(window.jQuery);

///////////////////////////////////////
//  utility functions               //
//////////////////////////////////////

function getSelectedComponent() {
	return $('#menu li a.active');
};

function notify(title, text, type) {
    $.pnotify({
    	title: title || '',
        text: text || '',
        type: type || 'success',
    });
}

function errnotify(title, text) {
	notify(title, text, 'error');
}

function toTitleCase(str)
{
    return str.replace(
    	/\w\S*/g,
    	function (txt) {
    		return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    	}
    );
}

// Close Active Modal Window
function closeModal() {
	$(this).fadeOut(200);
	$('body').removeClass('md-show');
	$('.activeModal').fadeOut(200);
};

function addBehaviorToMenuItems () {
	// accordion units
	$('#menu li a').on('click', function (event) {
		event.preventDefault();
		$(this).parent().children('ol').stop(true, true).slideToggle();
		$('#menu li a').removeClass('active');
		$(this).addClass('active');
		
		var node_id = $(this).attr('node_id');
		var existsLocalContent = existsLocalContentForComponent(node_id);
		if (existsLocalContent === true) {
			//console.log('same elem: nothing to do');
			var content = $(resolveLocalContent(node_id, false)).text();
			tinymce.editors[0].setContent(content);
			return;
		}
		else {
			var localContentDiv = $(resolveLocalContent(node_id, true));
			$.ajax({
				type: 'GET',
				url: '/authoring/api/v1/components/' + node_id,
				dataType: 'json',
	 			success: function(comp_data) {
	 				content = comp_data.content;
	 				tinymce.editors[0].setContent(content);
	 				localContentDiv.text(content);
	 			}
			});
		}
	});

	$('#menu li a, #item-actions li a').on('click', function (event) {
		event.preventDefault();
		$('span.actions').removeClass('on').addClass('off');
		$('#item-actions').fadeOut(200).removeClass('active');
	});

	// add Action Menu to Units & Lessons
	$('span.actions').on('click', function (event) {
		event.preventDefault();
		if ( $(this).hasClass('on') ) {
			$('span.actions').removeClass('on').addClass('off');
			$('#item-actions').fadeOut(200).removeClass('active');
		}
		else {
			$('span.actions').removeClass('on');
			$(this).addClass('on').removeClass('off');
			var position = $(this).offset().top-18;
			$('#item-actions').hide().css('top', position)
							  .fadeIn(200).addClass('active');
		}
	});
}


function updateMenu () {
	// construct menu json tree
	var tree = traverse($('#menu-container'), false);
	//console.log('sending tree: ' + JSON.stringify(tree));
	var courseId = $('#left').attr('node_id');
	tree.node_id = courseId;
	tree.node_type = $('#left').attr('node_type');
	// update course structure on server
	$.ajax({
		type: 'POST',
		url: '/authoring/api/v1/courses/'+ courseId +'/menu/',
		data: {menu_tree: JSON.stringify(tree)},
	});
}


function existsLocalContentForComponent (node_id) {
	return ($('#' + node_id + '_content').length !== 0);
}


function resolveLocalContent (node_id, create) {
	if (!existsLocalContentForComponent(node_id)) {
		if (create === true)
			$('#center').append(
				'<div id="'+ node_id +'_content" style="display: none;"></div>'
			);
		else
			return null;
	}
	return $('#' + node_id +'_content');
}


function traverse (dom_root, add_node_data) {
	var node = {children: []};
	if (add_node_data === true) {
		var anchor = dom_root.find('a:first');
		node.node_id = anchor.attr('node_id');
		node.node_type = anchor.attr('node_type');
	}
	var children = dom_root.children('ol').children('li');
	for (var i=0; i < children.length; i++) {
		node.children.push(traverse($(children[i]), true));
	}
	return node;
}


function buildMenu (syllabus) {
	// build menu tree from ajax response
	var html_str = '';
//	console.log(syllabus);

	function render_syllabus (tree, skipwrapper) {
		if ($.isEmptyObject(tree))
			return;
		if (!skipwrapper)
			html_str += '<ol class="ui-sortable">';
		for (var i=0; i<tree.length; i++) {
			var node = tree[i];
			html_str += '<li><span class="drag"></span><a href="#" node_id="'
					 + node.node_id + '" node_type="' + node.node_type + '">'
					 + node.title + '</a>';	
			render_syllabus(node.children, false);
			html_str += '<span class="actions off"></span></li>';
		}
		if (!skipwrapper)
			html_str += '</ol>';
	}
	
	var nid = syllabus.node_id;
	var course_root_div = $('div[id="left"]');
	course_root_div.attr('node_id', nid);
	course_root_div.attr('node_type', syllabus.node_type);
	course_root_div.find('h2:first span').append(syllabus.title);
	render_syllabus(syllabus.children, true);
	var menuDiv = $('#menu');
	menuDiv.html(html_str);
	addBehaviorToMenuItems();
	// select first unit
	menuDiv.find('a:first').addClass('active');
}


// initialize Tinymce
function initTinyMCE (selectorString) {
    $(selectorString).tinymce({
    	script_url: '/static/authoring/js/tinymce/tinymce.min.js',
		plugins: [
		    "save advlist autolink autosave link image lists charmap print preview hr anchor pagebreak spellchecker",
	        "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
	        "table contextmenu directionality emoticons template textcolor paste fullpage textcolor"
	    ],
	
		toolbar1: "fullpage | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | styleselect formatselect fontselect fontsizeselect",
		toolbar2: "cut copy paste | searchreplace | bullist numlist | outdent indent blockquote | undo redo | link unlink anchor image media code | inserttime preview | forecolor backcolor",
		toolbar3: "table | hr removeformat | subscript superscript | charmap emoticons | print fullscreen | ltr rtl | spellchecker | visualchars visualblocks nonbreaking template pagebreak restoredraft | save",
	
		menubar: false,
		
		// 'save' button stuff
		save_enablewhendirty: true,
	    save_onsavecallback: function () {
	        var newcontent = this.getContent({format : 'raw'});
	        var node_id = $(getSelectedComponent()).attr('node_id');
	        // update locally first
	        $(resolveLocalContent(node_id, false)).text(newcontent);
	        //console.log("Sending content to server: content=" + newcontent);
	        //console.log("component_id=" + node_id);
	    	$.ajax({
	    		type: 'POST',
	    		url: '/authoring/api/v1/components/' + node_id + '/',
	    		data: {'content': newcontent},
	    		error: function (resp) {
	    			err = $.parseJSON(resp.responseText);
	    			errnotify('Oops!... there was an error while saving content:', err.message);
	    		},
	    		success: function () {
	    			notify("Content successfully saved");
	    			// execs 'stateToggle' for 'save' button
	    			tinymce.editors[0].nodeChanged();
	    		}
	    	});
	    },
	
		style_formats: [
	        {title: 'Bold text', inline: 'b'},
			{title: 'Red text', inline: 'span', styles: {color: '#ff0000'}},
			{title: 'Red header', block: 'h1', styles: {color: '#ff0000'}},
			{title: 'Example 1', inline: 'span', classes: 'example1'},
			{title: 'Example 2', inline: 'span', classes: 'example2'},
			{title: 'Table styles'},
			{title: 'Table row 1', selector: 'tr', classes: 'tablerow1'}
		],
	
		templates: [
			{title: 'Test template 1', content: 'Test 1'},
			{title: 'Test template 2', content: 'Test 2'}
		]
		});
		
		var winSize = $(window).height();
		// TinyMCE Textarea Height
		$(selectorString).height(winSize);
		$(window).resize(function () {
			var winSize = $(window).height();
			$(selectorString).height(winSize);
		});
}