const http = require('http');
const app = require('./app');

const port = 8080;

const server = http.createServer(app);

server.listen(port, 'localhost', function() {
    console.log('Application worker ' + process.pid + ' started...');
});


const ngrok = require('ngrok');

(async function() {
    const url = await ngrok.connect({
        proto: "http", 
        addr: 8080, 
        authtoken: "5b88pKE7ewpjjQyLFFsaR_82d7txPE8XvhNa5rC59vP"
    })
    .then((r) => console.log('Tunnel started on: ' + r))
    .catch((e) => console.log('error', e));;
})();