const pdf = require('html-pdf-node');
const fs = require('fs');
const path = require('path')



const options = { format: 'A4', path: 'RelatorioOLT.pdf', printBackground:true};

// const fileInHtml = { content: fs.readFileSync('data.html', 'utf8') };

const fileInHtml = { url:`file:///${path.resolve('data.html')}`};

// pdf.create(fileInHtml, options).toFile('businesscard.pdf', function (err, res) {
//     if (err) return console.log(err);
//     console.log(res); // { filename: '/app/businesscard.pdf' }
// });

pdf.generatePdf(fileInHtml, options).then(pdfBuffer => {
    console.log("Conversão realizada com sucesso!");
});
