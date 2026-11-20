var video = document.querySelector("#vid"),
       canvas = document.querySelector('#canvas'),
       ctx = canvas.getContext('2d'),
       localMediaStream = null,
       onCameraFail = function (e) {
            console.log('Camera did not work.', e); // Исключение на случай, если камера не работает
        };
       navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
        window.URL = window.URL || window.webkitURL;
        navigator.getUserMedia({video: true}, function(stream) {
            video.src = window.URL.createObjectURL(stream);
            localMediaStream = stream;
        }, onCameraFail);