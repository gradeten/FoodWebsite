var pName = document.getElementById('pName');
pName.innerHTML=`언어`;

var pRate = document.getElementById("pRate");
pRate.innerHTML="언어";

var pAddress = document.getElementById("pAddress");
pAddress.innerHTML="언어";

var pTel = document.getElementById("pTel");
pTel.innerHTML="언어";

var pCategory = document.getElementById("pCategory");
pCategory.innerHTML="언어";

var pPrice = document.getElementById("pPrice");
pPrice.innerHTML="언어";

var pOPHour = document.getElementById("pOPHour");
pOPHour.innerHTML="언어";

var pParking = document.getElementById("pParking");
pParking.innerHTML="언어";

var pSite = document.getElementById("pSite");
pSite.innerHTML="언어";

var mAmount = document.getElementById("mAmount");
mAmount.innerHTML="언어";
var rAmount = document.getElementById("rAmount");
rAmount.innerHTML="언어";

var rDate1 = document.getElementById("rDate1");
rDate1.innerHTML="언어";
var rDate2 = document.getElementById("rDate2");
rDate2.innerHTML="언어";
var rText1 = document.getElementById("rText1");
rText1.innerHTML="언어";
var rText2 = document.getElementById("rText2");
rText2.innerHTML="언어";





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
