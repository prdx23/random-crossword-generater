var timer = 250;
var boardsize = 0
var wordsnum = 0
var sec = 0
var disable1 = false
var disable2 = false
var disable3 = false


function main()
{
	boardsize = $('#boardsize').val()
	wordno = $('#wordno').val()
	sec = $('#sec').val()

	if( parseInt(boardsize) >= 20 && parseInt(boardsize) <= 80)
	{
		$('.boardsize').addClass('has-success').removeClass('has-error')
		$('.i1').removeClass('glyphicon-remove').addClass('glyphicon-ok');
		disable1 = false
	}
	else
	{
		$('.boardsize').addClass('has-error').removeClass('has-success')
		$('.i1').removeClass('glyphicon-ok').addClass('glyphicon-remove');
		disable1 = true
	}

	if( parseInt(wordno) >= 10 && parseInt(wordno) <= 50)
	{
		$('.wordno').addClass('has-success').removeClass('has-error')
		$('.i2').removeClass('glyphicon-remove').addClass('glyphicon-ok');
		disable2 = false
	}
	else
	{
		$('.wordno').addClass('has-error').removeClass('has-success')
		$('.i2').removeClass('glyphicon-ok').addClass('glyphicon-remove');
		disable2 = true
	}


	if( parseInt(sec) >= 5 && parseInt(sec) <= 300)
	{
		$('.sec').addClass('has-success').removeClass('has-error')
		$('.i3').removeClass('glyphicon-remove').addClass('glyphicon-ok');
		disable3 = false
	}
	else
	{
		$('.sec').addClass('has-error').removeClass('has-success')
		$('.i3').removeClass('glyphicon-ok').addClass('glyphicon-remove');
		disable3 = true
	}

	if(disable1 == true || disable2 == true || disable3 == true)
	{
		$('#submit').attr("disabled", true);
	}
	else
	{
		$('#submit').attr("disabled", false);
	}

}

$(document).ready(
	function()
	{
		$(document).on('click','.btn-sm-1',
			function() 
			{
				$('#boardsize').val('20')
				$('#wordno').val('10')
				$('#sec').val('5')
			}
		);	

		$(document).on('click','.btn-md-1',
			function() 
			{
				$('#boardsize').val('30')
				$('#wordno').val('20')
				$('#sec').val('30')
			}
		);	

		$(document).on('click','.btn-md-2',
			function() 
			{
				$('#boardsize').val('30')
				$('#wordno').val('15')
				$('#sec').val('20')
			}
		);		

		$(document).on('click','.btn-lg-1',
			function() 
			{
				$('#boardsize').val('30')
				$('#wordno').val('40')
				$('#sec').val('90')
			}
		);	

		$(document).on('click','.btn-lg-2',
			function() 
			{
				$('#boardsize').val('30')
				$('#wordno').val('50')
				$('#sec').val('120')
			}
		);	

	}
);


var id = setInterval(main,timer); 