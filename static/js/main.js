


function check_screen_size()
{
	var sizes = ['xs','sm','md','lg'];
	var $element = $('<div>');
	var i;

	$element.appendTo($('body'));

	for(i=0;i<sizes.length;i++)
	{
		var size = sizes[i];
		var clas = 'hidden-' + size;

		$element.addClass(clas);

		if($element.is(':hidden'))
		{
			$element.remove();
			return size;
		}

	}

	return 'lg';
}

function scaletext()
{
	var currentsize = check_screen_size();
	if(currentsize == 'xs')
	{
		$('.heading').css('font-size','20px');
		$('.img').hide()
	}
	else if(currentsize == 'sm')
	{
		$('.heading').css('font-size','22px');
		$('.img').hide()	
	}
	else
	{
		$('.heading').css('font-size','25px');
		$('.img').show()
	}
}

setInterval(scaletext,100);