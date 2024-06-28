document
  .getElementById("upload-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append("file", document.getElementById("file-input").files[0]);

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);

    xhr.upload.onprogress = function (event) {
      if (event.lengthComputable) {
        let percentComplete = (event.loaded / event.total) * 100;
        document.getElementById("progress-bar").value = percentComplete;
        document.getElementById(
          "progress-status"
        ).innerText = `Uploading: ${percentComplete.toFixed(2)}%`;
      }
    };

    xhr.onload = function () {
      if (xhr.status === 202) {
        let response = JSON.parse(xhr.responseText);
        let taskId = response.task_id;
        checkTaskStatus(taskId);
      } else {
        document.getElementById(
          "progress-status"
        ).innerText = `Error: ${xhr.responseText}`;
      }
    };

    xhr.send(formData);
  });

function checkTaskStatus(taskId) {
  let xhr = new XMLHttpRequest();
  xhr.open("GET", `/status/${taskId}`, true);

  xhr.onload = function () {
    if (xhr.status === 200) {
      let response = JSON.parse(xhr.responseText);
      document.getElementById("progress-status").innerText = response.status;

      if (response.state === "SUCCESS") {
        document.getElementById("progress-status").innerText =
          "Conversion completed!";
        let downloadLink = document.createElement("a");
        downloadLink.href = `/download/${response.result}`;
        downloadLink.innerText = "Download your audiobook";
        document.getElementById("progress-status").appendChild(downloadLink);
      } else {
        setTimeout(function () {
          checkTaskStatus(taskId);
        }, 1000);
      }
    } else {
      document.getElementById(
        "progress-status"
      ).innerText = `Error: ${xhr.responseText}`;
    }
  };

  xhr.send();
}
