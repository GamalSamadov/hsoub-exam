// VideoPlayer modal
var VideoPlayer = document.getElementById("videoPlayer");

// when shown
VideoPlayer.addEventListener("show.bs.modal", function (event) {
  var button = event.relatedTarget;
  // get video ID
  var vid = button.getAttribute("data-bs-vid");

  var modalTitle = VideoPlayer.querySelector(".modal-title");
  var modalBodyInput = VideoPlayer.querySelector(".modal-body iframe");

  // change modal title and iframe src
  modalTitle.textContent = button.getAttribute("data-bs-title");
  modalBodyInput.src = "https://player.vimeo.com/video/" + vid;
});

// when hidden
VideoPlayer.addEventListener("hide.bs.modal", function (event) {
  // to stop video from playing in background after closing the modal
  VideoPlayer.querySelector(".modal-body iframe").src = "#";
});
