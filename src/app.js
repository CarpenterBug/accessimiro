const { board } = window.miro;

async function init() {
  var recorder;

  navigator.mediaDevices
    .getUserMedia({
      audio: true,
      video: false,
    })
    .then(async function (stream) {
      recorder = RecordRTC(stream, {
        type: "audio",
        mimeType: "audio/wav",
        recorderType: StereoAudioRecorder,
        numberOfAudioChannels: 1,
      });
    });

  let recBtn = document.querySelector("#record-btn");

  recBtn.addEventListener("click", () => {
    if (recBtn.classList.contains("button-danger")) {
      recorder.stopRecording(function () {
        let blob = recorder.getBlob();
        // invokeSaveAsDialog(blob);
        console.log("MAD blob", blob);
        sendData(blob);
      });

      recBtn.innerHTML = "Record Command";
      recBtn.classList.remove("button-danger");
    } else {
      console.log("recording");

      recBtn.innerHTML = "Recording";
      recBtn.classList.add("button-danger");

      recorder.startRecording();
    }
  });

  function sendData(blob) {
    let formData = new FormData();
    // formData.append("file", blob);
    formData.append("file", blob, "mad.wav");
    formData.append("title", "MAD audio file");

    recorder.reset();

    fetch("https://dgculturecommittee.me/submit", {
      method: "POST",
      cors: "no-cors",
      body: formData,
    })
      .then(function (response) {
        return response.text();
      })
      .then(function (data) {
        console.log(data);
      });
  }

  //   invokeSaveAsDialog(blob);
  /*
    var recorder;
  navigator.mediaDevices
    .getUserMedia({
      audio: true,
      video: false,
    })
    .then(async function (stream) {
      recorder = RecordRTC(stream, {
        type: "audio",
        mimeType: "audio/wav",
        recorderType: StereoAudioRecorder,
        numberOfAudioChannels: 1,
        ondataavailable: function (blob) {
          console.log("blob", blob);

          let formData = new FormData();
          formData.append("file", blob, "audio.wav");

          fetch("https://dgculturecommittee.me/submit", {
            method: "POST",
            cors: "no-cors",
            body: form,
          })
            .then(function (response) {
              return response.text();
            })
            .then(function (data) {
              console.log(data);
            });
        },
      });

      let blob;
      let recBtn = document.querySelector("#record-btn");

      recBtn.addEventListener("click", () => {
        if (recBtn.classList.contains("button-danger")) {
          recorder.stopRecording(function () {
            blob = recorder.getBlob();
          });

          recBtn.innerHTML = "Record Command";
          recBtn.classList.remove("button-danger");
        } else {
          console.log("recording");

          recBtn.innerHTML = "Recording";
          recBtn.classList.add("button-danger");

          recorder.startRecording();
        }
      });
    });
    */

  /* ----- */

  /*
  var recorder;
  let responseDOMCont = document.querySelector("#response-cont");

  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      // store streaming data chunks in array
      const chunks = [];

      // create media recorder instance to initialize recording
      recorder = new MediaRecorder(stream);
      // function to be called when data is received
      recorder.ondataavailable = (e) => {
        // add stream data to chunks
        chunks.push(e.data);
        // if recorder is 'inactive' then recording has finished
        if (recorder.state == "inactive") {
          console.log("recording finished");

          const blob = new Blob(chunks, { type: "audio/webm" });
          // send blob to server
          //send audio to wit.ai
          var data = new FormData();
          data.append("audio", blob, "audio.wav");

          fetch("https://dgculturecommittee.me/submit", {
            method: "POST",
            cors: "no-cors",
            body: data,
          })
            .then(function (response) {
              return response.text();
            })
            .then(function (data) {
              console.log(data);
            });

          while (chunks.length > 0) chunks.pop();
        }
      };
      let recBtn = document.querySelector("#record-btn");

      recBtn.addEventListener("click", () => {
        if (recBtn.classList.contains("button-danger")) {
          recorder.stop();

          recBtn.innerHTML = "Record Command";
          recBtn.classList.remove("button-danger");
        } else {
          console.log("recording");

          recBtn.innerHTML = "Recording";
          recBtn.classList.add("button-danger");

          recorder.start();
        }
      });
    })
    .catch(console.error);
    */
}

init();
