const canvas = document.getElementById("draw-area");
const ctx = canvas.getContext("2d");
let cPushArray = new Array();
let cStep = -1;
let isDrawing = false;
let drawTool = -1;
let colorCode = 0;
let lastX = 0;
let lastY = 0;
let rectX = 0;
let rectY = 0;
let background = null;
var cPic_rect = new Image();
let word1 = '';
let value1 = 0;
let word2 = '';
let value2 = 0;


function cPush() {
  cStep++;
  if (cStep < cPushArray.length) { cPushArray.length = cStep; }
  cPushArray.push(canvas.toDataURL());


  ////console.log('first array ' + cPushArray[cStep])

}
cPush();

function cUndo() {

  if (cStep > 0) {
    cStep--;
    ////console.log(cPushArray[cStep]);
    // Drawer sending 
    chatSocket.send(JSON.stringify({
      'type': 'undo',
      'pic': cPushArray[cStep]
    }));
  }
}

function seeWords() {
  ////console.log('seeWords() called')
  chatSocket.send(JSON.stringify({
    'type': 'see_words'
  }));
}

// document.querySelector('#pencil-btn').onclick = function (e) {
//   drawTool = 0;
// };

// document.querySelector('#rectangle-btn').onclick = function (e) {
//   drawTool = 1;
// };

// document.querySelector('#line-btn').onclick = function (e) {
//   drawTool = 2;
// };

// document.querySelector('#circle-btn').onclick = function (e) {
//   drawTool = 3;
// };

// document.querySelector('#undo-btn').onclick = function () {
//   cUndo();
// };

// document.querySelector('#color-val').onchange = function () {
//   colorCode = document.querySelector('#color-val').value;
// };
document.querySelector('#test-btn').onclick = function () {
  
  chatSocket.send(JSON.stringify({
    'type': "draw_turn"
  }))
};

document.querySelector('#end-btn').onclick = function () {
  //console.log("test");
  chatSocket.send(JSON.stringify({
    'type': "turn_ended"
  }))
};

document.querySelector("#word-btn1").onclick = function (){
  // let selected_word = this.innerHTML;
  let selected_word = word1
  console.log('Selected_word: ' + selected_word)
  chatSocket.send(JSON.stringify({
    'type': "set_word",
    'word': selected_word,
    'points': value1
  }));
  chatSocket.send(JSON.stringify({
    'type': "next_player"
  }));
  // console.log("1")
};
//gabriel: this is how the word button should be selected
document.querySelector("#word-btn2").onclick = function (){
  // let selected_word = this.innerHTML;
  let selected_word = word2
  console.log('Selected_word: ' + selected_word)
  chatSocket.send(JSON.stringify({
    'type': "set_word",
    'word': selected_word,
    'points': value2
  }));
  chatSocket.send(JSON.stringify({
    'type': "next_player"
  }));
  // console.log("2")
  
};
//gabriel: this is how the word button should be selected

document.querySelector('#see-words').onclick = function () {
  seeWords();
};

let chatField = document.getElementById("chat-field");

window.onload = function() {
  document.getElementById("chat-field").focus();
}

chatField.addEventListener('keydown', function(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    document.getElementById('')
    let guessBtn = document.getElementById('guess-btn');
    guessBtn.click();
  }
});

document.querySelector('#guess-btn').onclick = function () {
  chatSocket.send(JSON.stringify({
    'type': "guess",
    'guess': document.getElementById("chat-field").value,
    'player': username
  }))
  // console.log(chatField.value)
  chatField.value = "";

};


canvas.addEventListener('mousedown', (event) => {

  isDrawing = true;
  lastX = event.clientX - canvas.offsetLeft;
  lastY = event.clientY - canvas.offsetTop;
  background = canvas.toDataURL();


});



// Client getting the messages
chatSocket.onmessage = function(e){
  let draw_tool_row = document.getElementById('draw-tools');
  let data = JSON.parse(e.data);
  let wordList = document.getElementById("words-list");
  let playerList = document.getElementById("player-list");
  let hidden_word = document.getElementById("hidden-word");
  let chatDiv = document.getElementById('chat-div');
  let scoreboard = document.getElementById('scoreboard')
  

  switch(data.type) {
    case "add_players":
      ptag = document.createElement('p');
      ptag.innerHTML = data.player;
      playerList.appendChild(ptag);
      break;
    case "delete_players":
        //let playerList = document.getElementById("player-list");        
        let pElements = playerList.getElementsByTagName('p');

        // Loop through all p elements and remove them from the div
        while (pElements.length > 0) {
          playerList.removeChild(pElements[0]);
          //console.log("removed");
        }
      break;
    case "draw_stroke":
      ctx.strokeStyle = data.strokeStyle;
      ctx.beginPath();
      ctx.moveTo(data.lastX, data.lastY);
      ctx.lineTo(data.currentX, data.currentY);
      ctx.stroke();
      break;
    
    case "undo":
      //console.log('data pic: ' + data.pic);
      var cPic = new Image();
      cPic.onload = function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(cPic, 0, 0);
      }
      cPic.src = data.pic;
      //console.log('case undo2');
      break;
    case "show_drawer":
      
        let curr_drawer = document.getElementsByClassName("isDrawer");
        if (curr_drawer.length > 0){
          curr_drawer[0].classList.remove("isDrawer");
        }

        var pElems = document.getElementsByTagName("p");
        for (var i = 0; i < pElems.length; i++) {
          //console.log(pElems[i].innerHTML);
          if (pElems[i].innerHTML === data.player) {
            //console.log(data.player);
            pElems[i].classList.add("isDrawer");
          }
        }
        
      break;
    case "draw_turn":
      if (data.player === username){
        let modalBtn = document.getElementById('see-words');
        modalBtn.click();
        drawTool = 0;
        draw_tool_row.innerHTML = '<div id="draw-buttons"> Draw <button id="pencil-btn" class="btn-sm" onclick="pencil">&#9998</button> <button id="rectangle-btn" class="btn-sm" onclick="rectangle">&#11036</button><button id="line-btn" class="btn-sm" onclick="line">&#8213</button><button id="circle-btn" class="btn-sm" onclick="circle">&#x25EF</button><button id="undo-btn">undo</button><input type="Color" id="color-val" name="" class="form-control form-control-color" value="#000000"></div>';
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
      };

      break;
    case "turn_ended":

      draw_tool_row.innerHTML = "";

      drawTool = -1; // means no tool selected
      //console.log("w");
      // let endbtn = document.getElementById('end-btn');
      // endbtn.click();
      break;

      
    case "see_words":
      let pWords = wordList.getElementsByTagName('p');

      // Loop through all p elements and remove them from the div
      while (pWords.length > 0) {
        wordList.removeChild(pWords[0]);
        console.log("removed words");
      }
      // console.log('word1: ' + data.word1)
      // console.log('value1: ' + data.value1)
      // console.log('word2: ' + data.word2)
      // console.log('value2: ' + data.value2)
      ptag = document.createElement('p');
      ptag.innerHTML = data.word1 + ' -> ' + data.value1 + '<br>' + data.word2 + ' -> ' + data.value2;
      wordList.appendChild(ptag);
      word1 = data.word1
      value1 = data.value1
      word2 = data.word2
      value2 = data.value2
      break;

    case "hidden_word":
      //console.log(data.word);
      hidden_word.innerText = "Word: " + data.word;
      break;

    case "guess_return":
      pGuess = document.createElement('p');
      pGuess.innerHTML = data.msg
      chatDiv.appendChild(pGuess);
      console.log('case guess_return')
      break;
    
    case "end_game":
      ptag = document.createElement('p');
      ptag.innerHTML = data.player;
      scoreboard.appendChild(ptag);
      break;
      
      break;
    
  }
}
canvas.addEventListener('mousemove', (event) => {


  if (isDrawing && drawTool === 0) {
    //drawing with pencil
    const currentX = event.clientX - canvas.offsetLeft;
    const currentY = event.clientY - canvas.offsetTop;
    ctx.strokeStyle = colorCode
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(currentX, currentY);
    ctx.stroke();    
    chatSocket.send(JSON.stringify({
      'type': "draw_stroke",
      'lastX': lastX,
      'lastY': lastY,
      'currentX': currentX,
      'currentY': currentY,
      'strokeStyle': colorCode
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