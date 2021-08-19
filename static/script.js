function showMenu()
{
    var menu = document.getElementById('menu')
    var menuButton = document.getElementById('menuButton')
    if(menu.style.left == "-10vw") {
        menu.style.left = '0';
        menuButton.style.left = '10vw';
        menuButton.innerText = "<";
    } else if (menu.style.left == "0px")  {
        menu.style.left = '-10vw';
        menuButton.style.left = '0';
        menuButton.innerText = ">";
    }
}
