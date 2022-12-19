function setStarRating(rating) {
    for (var i = 1; i <= 5; i++) {
        var el = document.getElementById("star" + i);
        el.classList.remove("checked");
    }

    for (var i = 1; i <= rating; i++) {
        var el = document.getElementById("star" + i);
        el.classList.add("checked");
    }
    
    document.getElementById("star_rating").value = rating;
}

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById('preview').src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    document.getElementById('preview').src = "";
  }
}