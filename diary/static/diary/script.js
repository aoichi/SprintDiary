
$(".dropdown-trigger").dropdown();

$(document).ready(function(){
    $('.sidenav').sidenav();
    $('#sidenav-2').sidenav({ edge: 'left' });
    $('.collapsible').collapsible();
  });


  document.addEventListener('DOMContentLoaded', function() {
      M.AutoInit();

      let el = document.querySelector('.tabs');
      let instance = M.Tabs.init(el, {});


      let elem = document.querySelectorAll('.collapsible.expandable');
      let instanceCollapsible = M.Collapsible.init(elem, {
             accordion: false,
             onOpenStart: function(){
                //console.log('collasible Open Start');
          }
      });
  });
