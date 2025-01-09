const puppeteer = require('puppeteer');
const fs = require('fs');
const net = require('net');

const BOT_TIMEOUT = process.env.BOT_TIMEOUT || 2*1000;

const puppeter_args = {};

(async function(){
  const browser = await puppeteer.launch(puppeter_args);

  function ask_for_url(socket) {
      socket.state = 'URL';
      socket.write('Please send me a URL to open.\n');
  }

  async function load_url(socket, data) {
    let url = data.toString().trim();
    console.log(`checking url: ${url}`);
    // replace with your server as needed
    if (!url.startsWith('http://localhost:1234/') && !url.startsWith('https://localhost:1234/')) {
      socket.state = 'ERROR';
      socket.write('Invalid URL (must start with http:// or https://).\n');
      socket.destroy();
      return;
    }
    socket.state = 'LOADED';
    let cookie = JSON.parse(fs.readFileSync('/home/user/cookie'));

    const context = await browser.createBrowserContext();
    const page = await context.newPage();
    await page.setJavaScriptEnabled(false);
    await page.setCookie(cookie);
    socket.write(`Loading page ${url}.\n`);
    setTimeout(()=>{
      try {
        context.close();
        socket.write('timeout\n');
        socket.destroy();
      } catch (err) {
        console.log(`err: ${err}`);
      }
    }, BOT_TIMEOUT);
    await page.goto(url);
  }

  var server = net.createServer();
  server.listen(1338);
  console.log('listening on port 1338');

  server.on('connection', socket=>{
    socket.on('data', data=>{
      try {
        if (socket.state == 'URL') {
          load_url(socket, data);
        }
      } catch (err) {
        console.log(`err: ${err}`);
      }
    });

    try {
      ask_for_url(socket);
    } catch (err) {
      console.log(`err: ${err}`);
    }
  });
})();

