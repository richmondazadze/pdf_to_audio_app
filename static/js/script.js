document
  .getElementById("upload-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);
    xhr.upload.onprogress = function (event) {
      if (event.lengthComputable) {
        const percentComplete = (event.loaded / event.total) * 100;
        document.getElementById("progress-container").style.display = "block";
        document.getElementById("progress-bar").style.width =
          percentComplete + "%";
      }
    };
    xhr.onload = function () {
      if (this.status === 202) {
        const response = JSON.parse(this.responseText);
        trackProgress(response.task_id);
      } else {
        alert("Upload failed!");
      }
    };
    xhr.send(formData);
  });

function trackProgress(taskId) {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `/status/${taskId}`, true);
  xhr.onload = function () {
    const response = JSON.parse(this.responseText);
    if (response.state === "PENDING" || response.state === "PROGRESS") {
      setTimeout(function () {
        trackProgress(taskId);
      }, 1000);
    } else if (response.state === "SUCCESS") {
      document.getElementById("progress-bar").style.width = "100%";
      alert("Conversion complete! Download your file: " + response.result);
    } else {
      alert("Conversion failed!");
    }
  };
  xhr.send();
}
