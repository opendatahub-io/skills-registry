(function () {
  var shade;
  var iframe;

  var insertFrame = function () {
    shade = document.createElement("div");
    shade.classList.add("drawio-shade");
    iframe = document.createElement("iframe");
    shade.appendChild(iframe);
    document.body.appendChild(shade);
  };

  var closeFrame = function () {
    if (shade) {
      document.body.removeChild(shade);
      shade = undefined;
      iframe = undefined;
    }
  };

  var imghandler = function (img, imgdata) {
    var url = "https://embed.diagrams.net/";
    url += "?embed=1&ui=atlas&spin=1&modified=unsavedChanges&proto=json&saveAndEdit=1&noSaveBtn=1";

    var wrapper = document.createElement("div");
    wrapper.classList.add("drawio-wrapper");
    img.parentNode.insertBefore(wrapper, img);
    wrapper.appendChild(img);

    var btn = document.createElement("button");
    btn.classList.add("drawio-edit-btn");
    btn.setAttribute("title", "Edit this diagram in draw.io");
    btn.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">' +
      '<path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>' +
      "</svg> Edit";

    wrapper.appendChild(btn);

    btn.addEventListener("click", function () {
      if (iframe) return;
      insertFrame();

      var handler = function (evt) {
        var wind = iframe.contentWindow;
        if (evt.data.length > 0 && evt.source == wind) {
          var msg = JSON.parse(evt.data);

          if (msg.event == "init") {
            wind.postMessage(
              JSON.stringify({ action: "load", xml: imgdata }),
              "*"
            );
          } else if (msg.event == "save") {
            var fmt =
              imgdata.indexOf("data:image/png") == 0 ? "xmlpng" : "xmlsvg";
            wind.postMessage(
              JSON.stringify({ action: "export", format: fmt }),
              "*"
            );
          } else if (msg.event == "export") {
            var fn = img.src.replace(/^.*?([^/]+)$/, "$1");
            var dl = document.createElement("a");
            dl.setAttribute("href", msg.data);
            dl.setAttribute("download", fn);
            document.body.appendChild(dl);
            dl.click();
            dl.parentNode.removeChild(dl);
          }

          if (msg.event == "exit" || msg.event == "export") {
            window.removeEventListener("message", handler);
            closeFrame();
          }
        }
      };

      window.addEventListener("message", handler);
      iframe.setAttribute("src", url);
    });
  };

  document.addEventListener("DOMContentLoaded", function () {
    for (var i = 0; i < document.images.length; i++) {
      (function (img) {
        var src = img.getAttribute("src");
        if (!src || (!src.endsWith(".svg") && !src.endsWith(".png"))) return;

        var fullSrc = new URL(src, window.location.href).href;
        var xhr = new XMLHttpRequest();
        xhr.responseType = "blob";
        xhr.open("GET", fullSrc);
        xhr.addEventListener("load", function () {
          var fr = new FileReader();
          fr.addEventListener("load", function () {
            if (fr.result.indexOf("mxfile") != -1) {
              var fr2 = new FileReader();
              fr2.addEventListener("load", function () {
                imghandler(img, fr2.result);
              });
              fr2.readAsDataURL(xhr.response);
            }
          });
          fr.readAsBinaryString(xhr.response);
        });
        xhr.send();
      })(document.images[i]);
    }
  });
})();
