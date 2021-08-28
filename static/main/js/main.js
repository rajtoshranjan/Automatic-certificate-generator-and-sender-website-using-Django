
  document.querySelector('#sidebarCollapse').addEventListener('click',function() {
    document.querySelector('#sidebar').classList.toggle('active');
    document.querySelector('#content').classList.toggle('active');
  });



function editMenu(elm) {

	let title = document.getElementById(`${elm}-title`);
	let icon = document.getElementById(`${elm}-icon`);
	let url = document.getElementById(`${elm}-url`);
	let btn = document.getElementById(`${elm}-btn`);

	title.innerHTML = `<input type='text' value='${title.innerText}' style="width:100%">`;
	icon.innerHTML = `<input type='text' value='${icon.innerText}' style="width:100%">`;
	url.innerHTML = `<input type='text' value='${url.innerText}' style="width:100%">`;
	btn.innerHTML = `<input type='button' value='Save' onclick="editMenuSend('${elm}')">`;
}

function editMenuSend(elm){
	let title = document.getElementById(`${elm}-title`).querySelector('input').value;
	let icon = document.getElementById(`${elm}-icon`).querySelector('input').value;
	let url = document.getElementById(`${elm}-url`).querySelector('input').value;
	$.ajax(
    {
        type:"POST",
        url: '/updateMenu',
        data:{
        		 id: elm,
                 title: title,
                 icon: icon,
                 url:url,
        },	
        success: function(data) 
        {
        	document.getElementById(`${elm}-title`).innerText = data.title;
        	document.getElementById(`${elm}-icon`).innerText = data.icon;
        	document.getElementById(`${elm}-url`).innerText = data.url;
        	document.getElementById(`${elm}-btn`).innerHTML = `<i class="fa fa-edit" style="float: right; cursor: pointer;	" onclick="editMenu('${elm}')"></i>`;
        }
     });
}
