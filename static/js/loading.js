var timer = 30;
var count = 1;
var line1 = '';
var line2 = '';
var line3 = '';
var line4 = '';
var olddata = '';

function main()
{
    $.get('_info_', 
    	function(data, status)
    	{
        	if(data=='DONE')
        	{
        		window.location.replace('_output_');
        		clearInterval(id);
        	}
        	else
        	{
        		if(data != olddata)
        		{
        			olddata = data
        			line1 = '';
					line2 = '';
					line3 = '';
					line4 = '';

	        		for(i=0;i<data.length;i++)
	        		{
	        			if(count == 1)
	        			{
	        				if(data.charAt(i) != '#')
	        				{line1 += data.charAt(i)}
	        				else
	        				{count = 2}
	        			}
	        			else if(count == 2)
	        			{
	        				if(data.charAt(i) != '#')
	        				{line2 += data.charAt(i)}
	        				else
	        				{count = 3}
	        			}
	        			else if(count == 3)
	        			{
	        				if(data.charAt(i) != '#')
	        				{line3 += data.charAt(i)}
	        				else
	        				{count = 4}
	        			}
	        			else if(count == 4)
	        			{
	        				if(data.charAt(i) == '%')
	        				{
	        					count = 1;
	        					$('.line1').html(line1);
	        					$('.line2').html(line2);
	        					$('.line3').html(line3);
	        					$('.line4').html(line4);
	        				}
	        				else
	        				{line4 += data.charAt(i)}
	        			}
	        		}
        		}
        	}
    	}
    );
}

var id = setInterval(main,timer); 