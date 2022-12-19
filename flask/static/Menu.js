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


/*Slider*/

const fileInput = document.getElementById("img");

const handleFiles = (e) => {
  const selectedFile = [...fileInput.files];
  const fileReader = new FileReader();

  fileReader.readAsDataURL(selectedFile[0]);

  fileReader.onload = function () {
    document.getElementById("previewImg").src = fileReader.result;
  };
};

fileInput.addEventListener("change", handleFiles);


function button1_click()
{
  var div = document.createElement('div');
  div.innerHTML = document.getElementById('room_type').innerHTML;
  document.getElementById('field').append(div);

}