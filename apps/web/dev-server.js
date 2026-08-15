const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.jsx': 'text/javascript',
  '.ts': 'text/javascript',
  '.tsx': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.ogv': 'video/ogg'
};

const MEDIA_MAP = {
  '/images/courtroom.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776774938.jpg',
  '/images/scales.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776775007.jpg',
  '/images/advocates.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776775035.jpg',
  '/images/petition.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776775079.jpg',
  '/images/legal_notice.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776775133.jpg',
  '/images/boardroom.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786780382416.jpg',
  '/images/senior_partner.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786780382429.jpg',
  '/assets/img/boardroom.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786780382416.jpg',
  '/assets/img/senior_partner.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786780382429.jpg',
  '/assets/img/courtroom.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776774938.jpg',
  '/assets/img/supreme-court.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776774938.jpg',
  '/assets/img/evidence-review-poster.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776775079.jpg',
  '/assets/img/document-generation-poster.jpg': 'C:/Users/acer/.gemini/antigravity/brain/feb83fcd-fc3e-4cb1-a12c-aace7f6060e7/.user_uploaded/media_1786776775133.jpg',
};

const server = http.createServer((req, res) => {
  let urlPath = req.url.split('?')[0];
  let filePath;
  
  if (MEDIA_MAP[urlPath]) {
    filePath = MEDIA_MAP[urlPath];
  } else {
    filePath = path.join(__dirname, urlPath === '/' ? 'index.html' : urlPath);
    if (!fs.existsSync(filePath) && !path.extname(filePath)) {
      filePath = path.join(__dirname, 'index.html');
    }
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'text/plain';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        fs.readFile(path.join(__dirname, 'index.html'), (err2, htmlContent) => {
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(htmlContent, 'utf-8');
        });
      } else {
        res.writeHead(500);
        res.end(`Server Error: ${err.code}`);
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType, 'Cache-Control': 'public, max-age=3600' });
      res.end(content);
    }
  });
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`\n  🏛️ Jurisiva AI Web Client UI running at:`);
  console.log(`  > Local: http://127.0.0.1:${PORT}/\n`);
});
