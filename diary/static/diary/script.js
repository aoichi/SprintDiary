
$(".dropdown-trigger").dropdown();

$(document).ready(function(){
    $('.sidenav').sidenav();
    $('#sidenav-2').sidenav({ edge: 'left' });
  });


document.addEventListener('DOMContentLoaded', function() {
      var elems = document.querySelectorAll('.sidenav');
      var instances = M.Sidenav.init(elems, {});
    });
