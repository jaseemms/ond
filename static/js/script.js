function resize(){
	var windowWidth = $(window).width();
	var windowHeight = $(window).height();
	
	var sidebarHeight = windowHeight ;
	function equalPackageWidget1(){
		var h = 0;
		$('#list ul li').height('auto');
		$('#list ul li').each(function(){
			var height = $(this).height();
			if(height > h){
				h = height;
			}
		});
		$('#list ul li').height(h);
	}
	equalPackageWidget1();

	function equalPackageWidget2(){
		var h = 0;
		$('#categories .content div.bottom ul li').height('auto');
		$('#categories .content div.bottom ul li').each(function(){
			var height = $(this).height();
			if(height > h){
				h = height;
			}
		});
		$('#categories .content div.bottom ul li').height(h);
	}
	equalPackageWidget2();
	
}
$(document).ready(function(){
	
    $('a[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
                $('html, body').animate({
                  scrollTop: target.offset().top
                }, 2000);
                return true;
            }
        }
    });
    resize();

  	$(document).click(function(e){

	   if($(e.target).hasClass("dropdown-button")){
		  $('.dropdown-list').toggleClass('show');
	   }else{
	      $('.dropdown-list').removeClass('show');
	   }

	});

});	

$(window).resize(function(){
	resize();
});

$(window).load(function(){
	resize();
});