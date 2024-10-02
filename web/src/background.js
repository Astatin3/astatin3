function getBodyWidth(){
    return document.body.getBoundingClientRect().width;
}

function getBodyHeight(){
    rect = document.body.getBoundingClientRect()
    return Math.max(rect.height, window.innerHeight);
}

const terminal = new CanvasTerminal('terminalCanvas', 
getBodyWidth(), 
getBodyHeight()
);

const HEXAGON_STRING = [
"   ┏┛      ┗┓   ",
"━━━┫        ┣━━━",
"   ┗┓      ┏┛   ",
"    ┣━━━━━━┫    "
];

function hexagon(x, y) {
    let c = HEXAGON_STRING[y % 4][x % 16];
    if(c == " "){return ">"};
    return c;
}

const SQUARES = [
"%───────",
"│       ",
"│       ",
"│       ",
"│       ",
];


function squares(x, y) {
    let c = SQUARES[y % 5][x % 8];
    if(c == " "){return ">"};
    return c;
}

const SQUARES_2 = [
    "........",
    ".       ",
    ".       ",
    ".       ",
    ".       ",
];

function squares_2(x, y) {
    let c = SQUARES_2[y % 5][x % 8];
    if(c == " "){return ">"};
    return c;
}


const TRIANGLES  = [
    " . ",
    ". .",
    ".. ",
];


function triangles(x, y) {
    let c = TRIANGLES[y % 3][x % 3];
    if(c == " "){return ">"};
    return c;
}



const options_length = 6;
function noise2ascii(val, x, y){
//   return (y-1) % 10
  switch(Math.round((val + 1.0) / 2.0 * (options_length - 1))){
    case 0:
        return hexagon(x, y)
    case 1:
        return hexagon(x, y)
    case 2:
        return triangles(x, y)
    case 3:
        return squares(x, y)
    case 4:
        return squares_2(x, y)
    case 5:
        return squares_2(x, y)
  }
} 

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

let scale = 0.1;
let time = 0.0; 
const perlin = new PerlinNoise();

async function noise(){
    for(let y = 0; y < terminal.rows; y++){
        terminal.setCursor(0,y)
        let line = ""
        for(let x = 0; x < terminal.cols; x++){
            line += noise2ascii(perlin.noise(x*scale, y*scale, time), x, y)
        }
        terminal.printLine(line)
    }

    let y = 0;

    let time_scale = terminal.rows * 0.04

    setInterval(function () {
        y++
        if(y > terminal.rows) {
            y = 0
            time += time_scale
        }
        loop_noise(y)
    }, terminal.cols * 0.3);
}
async function loop_noise(y) {
    // for(let y = 0; y < terminal.rows-1; y++){
        terminal.setCursor(0,y)
        let line = ""
        for(let x = 0; x < terminal.cols; x++){
            line += noise2ascii(perlin.noise(x*scale, y*scale, time), x, y)
        }
        terminal.printLine(line)
        // await sleep(terminal.cols)
    // }
    // setTimeout(function () {
    //     noise()
    // }, 5000);
    // loop_noise()
}

window.onresize = function(event) {
    terminal.resize(
        getBodyWidth(), 
        getBodyHeight()
    )
    // noise()
};