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
      recBtn.classList.add("button-loading");
      recBtn.setAttribute("disabled", "true");
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
        let jsonData = JSON.parse(data);
        let responseDOMCont = document.querySelector("#response-cont");
        responseDOMCont.innerHTML = "You said: " + jsonData.text;
        setTimeout(() => {
          responseDOMCont.innerHTML = "";
        }, 5000);
        recBtn.classList.remove("button-loading");
        recBtn.removeAttribute("disabled");
        if (jsonData.action_required) textToSpeech(jsonData.text);
      })
      .catch((error) => {
        recBtn.classList.remove("button-loading");
        recBtn.removeAttribute("disabled");
        textToSpeech("Perkele, something went wrong!");
        throw error;
      });
  }

  function textToSpeech(text) {
    var msg = new SpeechSynthesisUtterance();
    msg.text = text;
    window.speechSynthesis.speak(msg);
  }
}

init();
