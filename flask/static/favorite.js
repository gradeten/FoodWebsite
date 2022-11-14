let popup = document.getElementById("popup");
let check = false;

    function openPopup(){
        if (check == false)
        {
            popup.classList.add("open-popup");
            check = true;
        }
        else
        {
            popup.classList.remove("open-popup");
            check = false;
        }
    }
