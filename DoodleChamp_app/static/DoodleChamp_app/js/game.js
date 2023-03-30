const canvas = document.getElementById("draw-area");
const ctx = canvas.getContext("2d");
let cPushArray = new Array();
let cStep = -1;
let isDrawing = false;
let drawTool = 0;
let colorCode = 0;
let lastX = 0;
let lastY = 0;
let rectX = 0;
let rectY = 0;
let background = null;
var cPic_rect = new Image();

function cPush() {
  cStep++;
  if (cStep < cPushArray.length) { cPushArray.length = cStep; }
  cPushArray.push(canvas.toDataURL());
}
cPush();
function cUndo() {

  if (cStep > 0) {
    cStep--;
    console.log(cStep);
    var cPic = new Image();
    cPic.onload = function () {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(cPic, 0, 0);
    }
    cPic.src = cPushArray[cStep];
    if (cPic.complete) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(cPic, 0, 0);
    }
  }
}

function toggleButton(btn) {
  let button = document.getElementById(btn + "-btn");

  if (button.classList.contains("active")) {
    return;
  }

  let buttons = document.getElementsByClassName("btn btn-secondary btn-sm");
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove("active");
  }

  button.classList.add("active");
}

document.querySelector('#pencil-btn').onclick = function (e) {
  drawTool = 0;
};

document.querySelector('#rectangle-btn').onclick = function (e) {
  drawTool = 1;
};

document.querySelector('#line-btn').onclick = function (e) {
  drawTool = 2;
};

document.querySelector('#circle-btn').onclick = function (e) {
  drawTool = 3;
};

document.querySelector('#undo-btn').onclick = function () {
  cUndo();
};

document.querySelector('#color-val').onchange = function () {
  colorCode = document.querySelector('#color-val').value;
};


canvas.addEventListener('mousedown', (event) => {

  isDrawing = true;
  lastX = event.clientX - canvas.offsetLeft;
  lastY = event.clientY - canvas.offsetTop;
  background = canvas.toDataURL();


});
chatSocket.onopen = function (e){
  chatSocket.send(JSON.stringify({
    'type': "get_player_list"
  }))

}

chatSocket.onmessage = function(e){
  
  let data = JSON.parse(e.data);

  switch(data.type) {
    case "draw_stroke":
      ctx.strokeStyle = colorCode;
      ctx.beginPath();
      ctx.moveTo(data.lastX, data.lastY);
      ctx.lineTo(data.currentX, data.currentY);
      ctx.stroke();
      break;
  }
}
canvas.addEventListener('mousemove', (event) => {


  if (isDrawing && drawTool === 0) {
    //drawing with pencil
    const currentX = event.clientX - canvas.offsetLeft;
    const currentY = event.clientY - canvas.offsetTop;
    ctx.strokeStyle = colorCode
    // ctx.beginPath();
    // ctx.moveTo(lastX, lastY);
    // ctx.lineTo(currentX, currentY);
    // ctx.stroke();    
    chatSocket.send(JSON.stringify({
      'type': "draw_stroke",
      'lastX': lastX,
      'lastY': lastY,
      'currentX': currentX,
      'currentY': currentY
    }))
   
    lastX = currentX;
    lastY = currentY;
   };

  if (isDrawing && drawTool === 1) {
    //live rectangle view

    const currentX = event.clientX - canvas.offsetLeft;
    const currentY = event.clientY - canvas.offsetTop;


    cPic_rect.onload = function () {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(cPic_rect, 0, 0);
    }
    cPic_rect.src = background;
    if (cPic_rect.complete) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(cPic_rect, 0, 0);
    }

    // if (cPic_rect.complete) {
    //     ctx.clearRect(0, 0, canvas.width, canvas.height);
    //     ctx.drawImage(cPic_rect, 0, 0);
    // }

    ctx.beginPath();
    ctx.rect(lastX, lastY, currentX - lastX, currentY - lastY);
    ctx.strokeStyle = colorCode;
    ctx.stroke();

  };

});

canvas.addEventListener('mouseup', (event) => {
  isDrawing = false;
  if (drawTool == 1) {
    //drawing rectangle
    const currentX = event.clientX - canvas.offsetLeft;
    const currentY = event.clientY - canvas.offsetTop;
    ctx.strokeStyle = colorCode
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.rect(lastX, lastY, currentX - lastX, currentY - lastY);
    ctx.stroke();
  }

  if (drawTool === 2) {
    //drawing line
    const currentX = event.clientX - canvas.offsetLeft;
    const currentY = event.clientY - canvas.offsetTop;
    ctx.strokeStyle = colorCode
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(currentX, currentY);
    ctx.stroke();
  }

  if (drawTool === 3) {
    //drawing circle
    const currentX = event.clientX - canvas.offsetLeft;
    const currentY = event.clientY - canvas.offsetTop;
    ctx.strokeStyle = colorCode
    ctx.beginPath();
    ctx.arc(currentX - (currentX - lastX) / 2, currentY - (currentY - lastY) / 2, (currentX - lastX) / 2, 0 * Math.PI, 2 * Math.PI)
    ctx.stroke();
  }

  cPush();
});