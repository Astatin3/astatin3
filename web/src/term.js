function getTextWidth(text, font) {
    const canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
    const context = canvas.getContext("2d");
    context.font = font;
    const metrics = context.measureText(text);
    return [metrics.width, metrics.actualBoundingBoxAscent + metrics.actualBoundingBoxDescent];
}

class CanvasTerminal {
constructor(canvasId, width, height, fontSize = 10) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');

    this.fontSize = fontSize;
    this.ctx.font = `${this.fontSize}px UbuntuMono`;
    const tmpsize = getTextWidth("█", this.ctx.font);
    this.lineWidth = tmpsize[0] * 0.5
    this.lineHeight = tmpsize[1]

    this.cursor = { x: 0, y: 0 };
    this.foregroundColor = 'white';
    this.backgroundColor = 'black';

    // this.offsetHeight = this.lineHeight*2


    this.ctx.textBaseline = 'top';

    this.resize(width, height);
    this.clear()
}

getRows(){
    return Math.floor(this.canvas.height / this.lineHeight)
}

getCols(){
    return Math.floor(this.canvas.width / this.lineWidth)
}

resetSize(){
    this.rows = this.getRows();
    this.cols = this.getCols();
}

resize(width, height) {
    this.canvas.width = width;
    this.canvas.height = height;
    this.resetSize()
    // this.clear();
}

clear() {
    this.resetSize()
    this.ctx.fillStyle = this.backgroundColor;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.cursor = { x: 0, y: 0 };
}



setCursorX(x) {
    this.cursor.x = Math.max(0, Math.min(x, this.cols - 1));
}

moveCursorX(dx) {
    this.setCursorX(this.cursor.x + dx);
}

setCursorY(y) {
    this.cursor.y = Math.max(0, Math.min(y, this.rows  - 1));
}

moveCursorY(dy) {
    this.setCursorY(this.cursor.y + dy);
}



setCursor(x, y) {
    this.cursor.x = Math.max(0, Math.min(x, this.cols - 1));
    this.cursor.y = Math.max(0, Math.min(y, this.rows - 1));
}

moveCursor(dx, dy) {
    this.setCursor(this.cursor.x + dx, this.cursor.y + dy);
}

printLine(word, fgColor = this.foregroundColor, bgColor = this.backgroundColor) {
    for (const char of word) {
        if(char == ">"){
            this.moveCursorX(1)
            continue
        }

        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(
            this.cursor.x * this.lineWidth,
            this.cursor.y * this.lineHeight,
            this.lineWidth*2,
            this.lineHeight
        );

        this.ctx.fillStyle = fgColor;
        this.ctx.fillText(
            char,
            this.cursor.x * this.lineWidth,
            this.cursor.y * this.lineHeight
        );
        

        this.cursor.x++;
        if (this.cursor.x >= this.cols) {
            this.cursor.y++;
            this.cursor.x = 0;
            if (this.cursor.y >= this.rows) {
                this.cursor.y = 0;
            }
        }
    }
}

scrollUp() {
    const imageData = this.ctx.getImageData(
    0, this.lineHeight, this.canvas.width, this.canvas.height - this.lineHeight
    );
    this.ctx.putImageData(imageData, 0, 0);
    this.ctx.fillStyle = this.backgroundColor;
    this.ctx.fillRect(
    0, (this.height - 1) * this.lineHeight,
    this.canvas.width, this.lineHeight
    );
    this.cursor.y--;
}
}
