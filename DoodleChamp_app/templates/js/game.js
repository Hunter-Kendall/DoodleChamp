const canvas = document.getElementById("draw-area");
            const ctx = canvas.getContext("2d");
            let cPushArray = new Array();
            let cStep = -1;
            let isDrawing = false;
            let drawTool = 0;
            let colorCode = 0;
            let lastX = 0;
            let lastY = 0;


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

            document.querySelector('#pencil-btn').onclick = function(e){
                drawTool = 0;
            };

            document.querySelector('#rectangle-btn').onclick = function(e){
                drawTool = 1;
            };

            document.querySelector('#line-btn').onclick = function(e){
              drawTool = 2;
            };

            document.querySelector('#circle-btn').onclick = function(e){
              drawTool = 3;
            };

            document.querySelector('#undo-btn').onclick = function(){
                cUndo();
            };

            document.querySelector('#color-val').onchange = function(){
              colorCode = document.querySelector('#color-val').value;
            };


            canvas.addEventListener('mousedown', (event) =>{
            
                isDrawing = true;
                lastX = event.clientX - canvas.offsetLeft;
                lastY = event.clientY - canvas.offsetTop;
                
            
            });

            canvas.addEventListener('mousemove', (event) => {


              if (isDrawing && drawTool == 0) {
                //drawing with pencil
                const currentX = event.clientX - canvas.offsetLeft;
                const currentY = event.clientY - canvas.offsetTop;
                ctx.strokeStyle = colorCode
                ctx.beginPath();
                ctx.moveTo(lastX, lastY);
                ctx.lineTo(currentX, currentY);
                ctx.stroke();
                lastX = currentX;
                lastY = currentY;
              };

            });

            canvas.addEventListener('mouseup', (event) => {
              isDrawing = false;
              if (drawTool == 1){
                //drawing rectangle
                const currentX = event.clientX - canvas.offsetLeft;
                const currentY = event.clientY - canvas.offsetTop;
                ctx.strokeStyle = colorCode
                ctx.beginPath();
                ctx.moveTo(lastX, lastY);
                ctx.rect(lastX, lastY, currentX - lastX, currentY - lastY);
                ctx.stroke();
              }

              if (drawTool === 2){
                //drawing line
                const currentX = event.clientX - canvas.offsetLeft;
                const currentY = event.clientY - canvas.offsetTop;
                ctx.strokeStyle = colorCode
                ctx.beginPath();
                ctx.moveTo(lastX, lastY);
                ctx.lineTo(currentX, currentY);
                ctx.stroke();
              }

              if (drawTool === 3){
                //drawing circle
                const currentX = event.clientX - canvas.offsetLeft;
                const currentY = event.clientY - canvas.offsetTop;
                ctx.strokeStyle = colorCode
                ctx.beginPath();
                ctx.arc(currentX-(currentX-lastX)/2, currentY-(currentY-lastY)/2, (currentX-lastX)/2, 0*Math.PI,2*Math.PI)
                ctx.stroke();
              }

              cPush();
            });