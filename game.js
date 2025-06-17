class Paddle {
    constructor() {
        this.width = 100;
        this.height = 20;
        this.x = (canvas.width - this.width) / 2;
        this.y = canvas.height - 50;
        this.speed = 8;
    }

    moveLeft() {
        if (this.x > 0) {
            this.x -= this.speed;
        }
    }

    moveRight() {
        if (this.x < canvas.width - this.width) {
            this.x += this.speed;
        }
    }

    draw(ctx) {
        ctx.fillStyle = '#0000ff';
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
}

class Ball {
    constructor() {
        this.radius = 25;
        this.reset();
    }

    reset() {
        this.x = canvas.width / 2;
        this.y = canvas.height - 70;
        this.speedX = 4 * Math.random() * 2 - 1;
        this.speedY = -4;
    }

    move() {
        this.x += this.speedX;
        this.y += this.speedY;

        // 壁との衝突
        if (this.x <= this.radius || this.x >= canvas.width - this.radius) {
            this.speedX *= -1;
        }
        if (this.y <= this.radius) {
            this.speedY *= -1;
        }
    }

    draw(ctx) {
        ctx.drawImage(ballImage, this.x - this.radius, this.y - this.radius, this.radius * 2, this.radius * 2);
    }
}

class Block {
    constructor(x, y) {
        this.width = 50;
        this.height = 30;
        this.x = x;
        this.y = y;
        this.active = true;
        this.color = `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)})`;
    }

    draw(ctx) {
        if (this.active) {
            ctx.fillStyle = this.color;
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }
}

let canvas = document.getElementById('gameCanvas');
let ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 600;

let paddle = new Paddle();
let ball = new Ball();
let blocks = [];
let score = 0;

// イメージの読み込み
let ballImage = new Image();
ballImage.src = 'corgi-sprite.png';

// サウンドの読み込み
let hitSound = new Audio('hit.wav');

// ゲーム状態
let gameState = 'title';
let titleScreen = document.getElementById('title-screen');
let gameOverScreen = document.getElementById('game-over-screen');
let scoreElement = document.getElementById('score');

// イベントリスナー
let startButton = document.getElementById('startButton');
let retryButton = document.getElementById('retryButton');
let titleButton = document.getElementById('titleButton');

startButton.addEventListener('click', startGame);
retryButton.addEventListener('click', startGame);
titleButton.addEventListener('click', () => {
    gameState = 'title';
    showTitleScreen();
});

document.addEventListener('keydown', (e) => {
    if (gameState === 'playing') {
        if (e.key === 'ArrowLeft') paddle.moveLeft();
        if (e.key === 'ArrowRight') paddle.moveRight();
    }
});

document.addEventListener('touchstart', (e) => {
    if (gameState === 'playing') {
        const touch = e.touches[0];
        const rect = canvas.getBoundingClientRect();
        const x = touch.clientX - rect.left;
        if (x < canvas.width / 2) paddle.moveLeft();
        else paddle.moveRight();
    }
});

// 初期化
function initGame() {
    paddle = new Paddle();
    ball = new Ball();
    blocks = [];
    score = 0;
    
    // ブロックの配置
    for (let row = 0; row < 10; row++) {
        for (let col = 0; col < 20; col++) {
            const x = col * (50 + 5) + 50;
            const y = row * (30 + 5) + 50;
            blocks.push(new Block(x, y));
        }
    }
}

// タイトル画面表示
function showTitleScreen() {
    titleScreen.style.display = 'block';
    gameOverScreen.style.display = 'none';
}

// ゲームオーバー画面表示
function showGameOverScreen() {
    titleScreen.style.display = 'none';
    gameOverScreen.style.display = 'block';
    document.getElementById('finalScore').textContent = `Score: ${score}`;
}

// ゲーム開始
function startGame() {
    gameState = 'playing';
    titleScreen.style.display = 'none';
    gameOverScreen.style.display = 'none';
    initGame();
}

// 衝突判定
function checkCollision() {
    // パドルとの衝突
    if (paddle.x <= ball.x && ball.x <= paddle.x + paddle.width &&
        paddle.y - ball.radius <= ball.y && ball.y <= paddle.y + paddle.height) {
        ball.speedY *= -1;
        playSound(hitSound);
    }

    // ブロックとの衝突
    for (let block of blocks) {
        if (!block.active) continue;

        if (block.x <= ball.x && ball.x <= block.x + block.width &&
            block.y <= ball.y && ball.y <= block.y + block.height) {
            block.active = false;
            ball.speedY *= -1;
            score += 10;
            scoreElement.textContent = `Score: ${score}`;
            playSound(hitSound);
            return true;
        }
    }
    return false;
}

// サウンド再生
function playSound(sound) {
    sound.currentTime = 0;
    sound.play();
}

// ゲームループ
function gameLoop() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'playing') {
        ball.move();
        if (checkCollision()) {
            // ブロックを全て破壊した場合
            if (blocks.every(block => !block.active)) {
                gameState = 'gameOver';
                showGameOverScreen();
            }
        }
        
        // ゲームオーバー判定
        if (ball.y > canvas.height) {
            gameState = 'gameOver';
            showGameOverScreen();
        }

        paddle.draw(ctx);
        ball.draw(ctx);
        blocks.forEach(block => block.draw(ctx));
    }
}

// ゲームループ開始
setInterval(gameLoop, 16);
